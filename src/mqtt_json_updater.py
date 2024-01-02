import json
import time
import random
from datetime import datetime
import paho.mqtt.client as mqtt

# Update the JSON File and Publish to MQTT Broker
# MQTT broker details
MQTT_BROKER = '127.0.0.1'
MQTT_PORT = 1883
MQTT_TOPIC = 'pKey/sn'
MQTT_CLIENT_ID = 'mqtt_python_dynamic'

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
        tag_data['seq'] = seq + i  # Increment seq for each tag
        tag_data['data']['m'] = f"Tag_{i}"
        tag_data['data']['v'] = random.randint(1, 10000)
        messages.append(tag_data)

    return messages

def update_json_file(seq):
    """Update the JSON file with new data and publish over MQTT."""
    data = generate_data(seq)
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    # Convert data to JSON string for MQTT publishing
    data_string = json.dumps(data)
    client.publish(MQTT_TOPIC, data_string)
# def update_json_file(seq):
#     """Update the JSON file with new data and publish over MQTT."""
#     data = generate_data(seq)
#     
#     # Load existing data from the file
#     try:
#         with open(json_filename, 'r') as json_file:
#             existing_data = json.load(json_file)
#     except FileNotFoundError:
#         existing_data = []
#     
#     # Append new data to existing data
#     existing_data.extend(data)
#     
#     # Write updated data back to the file
#     with open(json_filename, 'w') as json_file:
#         json.dump(existing_data, json_file, indent=4)
#     
#     # Convert data to JSON string for MQTT publishing
#     data_string = json.dumps(data)
#     client.publish(MQTT_TOPIC, data_string)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

# Initialize MQTT client and connect to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

def main():
    art = """

██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
    """
    print(art)
    print("Starting the magical MQTT JSON updater...")
    seq = 1012800  # Starting sequence number
    try:
        while True:
            update_json_file(seq)
            print(f"Published update to {MQTT_TOPIC} at sequence {seq}")
            seq += 1  # Increment the sequence number
            time.sleep(2)  # Wait for 2 seconds before the next update
    except KeyboardInterrupt:
        print("Stopped updating and publishing to MQTT. Goodbye!")
    finally:
        client.loop_stop()  # Stop the MQTT client loop
        client.disconnect()  # Disconnect from the MQTT broker

if __name__ == "__main__":
    main()