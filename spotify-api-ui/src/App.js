import React, {useEffect, useState} from 'react';
import './App.css';
import { Button, TextField } from '@material-ui/core';
import { withStyles, makeStyles } from '@material-ui/core/styles';

const client_secret = "sample_client_secret"; // Your client secret
const client_id = "sample_client_id"; // Your client id
const redirect_uri = "http://127.0.0.1:5000"; // Your redirect uri
const scope = [
  "user-read-private",
  "user-read-email",
  "playlist-read-private",
  "playlist-modify-public",
  "playlist-modify-private"
];
const scope_url = scope.join("%20")
const auth_url = "https://accounts.spotify.com/authorize";

const full_auth_url = `${auth_url}?client_id=${client_id}&redirect_uri=${redirect_uri}&scope=${scope_url}&response_type=token&state=123&show_dialog=true`;


const App = () => {

  useEffect(() => {
    if(window.location.hash) {
      const params_obj = getParams(window.location.hash);
      localStorage.setItem("objectparam", JSON.stringify(params_obj));
      localStorage.setItem("accessToken", JSON.stringify(params_obj.access_token))
      sendParams();
    }
  })
  
  const getParams = (hash) => {
    var params = {};
    const split_params = hash.substring(1).split("&");
    var i;
    for (i = 0; i < split_params.length; i++) {
      const [key, value] = split_params[i].split("=");
      params[key] = value;
    }
    return params;
  }

  const authenticateUser = () => {
    window.location = full_auth_url
  }

  const createPlaylist = async () => {
    await fetch('/send-current-user-info', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then(
      response => {
        console.log(response)
    })
    window.location = "/create-playlist"
  }

  const sendParams = async () => {
    const params = JSON.parse(localStorage.getItem("objectparam"));
    await fetch('/send-access-token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params)
    })
    .then(
      response => {
        console.log(response)
    })
  }
  
  const useStyles = makeStyles((theme) => ({
    margin: {
      margin: theme.spacing(1),
    },
  }));

  const BootstrapButton = withStyles({
    root: {
      boxShadow: 'none',
      textTransform: 'none',
      fontSize: 16,
      padding: '6px 12px',
      border: '1px solid',
      lineHeight: 1.5,
      backgroundColor: '#9e4c41',
      borderColor: '#9e4c41',
      fontFamily: 'Futura',
      fontStyle: 'italic',
      '&:hover': {
        backgroundColor: '#b56257',
        borderColor: '#b56257',
        boxShadow: 'none',
      },
      '&:active': {
        boxShadow: 'none',
        backgroundColor: '#9e4c41',
        borderColor: '#9e4c41',
      },
      '&:focus': {
        boxShadow: '0 0 0 0.2rem rgba(0,123,255,.5)',
      },
    },
  })(Button);

  const [userID, setuserID] = useState('');
  const checkUserExists = async () => {
    const accessToken = JSON.parse(localStorage.getItem("accessToken"));
    await fetch(`https://api.spotify.com/v1/users/${userID}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        "Authorization": `Bearer ${accessToken}`
      },
    })
    .then(
      response => {
        console.log(response)
        if (response.ok) {
          fetch(`/send-friends-user-info?user_id=${userID}`)
        }
        else {
        }
    })
  }
  
  return (
    <div className="App">
      <div className="section">
        <p className="title">
          OUR SHARED TRACKS
        </p>
      </div>
      <div className="section">
          <BootstrapButton variant="contained" color="secondary" onClick={authenticateUser}>Login With Spotify</BootstrapButton>
      </div>
      <div className="section">
        <p className="paragraphs">Enter your friend's Spotify user name:</p>
        <TextField required variant="outlined" id="outlined-required" label="Required" placeholder="friend's user name" defaultValue="" onChange={(event) => {setuserID(event.target.value)}} />
        <BootstrapButton variant="contained" color="primary" className={useStyles.margin} onClick={checkUserExists}>Check User</BootstrapButton>
      </div>
      <div className="section">
        <BootstrapButton variant="contained" color="primary" className={useStyles.margin} onClick={createPlaylist}>Create Playlist With Our Shared Tracks!</BootstrapButton>
      </div>
    </div>
  );
}

export default App;
