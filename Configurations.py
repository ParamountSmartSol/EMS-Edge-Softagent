# Configuration (can also come from MQTT later)
gateway_config = {
    "number_of_meters": 0,
    "Serial": [],
    "meters": [],
    "Intervals": 3
}

# MQTT Broker Details, These can be changed to your MQTT Server IP and port
Server = {
    "Host": "localhost",
    "Port": 1883,
    "Basetopic": "EMS/Data/Meter/"
}

# MQTT Settings for configuration listener
# These can be changed to your MQTT Server IP and port
MQTT_Settings_BROKER = "localhost"
MQTT_Settings_PORT = 1883
MQTT_Settings_Listener_Topic = "EMS/Config/GW/"
MQTT_Settings_Request_Topic = "EMS/Config/GW/Request/"

'''gateway_config = {
    "number_of_meters": 2,
    "Serial":[
        {"port":"COM11","baudrate": 9600,"bytesize": 8,"parity": "E","stopbits": 1,"timeout": 2}
    ],
    "meters": [
        {
            "slave_id": 2,
            "blocks": [
                {"start": 2998, "length": 124, "fc": 3, "block_id": "B1"},
                {"start": 2699, "length": 10, "fc": 3, "block_id": "B2"}
            ]
        }
    ],
    "Intervals": 3
}'''