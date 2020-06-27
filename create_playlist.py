#Step 1: Log into YouTube
#Step 2: Grab the liked videos
#Step 3: Create a New Playlist
#Step 4: Search for the Song
#Step 5: Add this song into the new Spotify playlist

import json
import requests
from secrets import spotify_user_id, spotify_token


class CreatePlaylist:

    def __init__(self):
        pass

    # Step 1: Log into YouTube
    def get_youtube_client(self):
        pass

    # Step 2: Grab the liked videos
    def get_liked_videos(self):
        pass

    # Step 3: Create a new Playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name": "YouTube Liked Vids",
            "description": "All Liked YouTube Video",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{user_id}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application.json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        # Playlist id
        return response_json["id"]

    # Step 4: Search for the Song
    def get_spotify_url(self, song_name, artist):
        query = query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # Only use the first song
        uri = songs[0]["uri"]

    # Step 5: Add this song into the new Spotify playlist
    def add_song_to_playlist(self):
        pass
