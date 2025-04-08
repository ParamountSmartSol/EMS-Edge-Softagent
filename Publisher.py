import paho.mqtt.client as mqtt
import json
from Configurations import Server

# MQTT Broker Details
MQTT_BROKER = Server["Host"]
MQTT_PORT = Server["Port"]
MQTT_KEEPALIVE = 60
Mqtt_Basetopic = Server["Basetopic"]

def publish_data_to_mqtt(data, meter_id):
    print("Publishing data to MQTT...")
    # Create the MQTT topic using the meter ID
    topic = Mqtt_Basetopic+meter_id
    # Convert the data to JSON format
    payload = json.dumps(data)
    # Connect to the MQTT broker and publish the data
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    client.publish(topic, payload)
    client.disconnect()

