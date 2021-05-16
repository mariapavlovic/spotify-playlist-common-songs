import './App.css';
import React, { Component } from 'react'
// import MySpotifyApi from 'my-spotify-api'

class App extends Component {
  constructor() {
    super();
    const params = this.getHashParams();
    this.state = params.access_token ? true:false
  }
  getHashParams() {
    var hashParams = {};
    var e, r = /([^&;=]+)=?([^&;]*)/g,
        q = window.location.hash.substring(1);
    while ( e = r.exec(q)) {
        hashParams[e[1]] = decodeURIComponent(e[2]);
    }
    return hashParams;
  }

  // spotifyApi = MySpotifyApi.__init__()
  
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>
            COMMON SONGS
          </p>
          <a href="http://localhost:8888">
            <button>Login With Spotify</button>
          </a>

          <button>Create Playlist With Common Songs!</button>
        </header>
      </div>
    );
  }
  
}

export default App;
