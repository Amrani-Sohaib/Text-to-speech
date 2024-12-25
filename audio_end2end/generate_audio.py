import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, Voice, VoiceSettings
from dotenv import load_dotenv
import pickle
import json

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API Key not found in environment variables!")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=api_key)



# deep ahmed Y99ruc9eEwTvDlDIWXFz ; ahmed fakhoury 7vV1oOAuJqnI0gCVx8qj ; ahmed deep test python wXwswnY4o9dwxVEULZPX
voice = client.voices.get(
    voice_id="7vV1oOAuJqnI0gCVx8qj",
)

# Define the audio generation process
try:
    # Load the cloned voice object
    #with open("cloned_voice.pkl", "rb") as file:
     #   voice = pickle.load(file)

    # Read text from JSON file
    with open(r"C:\Users\Sohaib\ReopML\Text-to-speech\Texts\texts.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        # Sort the data by timestamp and get the latest entry
        if isinstance(data, list):
            latest_entry = sorted(data, key=lambda x: x['timestamp'])[-1]
            text = latest_entry['content']
        else:
            text = data['content']  # Fallback for single entry JSON

    # Generate audio
    audio_generator = client.generate(text=text, voice=voice, model="eleven_turbo_v2_5",
                                      voice_settings=VoiceSettings(stability=0.65, similarity_boost=0.8))

    # Convert the generator to bytes
    audio_bytes = b"".join(audio_generator)

    # Play and save the audio
    output_dir = r"C:\Users\Sohaib\ReopML\Text-to-speech\workflow_audios"
    os.makedirs(output_dir, exist_ok=True)

    # Determine the next file number
    existing_files = [f for f in os.listdir(output_dir) if f.startswith(voice.name) and f.endswith('.wav')]
    next_file_number = len(existing_files) + 1

    # Construct the file name
    output_file_path = os.path.join(output_dir, f"{voice.name}_{next_file_number}.wav")

    # Save the audio
    with open(output_file_path, "wb") as file:
        file.write(audio_bytes)

    # Play the audio
    #play(audio_bytes)

    print(f"Audio saved to: {output_file_path}")

except Exception as e:
    print(f"An error occurred while generating audio: {e}")


