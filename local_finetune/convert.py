import json
import argparse

def convert_json_to_instruct_jsonl(input_path, output_path):
    # Read the entire JSON file (which should be an array of objects)
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)  # data is a list of dicts

    with open(output_path, 'w', encoding='utf-8') as out_file:
        for item in data:
            # Here we transform each item into the instruct-format
            instruct_obj = {
                "instruction": item.get("title", ""),
                "input": "",
                "output": item.get("processed_text", "")
            }
            # Write as a single line to the JSONL file
            line = json.dumps(instruct_obj, ensure_ascii=False)
            out_file.write(line + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a JSON array to instruction-style JSONL.")
    parser.add_argument('--input', '-i', required=True, help='Path to the input JSON file.')
    parser.add_argument('--output', '-o', required=True, help='Path to the output JSONL file.')
    args = parser.parse_args()

    convert_json_to_instruct_jsonl(args.input, args.output)
