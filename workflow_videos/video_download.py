import yt_dlp
import os

def download_video(video_url, save_path="downloads"):
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        # Set up options for yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save with video title
            'format': 'bestvideo+bestaudio/best',  # Download best quality
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    save_path = input("Enter the save directory (default: 'downloads'): ") or "downloads"
    download_video(video_url, save_path)
