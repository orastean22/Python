#download youtube video using python scrypt on Highest resolution
#install : pip install pytube; pip install yt-dlp; pip install -U yt-dlp; 

import yt_dlp

def download_video(url, output_path):
    try:
        # Set options for downloading the highest resolution video
        options = {
            'format': 'bestvideo[height<=?1080][fps<=?30]+bestaudio/best[height<=?1080][fps<=?30]',
            'outtmpl': output_path + '/%(title)s.%(ext)s',
            'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',  # Modify this path as needed
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
                            }
        }
        # Create a YoutubeDL object with options
        ydl = yt_dlp.YoutubeDL(options)

        # Download the video
        with ydl:
            result = ydl.extract_info(url, download=True)
        print("Download complete.")
    
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Ask the user to input the YouTube URL and output path
    url = input("Enter the YouTube URL: ")
    # output_path = '/Users/adrianorastean/Desktop/VIDEOCLIPS/'
    # output_path = '/Users/adrianorastean/Desktop/Trading Time/'
    output_path = '/Users/adrianorastean/Desktop/AUDIOBooks/'
    download_video(url, output_path)




