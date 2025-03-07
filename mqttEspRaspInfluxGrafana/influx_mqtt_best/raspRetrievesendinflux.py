# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
import time

# MQTT Configuration
mqtt_broker = "192.168.1.21"  # IP address of Mosquitto broker (Raspberry Pi)
mqtt_topic = "sensor/temperature"  # The topic where ESP32 publishes data
mqtt_port = 1883  # Default MQTT port

# InfluxDB Configuration
influxdb_url = "http://192.168.1.21:8086"  # InfluxDB URL
influxdb_token = "u92w7MZDGwsyvEZb-6pN4nVCKmq1QT4EmTap2fLkr4wfqt3I0xIVZnyoqo9Q0VLMn3Xg3iFTf9Los7jnQByUWQ=="
influxdb_org = "enis"
influxdb_bucket = "sensor_data"

# Initialize InfluxDB client
client_influxdb = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = client_influxdb.write_api()

# Callback when a message is received on the subscribed topic
def on_message(client, userdata, msg):
    temp = float(msg.payload.decode())  # Decode the temperature data
    print(f"Temperature received: {temp} C")  # Use the proper degree symbol

    # Write to InfluxDB
    from influxdb_client import Point
    point = Point("temperature") \
        .tag("sensor", "esp32") \
        .field("value", temp)

    write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)

# Initialize MQTT client
client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message  # Set the callback function

# Connect to MQTT broker and subscribe to the topic
client_mqtt.connect(mqtt_broker, mqtt_port, 60)
client_mqtt.subscribe(mqtt_topic)

# Start the MQTT loop to listen for messages
print("Listening for MQTT messages...")
client_mqtt.loop_forever()  # This will keep the script running to listen for messages
