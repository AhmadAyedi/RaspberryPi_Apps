from prometheus_client import start_http_server, Gauge
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = "192.168.1.21"  # Raspberry Pi IP
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/temperature"

# Prometheus Metric
temperature_gauge = Gauge("esp32_temperature", "Temperature readings from ESP32")

# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    temp = float(msg.payload.decode())  # Convert received data to float
    print(f"Received Temperature: {temp} C")
    temperature_gauge.set(temp)  # Update Prometheus metric

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start Prometheus HTTP Server on Port 8000
start_http_server(8000)

# MQTT Loop
mqtt_client.loop_forever()
