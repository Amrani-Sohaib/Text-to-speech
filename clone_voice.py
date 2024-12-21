import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import pickle

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API Key not found in environment variables!")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=api_key)

# Define the voice cloning process
try:
    # Clone the voice
    voice = client.clone(
        name="Ahmed deep test python",
        description="Ahmed Fakhouri's voice is rich, mid-to-deep, and well-balanced, combining authority with warmth. His clear enunciation, polished Syrian accent, and deliberate pacing make his delivery engaging and universally understandable. He skillfully modulates tone to convey urgency or softness, maintaining professionalism while connecting with the audience.",
        files=[os.path.join("C:/Users/Sohaib/ReopML/Text-to-speech/audios/segments", f) for f in os.listdir("C:/Users/Sohaib/ReopML/Text-to-speech/audios/segments") if f.endswith('.mp3')]
    )

    # Save the cloned voice object to a file
    with open("cloned_voice.pkl", "wb") as file:
        pickle.dump(voice, file)

    print("Voice cloned and saved successfully.")

except Exception as e:
    print(f"An error occurred while cloning the voice: {e}")
