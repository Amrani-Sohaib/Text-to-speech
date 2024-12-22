import os
from ollama import chat
from ollama import ChatResponse
import ollama  # <-- Instead of 'from ollama import chat, list', import the whole module

import json
import datetime

# File path to save the conversation history
json_file_path = r"C:\Users\Sohaib\ReopML\Text-to-speech\LLM_local_test\Logs.json"

def save_response(prompt, response):
    """Save the prompt and response to a JSON file."""
    try:
        # Create or load existing JSON data
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Add new conversation entry
        data.append({
            "timestamp": str(datetime.datetime.now()),
            "prompt": prompt,
            "response": response
        })

        # Save updated JSON data
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Conversation saved to: {json_file_path}")
    except Exception as e:
        print(f"Error saving conversation: {e}")

def choose_model():
    """Fetch and display available models from ollama, allow the user to choose one."""
    print("Fetching available models...\n")

    try:
        # 1) Get the ListResponse from ollama
        response = ollama.list()
        
        # 2) Extract the actual list of Model objects
        models = response.models  # <-- important

        if not models:
            print("No models found.")
            return None

        # 3) Display the available models
        print("Available Models:")
        for idx, model_obj in enumerate(models, start=1):
            # model_obj is an instance of ollama._types.Model
            # .model is its string name, e.g. 'mistral:latest'
            print(f"{idx}. {model_obj.model}")

        # 4) Let the user choose a model
        while True:
            try:
                choice = int(input("\nEnter the number of the model you want to use: "))
                if 1 <= choice <= len(models):
                    chosen_model = models[choice - 1]
                    print(f"You have chosen model: {chosen_model.model}")
                    return chosen_model
                else:
                    print("Invalid choice. Please choose a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    except Exception as e:
        print(f"Error fetching models: {e}")
        return None


def main():
    print("Real-Time Chat with Model (type 'exit' to quit)\n")


    # Let the user choose a model
    model_name = choose_model()
    if not model_name:
        print("No valid model selected. Exiting...")
        return

    print(f"\nYou selected the model: {model_name}\n")

    try:
        while True:
            # Get user input
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting the chat. Goodbye!")
                break

            # Send the prompt to the model
            try:
                response: ChatResponse = chat(
                    model='mixtral',
                    messages=[{
                        'role': 'user',
                        'content': user_input,
                    }]
                )
                # Extract the response content
                response_content = response['message']['content']
                print(f"Model: {response_content}")

                # Save both prompt and response
                save_response(user_input, response_content)

            except Exception as e:
                print(f"Error generating response: {e}")

    except KeyboardInterrupt:
        print("\nChat interrupted. Goodbye!")

if __name__ == "__main__":
    main()
