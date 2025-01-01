from  openai import OpenAI
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment variables from .env file
#load_dotenv()

# Retrieve the API key from the .env file
#openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt=""""A serene beach scene at sunrise with a lone warrior sitting on a large piece of driftwood. The warrior wears a flowing traditional blue kimono, their long hair blowing gently in the breeze. They hold a pair of crutches in their hands, symbolizing resilience and reflection. The sky is vibrant with dramatic, colorful clouds illuminated by the sun, and birds are flying across the horizon. The ocean waves gently lap at the shore, adding to the tranquil and contemplative atmosphere.""",
    size="1024x1024",
    quality="standard",
    n=1,
)

url = response.data[0].url 
# Download the image
response = requests.get(url)
if response.status_code == 200:
    # Save the image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'generated_image_{timestamp}.png', 'wb') as f:
        f.write(response.content)