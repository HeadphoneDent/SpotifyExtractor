import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import json
from youtube_search import YoutubeSearch
import re
import yt_dlp
from moviepy.editor import AudioFileClip



BANNER = """
##############################################################################################
#                                                                                            #
#                   .d88888b                      dP   oo .8888b                             #             
#                   88.    "'                     88      88   "                             #             
#                   `Y88888b. 88d888b. .d8888b. d8888P dP 88aaa  dP    dP                    #             
#                         `8b 88'  `88 88'  `88   88   88 88     88    88                    #             
#                   d8'   .8P 88.  .88 88.  .88   88   88 88     88.  .88                    #             
#                    Y88888P  88Y888P' `88888P'   dP   dP dP     `8888P88                    #             
#                             88                                      .88                    #             
#                             dP                                  d8888P                     #             
#   888888ba                               dP                         dP                     #
#   88    `8b                              88                         88                     #
#   88     88 .d8888b. dP  dP  dP 88d888b. 88 .d8888b. .d8888b. .d888b88 .d8888b. 88d888b.   #
#   88     88 88'  `88 88  88  88 88'  `88 88 88'  `88 88'  `88 88'  `88 88ooood8 88'  `88   #
#   88    .8P 88.  .88 88.88b.88' 88    88 88 88.  .88 88.  .88 88.  .88 88.  ... 88         #
#   8888888P  `88888P' 8888P Y8P  dP    dP dP `88888P' `88888P8 `88888P8 `88888P' dP         #
#                                                                                            #
##############################################################################################                                                                                
"""


def directorySetup():
    if not os.path.exists('playlists'):
        print("[+] Setting up playlist directory")
        os.makedirs('playlists')
    if not os.path.exists('audio'):
        print("[+] Setting up audio directory")
        os.makedirs('audio')
    if not os.path.exists('video'):
        print("[+] Setting up video directory")
        os.makedirs('video')
    print("[+] Directory setup complete")


def getPlaylistCSV(playlistUrl):
    # Load credentials from .env file
    load_dotenv()

    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

    # Authenticate
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

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


def readSongsFromCSV(filename):
    songs = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Remove square brackets and blank lines
            row = [item.strip("[]") for item in row if item.strip()]
            row = [item for item in row if item]  # Remove any blank lines
            row = [item for item in row if item.strip()]  # Remove any blank objects
            songs.append(row)
    songs = [song for song in songs if song]  # Remove any empty objects
    return songs


def searchYoutube(song):
    print("[+] Searching YouTube for songs.\n[+] Note: This may take a while")
    urlArray = []
    for i in song:
        searchQuery = i[0] + " " + i[1]
        print("[+] Searching for >>", searchQuery)
        # Take first YouTube result from search
        results = YoutubeSearch(searchQuery, max_results=1).to_json()
        results_dict = json.loads(results)
        url = "https://youtube.com" + results_dict['videos'][0]['url_suffix']
        print("[+] URL found >> " + url)
        urlArray.append(url)
    return urlArray


def downloadSong(url):
    # improve to download directly as mp3
    os.system(f"yt-dlp_x86.exe {url} -o ./video/%(title)s.%(ext)s")


def download_and_convert_to_mp3(url, output_directory='./audio'):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Define yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',  # Select the best audio stream
        'outtmpl': f'{output_directory}/%(title)s.%(ext)s',  # Output file template
        'postprocessors': [],  # No post-processing during download
    }

    # Download the audio using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Process each file in the output directory
    for file in os.listdir(output_directory):
        file_path = os.path.join(output_directory, file)
        if file_path.endswith(('.webm', '.m4a')):  # Adjust for formats downloaded
            mp3_file_path = os.path.splitext(file_path)[0] + '.mp3'
            audio_clip = AudioFileClip(file_path)
            audio_clip.write_audiofile(mp3_file_path, codec='mp3')
            print(f"[+] Converted to MP3 with moviepy: {mp3_file_path}")
            audio_clip.close()  # Close the audio clip to free resources
            os.remove(file_path)  # Remove the original file if no longer needed


print(BANNER)
directorySetup()
playlist = str(input("Enter the playlist URL\nFormat: https://open.spotify.com/playlist/<playlist>?si=<sourceID>\n>> "))
playlistName = getPlaylistCSV(playlist)
songArray = readSongsFromCSV(playlistName)

print("[+] Starting download operations")
urlArray = searchYoutube(songArray)
for i in urlArray:
    download_and_convert_to_mp3(i)