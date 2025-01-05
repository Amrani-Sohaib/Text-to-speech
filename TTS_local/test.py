import torch
from TTS.api import TTS
import os
import subprocess


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
# List available TTS 

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False) 
#tts = TTS("tts_models/en/ljspeech/glow-tts", progress_bar=False) 
tts = tts.to(device)

content = "  يمثل إيرين ييغر شخصية معقدة في علاقتها بالفلسفة العدمية. فبعد اكتشافه للحقيقة المريرة حول عالمه والتاريخ المأساوي لشعبه، يتحول تفكيره تدريجياً نحو رؤية عدمية للوجود. يرى أن المعاناة والصراع هما جوهر الحياة، وأن البحث عن معنى أو قيم مطلقة هو وهم. هذا التحول الفلسفي يدفعه لاتخاذ قرارات متطرفة، معتقداً أن الحرية الحقيقية تكمن في القدرة على تدمير العالم وإعادة تشكيله، حتى لو كان ذلك يعني التخلي عن إنسانيته وقيمه السابقة."

content_fr = "bonjour je suis amrani sohaib et je suis un étudiant en informatique à l'université de constantine 2, je suis passionné par l'intelligence artificielle et le machine learning. j'ai réalisé plusieurs projets en utilisant ces technologies. je suis très content de travailler avec vous et j'espère que je vais apprendre beaucoup de choses avec vous merci"
content_eng = 'hello my name is sohaib amrani and i am a computer science student at the university of constantine 2, i am passionate about artificial intelligence and machine learning. i have completed several projects using these technologies. i am very happy to work with you and i hope that i will learn a lot of things with you, thank you'
# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output


waves_path = r"C:\Users\Sohaib-\RepoML\Text-to-speech\audios\converted_wavs"
# List all .wav files in the converted directory
speaker_wavs = [os.path.join(waves_path, file) for file in os.listdir(waves_path) if file.endswith(".wav")]
#print(f"Speaker .wav files: {speaker_wavs}")





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

tts.tts_to_file(text=content_eng, 
                file_path="output.wav",
                speaker_wav=speaker_wavs,
                language="en" 
                )
