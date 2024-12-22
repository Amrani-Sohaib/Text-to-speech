import os 
from ollama import chat 
from ollama import ChatResponse
from dotenv import load_dotenv 
import json
import datetime


# Load environment variables from a .env file (if applicable)
load_dotenv()

try:

    try:
        with open('prompt.json', 'r', encoding='utf-8') as f:
            prompt_data = json.load(f)

        # Ensure the JSON is a list of dictionaries and contains a 'prompt' key
        if isinstance(prompt_data, list) and len(prompt_data) > 0:
            # Retrieve the 'prompt' string from the first dictionary in the list
            if 'prompt' in prompt_data[0]:
                prompt_content = prompt_data[0]['prompt']
            else:
                raise KeyError("The first dictionary in the list does not contain the 'prompt' key.")
        else:
            raise ValueError("The JSON file does not contain a list of dictionaries.")

        print("Prompt content successfully retrieved:")

    except FileNotFoundError:
        print("Error: prompt.json file not found.")
        raise
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in prompt.json.")
        raise
    except KeyError as e:
        print(f"Error: {e}")
        raise
    except ValueError as e:
        print(f"Error: {e}")
        raise


    response: ChatResponse = chat(
        model='mistral-nemo', 
        messages=[{
            'role': 'user',
            'content': prompt_content,
        }]
    )
    response_content = response['message']['content'] 
    # or access fields directly from the response object
    print("answer generated")

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
