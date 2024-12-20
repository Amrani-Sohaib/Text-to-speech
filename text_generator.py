import os
from openai import OpenAI as openai
from dotenv import load_dotenv

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
            "content": "je veux que tu me parle de naruto et la philosophie du nihilism et exisctantialism dans ce manga en arabe avec la manière de Ahmed fakhoury"
        }
    ]

    # Call the OpenAI API for a chat completion
    response = client.chat.completions.create(
        model="gpt-4o",  # Use a valid model name
        messages=messages
    )

    # Extract the content of the response
    response_content = response.choices[0].message.content
    print("Chat completion response:", response_content)

    # Save the response to a text file
    os.makedirs(os.path.dirname(text_file_path), exist_ok=True)  # Ensure the directory exists
    with open(text_file_path, "a", encoding="utf-8") as text_file:
        text_file.write(response_content + "\n")  # Append the response with a newline

    print(f"Response saved to: {text_file_path}")

except Exception as e:
    # Handle errors during the API call
    print("Error creating chat completion:", str(e))
