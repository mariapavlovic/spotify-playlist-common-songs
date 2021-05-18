# step 1: get current user's playlist - Get a List of Current User's Playlists - get https://api.spotify.com/v1/me/playlists
# step 2: get friend's user playlist - Get a List of a User's Playlists - get https://api.spotify.com/v1/users/{user_id}/playlists
# step 3: compare and find common tracks - Get a Playlist's Items - get https://api.spotify.com/v1/playlists/{playlist_id}/tracks
# step 4: get track URIs - Search for an Item - get https://api.spotify.com/v1/search
# step 5: create new playlist - Create a Playlist - post https://api.spotify.com/v1/users/{user_id}/playlists
# step 6: add common tracks to new playlist - Add Items to a Playlist - post https://api.spotify.com/v1/playlists/{playlist_id}/tracks

import json
import requests
import flask
from flask import request

app = flask.Flask(__name__)

@app.route("/")
def my_index():
    return flask.render_template("index.html", token="Flask+React")


@app.route("/send-access-token", methods=['POST'])
def save_access_token():
    file = open("private-info.txt", "w")
    file.write(request.json['access_token']+"\n")
    # file.write("access_token=\""+request.json['access_token']+"\"\n")
    # file.write("expires_in="+request.json['expires_in']+"\n")
    # file.write("token_type=\""+request.json['token_type']+"\"\n")
    file.close()
    return "success"


@app.route("/create-playlist")
def create_playlist():
    a = MySpotifyApi()
    a.add_tracks_to_new_playlist()
    return "success"


@app.route("/send-friends-user-info")
def save_friends_user_info():
    user_id = request.args.get('user_id')
    file = open("private-info.txt", "a")
    file.write(user_id+"\n")  
    file.close()  
    return "success" 


@app.route("/send-current-user-info")
def save_current_user_info():
    access_token = file.readlines().rstrip()
    print(access_token)
    file = open("private-info.txt", "a")
    query = "https://api.spotify.com/v1/me"
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
    )
    response_json = response.json()
    user_id = response_json["id"]
    file = open("private-info.txt", "a")
    file.write(user_id+"\n")
    file.close()
    return "success" 


class MySpotifyApi: 
    def __init__(self):
        file = open("private-info.txt", "r")
        self.access_token = file.readlines()[0].rstrip()
        self.friend_id = file.readlines()[1]
        self.user_id = file.readlines()[2]
        file.close()


    def get_my_playlist_ids(self):
        query = "https://api.spotify.com/v1/me/playlists"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.access_token)
            }
        )
        response_json = response.json()
        return [o["id"] for o in response_json["items"]]


    def get_friends_playlist_ids(self, my_friends_user_id):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(my_friends_user_id)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.access_token)
            }
        )
        response_json = response.json()
        return [o["id"] for o in response_json["items"]]


    def get_my_playlist_track_uris(self):
        my_playlist_ids = self.get_my_playlist_ids()
        num_of_playlists = len(my_playlist_ids)
        response_json = []

        for i in range(num_of_playlists):
            query = "https://api.spotify.com/v1/playlists/{}/tracks".format(my_playlist_ids[i])
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            playlists_track_uris = [o["track"]["uri"] for o in response.json()["items"]]
            response_json.extend(playlists_track_uris)
        
        return response_json


    def get_friends_playlist_track_uris(self, friends_user_id):
        friends_playlist_ids = self.get_friends_playlist_ids(friends_user_id)
        num_of_playlists = len(friends_playlist_ids)
        response_json = []

        for i in range(num_of_playlists):
            query = "https://api.spotify.com/v1/playlists/{}/tracks".format(friends_playlist_ids[i])
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            playlists_track_uris = [o["track"]["uri"] for o in response.json()["items"]]
            response_json.extend(playlists_track_uris)

        return response_json


    def find_common_tracks(self):
        my_track_uris = self.get_my_playlist_track_uris()
        friends_track_uris = self.get_friends_playlist_track_uris(self.friend_id)
        return list(set(my_track_uris).intersection(friends_track_uris))
    
    
    def create_new_playlist(self):
        request_body = json.dumps({
            "name": "Our Joint Playlist123",
            "description": "Common playlist tracks between us",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.access_token)
            }
        )
        response_json = response.json()
        return response_json["id"]


    def add_tracks_to_new_playlist(self):
        new_playlist_id = self.create_new_playlist()
        request_data = json.dumps({
            "uris": self.find_common_tracks()
        })

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(new_playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.access_token)
            }
        )

        response_json = response.json()
        return response_json


if __name__ == "__main__":
    app.run(debug=True)
