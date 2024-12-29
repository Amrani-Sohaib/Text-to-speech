from  openai import OpenAI
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
#load_dotenv()

# Retrieve the API key from the .env file
#openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="""A colored manga illustration in the style of modern Berserk colorized chapters, featuring Guts sitting peacefully against a tree. The scene captures Miura's detailed art style but with rich colors - deep blues and purples in the sky blending into warm orange and gold sunset hues. The character maintains the sharp, detailed linework and proportions from the manga, while the environment shows those signature intricate details - the weathered tree bark, the precise ripples on the lake's surface, and the jagged mountain peaks in the background. The color palette should feel painterly yet maintain that distinct manga sharpness, with careful attention to light and shadow play across Guts' armor and the landscape. The peaceful atmosphere contrasts with the character's usual intensity, showing a rare moment of tranquility.""",
    size="1024x1024",
    quality="standard",
    n=1,
)

url = response.data[0].url 
# Download the image
response = requests.get(url)
if response.status_code == 200:
    # Save the image
    with open('generated_image.png', 'wb') as f:
        f.write(response.content)