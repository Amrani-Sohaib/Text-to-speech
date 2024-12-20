import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API Key not found in environment variables!")


client = ElevenLabs(
  api_key=api_key, # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)



try:
    # Clone the voice
    client = ElevenLabs(api_key=api_key)
    voice = client.clone(
        name="Ahmed deep voice",
        description="Ahmed Fakhouri's voice is rich, mid-to-deep, and well-balanced, combining authority with warmth. His clear enunciation, polished Syrian accent, and deliberate pacing make his delivery engaging and universally understandable. He skillfully modulates tone to convey urgency or softness, maintaining professionalism while connecting with the audience.",
        files=[os.path.join("C:/Users/Sohaib/ReopML/Text-to-speech/audios/segments", f) for f in os.listdir("C:/Users/Sohaib/ReopML/Text-to-speech/audios/segments") if f.endswith('.mp3')]
    )

    # Generate audio
    audio_generator = client.generate(text="يمثل إيرين ييغر شخصية معقدة في علاقتها بالفلسفة العدمية. فبعد اكتشافه للحقيقة المريرة حول عالمه والتاريخ المأساوي لشعبه، يتحول تفكيره تدريجياً نحو رؤية عدمية للوجود. يرى أن المعاناة والصراع هما جوهر الحياة، وأن البحث عن معنى أو قيم مطلقة هو وهم. هذا التحول الفلسفي يدفعه لاتخاذ قرارات متطرفة، معتقداً أن الحرية الحقيقية تكمن في القدرة على تدمير العالم وإعادة تشكيله، حتى لو كان ذلك يعني التخلي عن إنسانيته وقيمه السابقة.", voice=voice)

    # Convert the generator to bytes
    audio_bytes = b"".join(audio_generator)

    # Play and save the audio
    output_dir = r"C:\Users\Sohaib\ReopML\Text-to-speech\generated_audios"
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
    play(audio_bytes)

except Exception as e:
    print(f"An error occurred: {e}")
