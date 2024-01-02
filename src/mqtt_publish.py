import paho.mqtt.client as mqtt
import time

# Define the MQTT server details
MQTT_BROKER = '127.0.0.1'
MQTT_PORT = 1883
MQTT_TOPIC = 'pKey/sn'
MQTT_CLIENT_ID = 'mqtt_python'

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Callback when the client publishes a message to the server
def on_publish(client, userdata, mid):
    print("Message Published...")

# Create an MQTT client instance with a client ID
client = mqtt.Client(MQTT_CLIENT_ID)

# Assign event callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop in a non-blocking way to handle reconnection and callbacks
client.loop_start()

# Publish a message every 2 seconds
try:
    while True:
        MQTT_MESSAGE = 'Hello MQTT, now is ' + time.ctime()
        # Publishing the message
        client.publish(MQTT_TOPIC, MQTT_MESSAGE)
        print(f"Sent: {MQTT_MESSAGE}")
        time.sleep(2)  # Sleep for 2 seconds
except KeyboardInterrupt:
    print("Exiting...")

# Stop the loop before finishing
client.loop_stop()

# Disconnecting the client
client.disconnect()