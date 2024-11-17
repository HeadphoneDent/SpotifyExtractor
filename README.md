# SpotifyExtractor

A Python script that downloads data from a Spotify playlist, retrieves the corresponding audio from YouTube, and converts them into MP3 files.

## Installation

1. **Get Spotify Credentials**:

    - Obtain a Client ID and Client Secret from a [Spotify Developer project](https://developer.spotify.com/dashboard).
    - Add these values into the SpotifyExtractor.py file:

[//]: # (2. **Install Dependencies**:)

[//]: # ()
[//]: # (    - Ensure you have Python 3 and `pip` installed.)

[//]: # (    - Install the required Python libraries by running:)

[//]: # ()
[//]: # (        ```bash)

[//]: # (        pip install -r requirements.txt)

[//]: # (        ```)

2. **Add playlist URLs**:

    - Add the URLs of the Spotify playlists you want to download to the `playlist_urls` list in the `SpotifyExtractor.py` file.

4. **Run the Script**:

    - Execute the script using Python:

        ```bash
        python3 SpotifyExtractor.py
        ```

    - Note: Currently, the script does not accept command-line arguments and is designed to be run as-is.

## Features

-   **Automatic Directory Structuring**: Creates necessary directories for storing playlists, videos, and audio files.
-   **Automatic Processing**: Searches for each song on YouTube, downloads the video, and converts it to MP3.

## Roadmap

-   **URL Array Saving**: Save processed playlist URLs for resuming or tracking.
-   **Resume Functionality**: Add the ability to resume downloads if interrupted.
-   **Enhanced Error Handling**: Improve the script's robustness with better error handling.
-   **Code Improvements**: Refactor code for better readability and maintainability.
-   **Dependency Management**: Review and manage dependencies more effectively.
-   **Automatic Zipping/Packaging**: Add functionality to zip or package the downloaded files.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to help improve the project.
