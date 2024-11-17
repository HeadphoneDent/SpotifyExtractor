"""
Method for obtaining info from a Spotify playlist, including each song's name, artist, album, and genre.
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import csv

def getPlaylistCSV(playlistUrl):
    spotify_id = "" # Your Spotify ID
    spotify_secret = "" # Your Spotify Secret

    # Authenticate
    client_credentials_manager = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret)

    # Create spotify session object
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get uri from https link
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", playlistUrl):
        print("[+] Valid URL format")
        playlist_uri = match.groups()[0]
    else:
        print("[-] Invalid URL format")
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")

    # Get list of tracks in a given playlist (note: max playlist length 100)
    tracks = session.playlist_tracks(playlist_uri)["items"]

    playlistName = session.playlist(playlist_uri)["name"]

    # Create csv file
    with open(("./playlists/" + playlistName + ".csv"), "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Extract name and artist
        for track in tracks:
            name = track["track"]["name"]
            artists = ", ".join(
                [artist["name"] for artist in track["track"]["artists"]]
            )
            # Write to csv
            writer.writerow([name, artists])
    print("[+] Pulled CSV from " + playlistName + " playlist")
    playlistName = "./playlists/" + playlistName + ".csv"
    return playlistName