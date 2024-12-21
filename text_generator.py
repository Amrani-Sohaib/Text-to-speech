import os
from openai import OpenAI as openai
from dotenv import load_dotenv
import json
import datetime

# Load environment variables from a .env file (if applicable)
load_dotenv()

# Load the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
client = openai()

# Confirm that the OpenAI client is set up
print("OpenAI client initialized.")

# Define the file path for saving the response
text_file_path = r"C:\Users\Sohaib\ReopML\Text-to-speech\Texts\texts.txt"

# Create a chat completion
try:
    # Define the chat messages
    messages = [
        {
            "role": "user",
            "content": """
                        
                        """
        }
    ]

    # Call the OpenAI API for a chat completion
    response = client.chat.completions.create(
        model="chatgpt-4o-latest",  # Use a valid model name
        messages=messages
    )

    # Extract the content of the response
    response_content = response.choices[0].message.content
    print("Gpt answer")

    # Save the response to a JSON file
    json_file_path = r"C:\Users\Sohaib\ReopML\Text-to-speech\Texts\texts.json"
    
    # Create or load existing JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    # Add new response as a dictionary
    data.append({
        "timestamp": str(datetime.datetime.now()),
        "content": response_content
    })
    
    # Save updated JSON data
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Response saved to: {json_file_path}")

except Exception as e:
    # Handle errors during the API call
    print("Error creating chat completion:", str(e))
