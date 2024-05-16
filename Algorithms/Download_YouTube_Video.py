#download youtube video using python scrypt
# need to open terminal and install this:    pip install yt-dlp

import yt_dlp

# Specify the output directory where the video will be saved
output_directory = '/Users/adrianorastean/Downloads/VIDEOCLIPS/'

# Prompt the user for the video URL
url = input("Enter video URL: ")

# Set the options for youtube-dl
ydl_opts = {
    'outtmpl': output_directory + '%(title)s.%(ext)s'  # Set the output template
}

# Download the video to the specified location
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])  # Pass the URL as a list to download a single video

print("Video downloaded successfully to:", output_directory)

