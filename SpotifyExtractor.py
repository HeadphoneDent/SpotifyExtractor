from PlaylistData import getPlaylistData
from YouTube import searchYoutube
import os
import yt_dlp
from moviepy.editor import AudioFileClip
import eyed3
import sys
from dotenv import load_dotenv


# Load Spotify ID and SECRET
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# Get playlists from command line input
playlistCount = len(sys.argv) - 1
playlistArray = []
for i in range(1, playlistCount + 1):
    playlistArray.append(sys.argv[i])


# Write metadata to each song file
def writeMetadata(file_path, name, artists, album, genre):
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()
    audiofile.tag.title = name
    audiofile.tag.artist = artists
    audiofile.tag.album = album
    audiofile.tag.genre = genre
    audiofile.tag.save()


# Download and convert existing song format to mp3
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
            print("[+] Converted to MP3 with moviepy: " + mp3_file_path)
            audio_clip.close()  # Close the audio clip to free resources
            os.remove(file_path)  # Remove the original file if no longer needed


def setup():
    # Directory setup
    if not os.path.exists('audio'):
        print("[+] Setting up audio directory")
        os.makedirs('audio')
        print("[+] Created audio directory")
    else:
        print("[+] Using existing directory setup")

    # playlistArray = []
    if (len(playlistArray) == 0):
        print("[-] ERROR: No playlists given")
        print("[-] Usage: python SpotifyExtractor.py {url}")
        quit(1)


def main():
    for j in playlistArray:
        playlist_data = getPlaylistData(j, client_id, client_secret)
        print("[+] Starting download operations")
        for track in playlist_data:
            name, artists, album, genre = track
            print(f"[+] Track details - Name: {name}, Artists: {artists}, Album: {album}, Genre: {genre}")
            currentfile = f'audio/{name}.mp3'
            if os.path.exists(currentfile):
                audiofile = eyed3.load(currentfile)
                if audiofile.tag.artist == artists:
                    print(f"[+] {name} already exists in audio directory")
                    continue
                url = searchYoutube(name + " " + artists + " lyric video")
                try:
                    download_and_convert_to_mp3(url, name)
                    writeMetadata(f'audio/{name}.mp3', name, artists, album, genre)
                except:
                    print("[-] Error occurred when downloading or renaming")
            else:
                url = searchYoutube(name + " " + artists + " lyric video")
                try:
                    download_and_convert_to_mp3(url, name)
                    writeMetadata(f'audio/{name}.mp3', name, artists, album, genre)
                except:
                    print("[-] Error occurred when downloading or renaming")
    print("[+] Download operations complete")


if __name__ == '__main__':
    setup()
    main()
