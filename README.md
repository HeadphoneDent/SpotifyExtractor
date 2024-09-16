# SpotifyDownloader

A Python script that downloads songs from a Spotify playlist, retrieves the corresponding videos from YouTube, and converts them into MP3 files.

## Installation

1. **Get Spotify Credentials**:

    - Obtain a Client ID and Client Secret from a [Spotify Developer project](https://developer.spotify.com/dashboard).
    - Create a `.env` file in the project directory with the following format:

        ```ini
        CLIENT_ID='YOUR_CLIENT_ID'
        CLIENT_SECRET='YOUR_CLIENT_SECRET'
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
        python3 SpotifyDownloader.py
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
