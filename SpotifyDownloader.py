from PlaylistInfo import *

import os
import csv
import json
from youtube_search import YoutubeSearch
import yt_dlp
from moviepy.editor import AudioFileClip


"""
Set up 'playlist' and 'audio' directories
"""
def directorySetup():
    if not os.path.exists('playlists'):
        print("[+] Setting up playlist directory")
        os.makedirs('playlists')
    if not os.path.exists('audio'):
        print("[+] Setting up audio directory")
        os.makedirs('audio')
    print("[+] Directory setup complete")


"""
Create an array of songs and the artist/s
"""
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

"""
Search Youtube for the first result
"""
def searchYoutube(song):
    print("[+] Searching YouTube for songs.\n[+] Note: This may take a while")
    searchQuery = song[0] + " " + song[1]
    print("[+] Searching for >>", searchQuery)
    results = YoutubeSearch(searchQuery, max_results=1).to_json()
    results_dict = json.loads(results)
    url = "https://youtube.com" + results_dict['videos'][0]['url_suffix']
    print("[+] URL found >> " + url)
    return url

"""
Download and convert existing song format to an mp3 
"""
def download_and_convert_to_mp3(url, songName, output_directory='./audio'):
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
        info_dict = ydl.extract_info(url, download=True)
        song_title = info_dict.get('title', None)
        print(f"[+] Downloaded: {song_title}")
    
    # Process each file in the output directory
    for file in os.listdir(output_directory):
        file_path = os.path.join(output_directory, file)
        if file_path.endswith(('.webm', '.m4a')):  # Adjust for formats downloaded
            mp3_file_path = os.path.join(output_directory, songName + '.mp3')
            audio_clip = AudioFileClip(file_path)
            audio_clip.write_audiofile(mp3_file_path, codec='mp3')
            print(f"[+] Converted to MP3 with moviepy: {mp3_file_path}")
            audio_clip.close()  # Close the audio clip to free resources
            os.remove(file_path)  # Remove the original file if no longer needed

"""
Main operation to be repeated for each playlist
"""
def downloadOperation(playlist):
    # playlist = str(input("Enter the playlist URL\nFormat: https://open.spotify.com/playlist/<playlist>?si=<sourceID>\n>> "))
    playlist = playlist
    playlistName = getPlaylistCSV(playlist)
    songArray = readSongsFromCSV(playlistName)
    print("[+] Starting download operations")
    for i in songArray:
        songName = i[0] + " " + i[1]
        url = searchYoutube(i)
        try:
            download_and_convert_to_mp3(url, songName)
        except:
            print("Error occoured when downloading or renaming")

"""
Main function to repeat for each playlist
"""
directorySetup()
playlistArray = ["https://open.spotify.com/playlist/1xJkoLFPLKlOBkARzkpLQ5?si=10620a5aa24b436f"] # Insert playlists here
for i in playlistArray:
    downloadOperation(i)
