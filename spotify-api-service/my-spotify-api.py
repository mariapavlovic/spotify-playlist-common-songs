# step 1: get current user's playlist - Get a List of Current User's Playlists - get https://api.spotify.com/v1/me/playlists
# step 2: get friend's user playlist - Get a List of a User's Playlists - get https://api.spotify.com/v1/users/{user_id}/playlists
# step 3: compare and find common tracks - Get a Playlist's Items - get https://api.spotify.com/v1/playlists/{playlist_id}/tracks
# step 4: get track URIs - Search for an Item - get https://api.spotify.com/v1/search
# step 5: create new playlist - Create a Playlist - post https://api.spotify.com/v1/users/{user_id}/playlists
# step 6: add common tracks to new playlist - Add Items to a Playlist - post https://api.spotify.com/v1/playlists/{playlist_id}/tracks

import json
import requests
import flask

@app.route("/")
app = flask.Flask("__main__")

class MySpotifyApi: 
    
    def my_index():
        return flask.render_template("index.html", token="Flask+React")

    def __init__(self):
        self.user_id = "mariatronn"
        self.friend_id = "choiclara1"
        self.access_token = "BQAyQxS1K3XhKxYIJNIktlh6vqRlbMScyM9bUtblJma9GrXaU_cN0kDQZB9OXN6GiT8vuakVWA8qvS1Km5Rd4eLtXj0vwiBFyyWotCgjj0xvfObHBWpeV5e_O_Pm2pGJ02UlRukfUN1lYuPVGQ3jn_f6gc3-NXKnXYpF_bDoVbeW0PS549TgKShR2dKtncylg3bhYjvNC6R-QoI3LHLooW8"


    def set_access_token(self, access_token):
        self.access_token = access_token


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
            "name": "Our Joint Playlist",
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


app.run(debug=False)
# a = MySpotifyApi()

# a.get_my_playlist_ids()

# a.get_friends_playlist_ids("choiclara1")

# my_tracks = a.get_my_playlist_track_uris()

# friends_tracks = a.get_friends_playlist_track_uris("choiclara1")

# print(a.find_common_tracks(my_tracks, friends_tracks))

# print(a.add_tracks_to_new_playlist())