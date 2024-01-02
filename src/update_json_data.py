import json
import time
from datetime import datetime
import random

# The filename of the JSON file to be updated
json_filename = 'dynamic_data.json'

def generate_data(seq):
    """Generate the data for the JSON file with updated tag values."""
    base_data = {
        "ver": "v2.0.0",
        "pKey": "pKey",
        "sn": "sn",
        "seq": seq,
        "type": "cmd/set",
        "ts": int(datetime.now().timestamp()),
        "data": {
            "sysid": "1169925172722737152",
            "dev": "Device_1",
        }
    }
    
    # Generate entries for each tag
    messages = []
    for i in range(1, 36):
        tag_data = base_data.copy()
        tag_data['data']['m'] = f"Tag_{i}"
        tag_data['data']['v'] = random.randint(1, 10000)
        messages.append(tag_data)
    
    return messages

def update_json_file(seq):
    """Update the JSON file with new data."""
    data = generate_data(seq)
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    seq = 1012800  # Starting sequence number
    try:
        while True:
            update_json_file(seq)
            print(f"Updated {json_filename} at sequence {seq}")
            seq += 1  # Increment the sequence number
            time.sleep(2)  # Wait for 2 seconds before the next update
    except KeyboardInterrupt:
        print("Stopped updating the JSON file.")

if __name__ == "__main__":
    main()