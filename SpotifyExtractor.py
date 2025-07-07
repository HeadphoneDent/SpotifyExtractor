#     # Get list of tracks in a given playlist (note: max playlist length 100)
#     print("[+] Pulling playlist data from Spotify API")
#     tracks = session.playlist_tracks(playlist_uri)["items"]
#     playlistName = session.playlist(playlist_uri)["name"]

#     # Store data in memory
#     playlist_data = []
#     for track in tracks:
#         name = track["track"]["name"]
#         artists = ", ".join([artist["name"] for artist in track["track"]["artists"]])
#         album = track["track"]["album"]["name"]
#         genres = session.artist(track["track"]["artists"][0]["id"])["genres"]
#         genre = genres[0] if genres else "Unknown"
#         playlist_data.append([name, artists, album, genre])

#     print("[+] Pulled data from " + playlistName + " playlist")
#     return playlist_data


import requests
import base64
import re

url = [
    "insert playlist link here"
]
client_id = "insert client id here"
client_secret = "insert client secret here"

# Check URL's for the playlist regex
def validateUrls():
    for link in url:
        if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", link):
            print("[+] Correct format of URL: ", link)
            playlist_uri = match.groups()[0]
        else:
            print("[-] Invalid URL format of: ", link)
            print("[-] Ensure only playlist links are provided...")
            exit(1)

# Use the provided client_id and client_secret to request an access token
def getAccessToken():
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {"Authorization": f"Basic {b64_auth_str}"}
    data = {"grant_type": "client_credentials"}

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    if response.status_code == 200:
        print("Acces Token: ", response.json().get("access_token"))
        print("Token Type: ", response.json().get("token_type"))
        print("Expires In: ", response.json().get("expires_in"))
    else:
        print("Failed to get token:", response.status_code, response.text)


if __name__ == "__main__":
    validateUrls()
