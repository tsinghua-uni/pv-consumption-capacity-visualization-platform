import json
import paho.mqtt.client as mqtt
import openpyxl

# MQTT broker details
MQTT_BROKER = '127.0.0.1'
MQTT_PORT = 1883
MQTT_TOPIC = 'pKey/sn'

# File name of the Excel file to be updated
excel_filename = 'data-dynamic-mqtt.xlsx'

# Function to update the Excel file with data received from MQTT
def update_excel(data):
    workbook = openpyxl.load_workbook(excel_filename)
    sheet = workbook.active
    for i, value in enumerate(data, start=2):  # Assuming data is a list of values
        sheet[f'B{i}'].value = value
    workbook.save(excel_filename)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}")
    data = json.loads(msg.payload)  # Assuming the payload is a JSON array of values
    update_excel(data)
    # You can call generate_map() here if you want to update the map each time new data comes in

# Initialize MQTT client and set up callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop to process MQTT messages
client.loop_forever()