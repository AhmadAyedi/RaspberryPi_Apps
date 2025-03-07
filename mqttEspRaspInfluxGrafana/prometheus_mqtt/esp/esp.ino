#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// WiFi Credentials
const char* ssid = "TOPNET_21F8";
const char* password = "yp5qac98w8";

// MQTT Broker (Raspberry Pi)
const char* mqtt_broker = "192.168.1.21"; // Replace with your Raspberry Pi IP
const int mqtt_port = 1883;
const char* mqtt_topic = "esp32/temperature"; // MQTT topic to publish data

// DHT Sensor
#define DHTPIN 4  // GPIO where the DHT11 is connected
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Initialize WiFi and MQTT Client
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    Serial.begin(115200);
    
    // Connect to WiFi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected");

    // Setup MQTT
    client.setServer(mqtt_broker, mqtt_port);
    while (!client.connected()) {
        Serial.print("Connecting to MQTT...");
        if (client.connect("ESP32Client")) {
            Serial.println("connected!");
        } else {
            Serial.print("failed with state ");
            Serial.println(client.state());
            delay(2000);
        }
    }

    dht.begin();
}

void loop() {
    float temperature = dht.readTemperature();

    if (!isnan(temperature)) {
        String payload = String(temperature);
        client.publish(mqtt_topic, payload.c_str());
        Serial.print("Published Temperature: ");
        Serial.println(payload);
    } else {
        Serial.println("Failed to read from DHT sensor!");
    }

    delay(5000); // Send data every 5 seconds
}
