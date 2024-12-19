import os
from pydub import AudioSegment

# Input directory containing the audio files
input_dir = r"C:\Users\Sohaib\ReopML\Text-to-speech\audios"
output_dir = os.path.join(input_dir, "segments")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Length of each segment in milliseconds
segment_length = 40 * 1000  # 40 seconds

# Iterate over all files in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".mp3"):
        file_path = os.path.join(input_dir, file_name)
        
        # Load the audio file
        audio = AudioSegment.from_file(file_path)
        
        # Calculate number of segments
        total_length = len(audio)
        num_segments = (total_length + segment_length - 1) // segment_length

        for i in range(num_segments):
            start_time = i * segment_length
            end_time = min(start_time + segment_length, total_length)

            # Extract segment
            segment = audio[start_time:end_time]

            # Save segment to output directory
            segment_file_name = f"{os.path.splitext(file_name)[0]}_part{i + 1}.mp3"
            segment_file_path = os.path.join(output_dir, segment_file_name)
            segment.export(segment_file_path, format="mp3")

print(f"Audio splitting complete. Files saved in: {output_dir}")