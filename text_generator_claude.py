import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json
import datetime

# Load environment variables from a .env file (if applicable)
load_dotenv()

# Load the OpenAI API key from environment variables
api_key = os.getenv("CLAUDE_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables.")


# Confirm that the OpenAI client is set up
print("Anthropic client initialized.")

# Define the file path for saving the response
text_file_path = r"C:\Users\Sohaib\ReopML\Text-to-speech\Texts\texts.txt"


# Create a chat completion
try:
    # Initialize the Anthropic client
    client = Anthropic( 

        api_key=api_key
        
    )
    
    # Read prompt from JSON file
    with open(r"C:\Users\Sohaib\ReopML\Text-to-speech\prompt.json", 'r', encoding='utf-8') as f:
        prompt_data_list = json.load(f)

    # Extract the first item's prompt
    prompt_text = prompt_data_list[2]["prompt_guts"]

    # Define the model
    model_name = "claude-3-5-sonnet-20241022"  # You can make this configurable too

    # Create message with system prompt and user content
    response = client.messages.create(
        model=model_name,
        max_tokens=1024,
        temperature=0.0,
        system="""You are an arabic world-class author with a heavy background in manga and philosophy 
                  and you shine at making philosophical analysis of great works (manga, anime, cinema, books..).
                  Be formal and use a poetic tone.""",
        messages=[
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    )


    # Extract the content of the response
    response_content = response.content[0].text
    print("Claude's answer")

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
        "model": response.model,  # This will now get the model from the response
        "prompt": prompt_text,
        "content": response_content
    })
    
    # Save updated JSON data
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Response saved to: {json_file_path}")

except Exception as e:
    print("Error:", str(e))






