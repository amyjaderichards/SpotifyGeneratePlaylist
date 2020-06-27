#Step 1: Log into YouTube
#Step 2: Grab the liked videos
#Step 3: Create a New Playlist
#Step 4: Search for the Song
#Step 5: Add this song into the new Spotify playlist

import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from exceptions import ResponseException
from secrets import spotify_user_id, spotify_token


class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    # Step 1: Log into YouTube
    def get_youtube_client(self):
        """ Log into YouTube, copied from the YouTube Data API """
        # Disable OAuthlib's HTTPS verification when running locally,
        # DO NOT leave this option enables in production
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client.secret.json"

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # From the YouTube Data API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    # Step 2: Grab the liked videos
    def get_liked_videos(self):
        """ Grab our liked videos and create a dictionary of important song information """
        request = self.get_youtube_client().list(
            part="snipper, contentDetails, statistics",
            myRating="like"
        )
        response = request.execute()

        # Collect each video and get important information
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"]
            )

            # Use youtube_dl to collect the song name and artist name
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)
            song_name = video["track"]
            artist = video["artist"]

            if song_name is not None and artist is not None:
                # Save all important info and skip any missing song and artist
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,

                    # Add the url, easy to get song to put into playlist
                    "spotify-url": self.get_spotify_url(song_name, artist)
                }

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
