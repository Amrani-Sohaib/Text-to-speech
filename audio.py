import yt_dlp
import os

def download_audio(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'verbose': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Usage
url = "https://www.youtube.com/watch?v=-hzIwlIPYAU"

output_path = "C:/Users/Sohaib/ReopML/ML-Models/audios"

download_audio(url, output_path)