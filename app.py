import time, datetime
import minimalmodbus
from Gateway_ID import get_gateway_id
from Publisher import publish_data_to_mqtt
from Configurations import gateway_config  # initially empty
from Mqtt_Config_Listener import start_config_listener, request_configurations
from Time import get_ntp_time
# Start listening for config before doing anything
start_config_listener()

# Wait for configuration to be loaded
def is_config_ready(cfg):
    return (
        cfg["number_of_meters"] > 0 and
        len(cfg["Serial"]) > 0 and
        len(cfg["meters"]) > 0 and
        cfg["Intervals"] > 0
    )

print("⏳ Waiting for gateway configuration from MQTT...")
while not is_config_ready(gateway_config):
    request_configurations()  # Request config from MQTT
    time.sleep(60)  # Check every minute

print("✅ Gateway configuration received. Starting...")

# Now safe to access config values
PORT = gateway_config["Serial"][0]["port"]
Bardrate = gateway_config["Serial"][0]["baudrate"]
bytesize = gateway_config["Serial"][0]["bytesize"]

parity = {
    "E": minimalmodbus.serial.PARITY_EVEN,
    "O": minimalmodbus.serial.PARITY_ODD
}.get(gateway_config["Serial"][0]["parity"], minimalmodbus.serial.PARITY_NONE)

stopbits = gateway_config["Serial"][0].get("stopbits", 1)
timeout = gateway_config["Serial"][0].get("timeout", 2)

gateway_id = get_gateway_id()

# Read from meters
while True:
    start_time = time.time()
    for meter in gateway_config["meters"]:
        slave_id = meter["slave_id"]
        instrument = minimalmodbus.Instrument(PORT, slave_id)
        instrument.serial.baudrate = Bardrate
        instrument.serial.bytesize = bytesize
        instrument.serial.parity = parity
        instrument.serial.stopbits = stopbits
        instrument.serial.timeout = timeout
        instrument.clear_buffers_before_each_transaction = True

        print(f"\n🔄 Reading from Meter ID {slave_id}")
        data23 = ""
        Meter = True

        for block in meter["blocks"]:
            try:
                start = block["start"]
                length = block["length"]
                fc = block["fc"]
                block_id = block["block_id"]

                data = instrument.read_registers(start, length, functioncode=fc)
                hex_values = [format(reg, '04X') for reg in data]
                hex_string = ''.join(hex_values)
                data23 += hex_string

            except Exception as e:
                print(f"  ❌ Error reading block {block_id}: {e}")
                Meter = False

        message = {
            "Timestamp": get_ntp_time().strftime("%Y-%m-%d %H:%M:%S"),
            "gateway_id": gateway_id,
            "slave_id": slave_id,
            "Status": Meter,
            "data": data23 if Meter else ""
        }
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        publish_data_to_mqtt(message, gateway_id)
        print("  ✅ Data published to MQTT" if Meter else "  ⚠️ Error in reading, sent status")
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    interval = gateway_config["Intervals"] * 60  # Assuming interval is in minutes
    sleep_time = max(0, interval - execution_time)
    print(execution_time," ",sleep_time)
    time.sleep(sleep_time)# Sleep between meter reads

