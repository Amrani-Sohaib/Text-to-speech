import json

def process_json_file(input_file, output_file):
    """
    Process a JSON file to extract 'title' and 'processed_text' fields and save to a new JSON file.
    
    Args:
        input_file (str): Path to input JSON file
        output_file (str): Path to output JSON file
    """
    try:
        # Read the JSON file
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Create new list with only required fields
        processed_data = []
        for item in data:
            processed_item = {
                'title': item['title'],
                'processed_text': item['processed_text']
            }
            processed_data.append(processed_item)
        
        # Write to new JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)
            
        print(f"Successfully processed {len(processed_data)} items")
        print(f"Output saved to {output_file}")
            
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in input file")
    except KeyError as e:
        print(f"Error: Missing required field {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "processed_transcripts.json"  # Replace with your input file path
    output_file = "processed_data.json"  # Replace with desired output file path
    process_json_file(input_file, output_file)