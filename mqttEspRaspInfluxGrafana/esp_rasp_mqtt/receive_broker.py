import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensor/temperature"

def on_message(client, userdata, msg):
    print(f"Received Temperature Data: {msg.payload.decode()} °C")

client = mqtt.Client()
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print(f"Subscribed to topic: {MQTT_TOPIC}")
client.loop_forever()
