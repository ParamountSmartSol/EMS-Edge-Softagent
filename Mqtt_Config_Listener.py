import paho.mqtt.client as mqtt
import json
from Configurations import gateway_config, MQTT_Settings_BROKER, MQTT_Settings_PORT, MQTT_Settings_Listener_Topic, MQTT_Settings_Request_Topic
from Gateway_ID import get_gateway_id
gateway_id = get_gateway_id()

MQTT_TOPIC = MQTT_Settings_Listener_Topic+gateway_id

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to topic: {MQTT_TOPIC}")
    else:
        print("❌ Failed to connect, return code:", rc)

def on_message(client, userdata, msg):
    global gateway_config
    try:
        config_data = json.loads(msg.payload.decode())
        if all(k in config_data for k in ["number_of_meters", "Serial", "meters", "Intervals"]):
            # Update in-place if you're sharing the dict reference
            gateway_config["number_of_meters"] = config_data["number_of_meters"]
            gateway_config["Serial"] = config_data["Serial"]
            gateway_config["meters"] = config_data["meters"]
            gateway_config["Intervals"] = config_data["Intervals"]
            print("🔧 Configuration updated from MQTT")
        else:
            print("⚠️ Incomplete config received:", config_data)
    except Exception as e:
        print("❌ Error decoding config:", e)

def start_config_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_Settings_BROKER, MQTT_Settings_PORT, 60)
        client.loop_start()
    except Exception as e:
        print("❌ MQTT connection failed:", e)

def request_configurations():
    print("Requesting configurations from MQTT...")
    # Create the MQTT topic for requesting configurations
    topic = MQTT_Settings_Request_Topic+gateway_id
    # Connect to the MQTT broker and publish the request
    client = mqtt.Client()
    client.connect(MQTT_Settings_BROKER, MQTT_Settings_PORT, 60)
    client.publish(topic, gateway_id)
    client.disconnect()
