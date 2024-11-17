from Spotify import getPlaylistData
from YouTube import searchYoutube
import os
import yt_dlp
from moviepy.editor import AudioFileClip
import eyed3


# Define Spotify ID and Secret here
spotify_id = ""
spotify_secret = ""

"""
Write metadata to each song file
"""
def writeMetadata(file_path, name, artists, album, genre):
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()
    audiofile.tag.title = name
    audiofile.tag.artist = artists
    audiofile.tag.album = album
    audiofile.tag.genre = genre
    audiofile.tag.save()


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
Download operation to be repeated for each playlist
"""
def downloadOperation(playlist):
    playlist_data = getPlaylistData(playlist, spotify_id, spotify_secret)
    print("[+] Starting download operations")
    for track in playlist_data:
        name, artists, album, genre = track
        songName = name + " " + artists
        url = searchYoutube(track)
        print(f"[+] Downloading: {name}")
        print(f"    Artists: {artists}")
        print(f"    Album: {album}")
        print(f"    Genre: {genre}")
        try:
            download_and_convert_to_mp3(url, songName)
            writeMetadata(f'audio/{songName}.mp3', name, artists, album, genre)
        except:
            print("Error occurred when downloading or renaming")


"""
Main function to repeat for each playlist
"""
def main():
    if not os.path.exists('audio'):
        print("[+] Setting up audio directory")
        os.makedirs('audio')
    print("[+] Directory setup complete")
    playlistArray = ["https://open.spotify.com/playlist/1xJkoLFPLKlOBkARzkpLQ5?si=10620a5aa24b436f"]  # Insert playlists here
    for i in playlistArray:
        downloadOperation(i)
    print("[+] Download operations complete")


if __name__ == '__main__':
    main()
