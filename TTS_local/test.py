import torch
from TTS.api import TTS
import os
import subprocess


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

# List available TTS models

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

content = "  يمثل إيرين ييغر شخصية معقدة في علاقتها بالفلسفة العدمية. فبعد اكتشافه للحقيقة المريرة حول عالمه والتاريخ المأساوي لشعبه، يتحول تفكيره تدريجياً نحو رؤية عدمية للوجود. يرى أن المعاناة والصراع هما جوهر الحياة، وأن البحث عن معنى أو قيم مطلقة هو وهم. هذا التحول الفلسفي يدفعه لاتخاذ قرارات متطرفة، معتقداً أن الحرية الحقيقية تكمن في القدرة على تدمير العالم وإعادة تشكيله، حتى لو كان ذلك يعني التخلي عن إنسانيته وقيمه السابقة."

content_fr = "bonjour je suis amrani sohaib et je suis un étudiant en informatique à l'université de constantine 2, je suis passionné par l'intelligence artificielle et le machine learning, j'ai réalisé plusieurs projets en utilisant ces technologies, je suis très content de travailler avec vous et j'espère que je vais apprendre beaucoup de choses avec vous, merci."
# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
"""



"""
# Directory containing .mp3 files
segments_dir = r"C:\Users\Sohaib\ReopML\Text-to-speech\audios\segments"

# Directory to save converted .wav files
output_dir = os.path.join(segments_dir, "converted_wavs")
os.makedirs(output_dir, exist_ok=True)

# Function to convert .mp3 to .wav using ffmpeg
def convert_mp3_to_wav(mp3_path, wav_path):
    try:
        # Run ffmpeg command
        subprocess.run(
            ["ffmpeg", "-i", mp3_path, wav_path, "-y"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Converted {mp3_path} to {wav_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {mp3_path}: {e.stderr.decode()}")

# Convert all .mp3 files in the directory
for file in os.listdir(segments_dir):
    if file.endswith(".mp3"):
        mp3_path = os.path.join(segments_dir, file)
        wav_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".wav")
        convert_mp3_to_wav(mp3_path, wav_path)

# List all .wav files in the converted directory
speaker_wavs = [os.path.join(output_dir, file) for file in os.listdir(output_dir) if file.endswith(".wav")]
print(f"Speaker .wav files: {speaker_wavs}")




# List all .wav files in the directory
#speaker_wavs = [os.path.join(segments_dir, file) for file in os.listdir(segments_dir) if file.endswith(".wav")]
"""
# Text to speech to a list of amplitude values
wav = tts.tts(text=content, 
              speaker_wavs = speaker_wavs, 
              language="ar",
              file_path="output.wav",
              )
"""


tts.tts_to_file(text=content_fr, 
                file_path="output.wav",
                speaker_wav=speaker_wavs, 
                language="fr" )
