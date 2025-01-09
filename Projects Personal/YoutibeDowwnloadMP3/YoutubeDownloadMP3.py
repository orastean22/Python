# ------------------------------------------------------------------------------------------------------------------
# -- Python Script File
# -- Created on 19/12/2024
# -- Author: AdrianO
# -- Version 0.1 - download youtube video to MP3
# -- Activate Virtual Envornment: source /Users/adrianorastean/Programming/Python/.venv/bin/activate
# -- Install pytube:  pip install pytube pydub
# -- Verify Installation: pip show pytube
# -- in case of not working upgrade the library: pip install --upgrade pytube
# -- install pydub: pip install pydub
# -- install FFmpeg: brew install ffmpeg
# ------------------------------------------------------------------------------------------------------------------

import os
import subprocess

def download_youtube_audio(url, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # yt-dlp command to download and convert to MP3
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", f"{output_folder}/%(title)s.%(ext)s",
        url
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Audio successfully downloaded to {output_folder}")
    except Exception as e:
        print(f"An error occurred: {e}")

# main 
if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")
    output_folder = os.path.expanduser("~/Desktop/Muzica Aniversare Ana 2024")
    download_youtube_audio(youtube_url, output_folder)
    
#END 08.01.2025