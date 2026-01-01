import json
import os
import sys
from .converter import KindleConverter

CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} not found.")
        print("Please copy config.example.json to config.json and set your paths.")
        return None
        
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config
    except json.JSONDecodeError:
        print(f"Error: Failed to decode {CONFIG_FILE}. Please ensure it is valid JSON.")
        return None

def main():
    config = load_config()
    if not config:
        sys.exit(1)
        
    input_dir = config.get('input_dir')
    output_dir = config.get('output_dir')
    
    if not input_dir or not output_dir:
        print("Error: 'input_dir' and 'output_dir' must be specified in config.json")
        sys.exit(1)
        
    converter = KindleConverter(input_dir, output_dir)
    converter.convert_all()

if __name__ == "__main__":
    main()
