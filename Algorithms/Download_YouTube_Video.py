#download youtube video using python scrypt
# need to open terminal and install this:    pip install yt-dlp

import yt_dlp
url = input("Enter video url: ")
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Video download successfully!")
