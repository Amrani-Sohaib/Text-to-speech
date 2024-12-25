import yt_dlp
import os
import json

# Function to download and convert YouTube video to WAV
def download_audio_as_wav(url, title, output_path):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # YouTube-DL options for WAV format
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': os.path.join(output_path, f'{title}.%(ext)s'),
        'verbose': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download and conversion completed successfully for: {title}")
    except Exception as e:
        print(f"An error occurred for {title} ({url}): {str(e)}")

# Function to process JSON file and download videos
def process_json(json_file, output_path):
    try:
        # Read JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            music_data = json.load(f)

        for item in music_data:
            title = item.get("title", "Untitled")
            link = item.get("link")
            if link:
                print(f"Processing: {title} - {link}")
                download_audio_as_wav(link, title, output_path)
            else:
                print(f"No link found for {title}")
    except FileNotFoundError:
        print(f"The JSON file {json_file} was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file {json_file}. Ensure it is formatted correctly.")
    except Exception as e:
        print(f"An error occurred while processing the JSON file: {e}")

# Example usage
if __name__ == "__main__":
    # Path to the JSON file containing music data
    json_file_path = r"C:\Users\Sohaib\ReopML\Text-to-speech\workflow_back_music\music.json"
    # Folder where you want the audio to be saved
    output_path = r"C:\Users\Sohaib\ReopML\Text-to-speech\workflow_back_music\audios"

    # Process the JSON file and download videos
    process_json(json_file_path, output_path)
