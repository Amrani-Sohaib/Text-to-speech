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
    prompt="""A colored image featuring Guts sitting peacefully on a rock infront of a lac in a landscape similar to the swiss alpes. 
              The scene captures deep blues and purples in the sky blending into warm orange and gold sunset hues. 
              while the environment shows those signature intricate details - the weathered tree bark, 
              the precise ripples on the lake's surface, and the jagged mountain peaks in the background. 
              The color palette should feel painterly yet maintain that distinct manga sharpness, 
              with careful attention to light and shadow play across Guts' armor and the landscape. 
              The peaceful atmosphere contrasts with the character's usual intensity, showing a rare moment of tranquility.
              The scene is from a long distance capturing both the character and the environment.""",
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