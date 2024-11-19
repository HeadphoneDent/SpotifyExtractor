import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

# Pulls the playlist songs and data from the Spotify API
def getPlaylistData(url, spotify_id, spotify_secret):
    print("[+] Creating Spotify session")
    # Authenticate and create session object
    client_credentials_manager = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret)
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get uri from https link
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", url):
        print("[+] Valid URL format")
        playlist_uri = match.groups()[0]
    else:
        print("[-] Invalid URL format")
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")

    # Get list of tracks in a given playlist (note: max playlist length 100)
    print("[+] Pulling playlist data from Spotify API")
    tracks = session.playlist_tracks(playlist_uri)["items"]
    playlistName = session.playlist(playlist_uri)["name"]

    # Store data in memory
    playlist_data = []
    for track in tracks:
        name = track["track"]["name"]
        artists = ", ".join([artist["name"] for artist in track["track"]["artists"]])
        album = track["track"]["album"]["name"]
        genres = session.artist(track["track"]["artists"][0]["id"])["genres"]
        genre = genres[0] if genres else "Unknown"
        playlist_data.append([name, artists, album, genre])

    print("[+] Pulled data from " + playlistName + " playlist")
    return playlist_data