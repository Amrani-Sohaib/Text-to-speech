import yt_dlp
import os
import json

def download_audio(url, output_path):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # YouTube-DL options
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
        print(f"Download completed successfully for: {url}")
    except Exception as e:
        print(f"An error occurred for {url}: {str(e)}")


# --- MAIN SCRIPT ---

# Path to your JSON file containing links
json_file_path = r"C:\Users\Sohaib\ReopML\Text-to-speech\links.json"

# Folder where you want the audio to be saved
output_path = r"C:\Users\Sohaib\ReopML\Text-to-speech\audios"

# Read the JSON file
with open(json_file_path, 'r') as f:
    data = json.load(f)

# If your JSON is structured as {"links": ["url1", "url2", ...]}
# iterate over the list of URLs
for url in data["links"]:
    download_audio(url, output_path)
