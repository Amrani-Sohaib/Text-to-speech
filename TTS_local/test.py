import torch
from TTS.api import TTS


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

content = """  يمثل إيرين ييغر شخصية معقدة في علاقتها بالفلسفة العدمية. فبعد اكتشافه للحقيقة المريرة حول عالمه والتاريخ المأساوي لشعبه، يتحول تفكيره تدريجياً نحو رؤية عدمية للوجود. يرى أن المعاناة والصراع هما جوهر الحياة، وأن البحث عن معنى أو قيم مطلقة هو وهم. هذا التحول الفلسفي يدفعه لاتخاذ قرارات متطرفة، معتقداً أن الحرية الحقيقية تكمن في القدرة على تدمير العالم وإعادة تشكيله، حتى لو كان ذلك يعني التخلي عن إنسانيته وقيمه السابقة."""

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
#wav = tts.tts(text=content, speaker_wav="C:\Users\Sohaib\ReopML\Text-to-speech\generated_audios\Ahmed deep test python_1.wav", language="ara")
# Text to speech to a file
tts.tts_to_file(text=content, speaker_wav=r"C:\Users\Sohaib\ReopML\Text-to-speech\audios\full_audios\الأسد والخروف وكلمات المتنبي.wav", language="ar", file_path="output.wav")