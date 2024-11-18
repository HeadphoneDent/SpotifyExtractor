# SpotifyExtractor

A Python script that downloads data from a Spotify playlist, retrieves the corresponding audio from YouTube, and converts them into MP3 files.

## Installation

1. **Get Spotify Credentials**:

    - Obtain a Client ID and Client Secret from a [Spotify Developer project](https://developer.spotify.com/dashboard).
    - Add these values into a `.env` file in the root directory of the project:

        ```bash
        CLIENT_ID="your_client_id"
        CLIENT_SECRET="your_client_secret"
        ```

2. **Install Dependencies**:

    - Ensure you have Python 3 and `pip` installed.

    - Install the required Python libraries by running:

        ```bash
        pip install -r requirements.txt
        ```

3. **Run the Script**:

    - Execute the script using Python:

        ```bash
        python3 SpotifyExtractor.py {urls}
        python3 SpotifyExtractor.py https://open.spotify.com/playlist/3VW1uoFR0DpUR5FFpn7XJh?si=68d3396328154f68 https://open.spotify.com/playlist/43g9WYiJsP8cyeNhU4ry89?si=0b1cca0ed59c4a3f
        ```

    - Alternatively, add the URLs of the Spotify playlists you want to download to `playlist_urls` list at the end of the `SpotifyExtractor.py` file.

## Features

-   **Automatic Directory Structuring**: Creates necessary directories for storing playlists, videos, and audio files.
-   **Automatic Processing**: Searches for each song on YouTube, downloads the video, and converts it to MP3.
-   **Metadata Extraction**: Retrieves metadata for each song, including the title, artist, and album.

## Roadmap

-   **Resume Functionality**: Add the ability to resume downloads if interrupted.
-   **Enhanced Error Handling**: Improve the script's robustness with better error handling.
-   **Code Improvements**: Refactor code for better readability and maintainability.
-   **Dependency Management**: Review and manage dependencies more effectively.
-   **Automatic Zipping/Packaging**: Add functionality to zip or package the downloaded files if hosted on a server.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request to help improve the project.
