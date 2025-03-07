#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 4      // GPIO where the DHT11 is connected
#define DHTTYPE DHT11 

const char* ssid = "TOPNET_21F8";
const char* password = "yp5qac98w8";
const char* mqtt_server = "192.168.1.21"; // Mosquitto broker IP (Raspberry Pi)

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected");

    client.setServer(mqtt_server, 1883);
    dht.begin();
}

void reconnect() {
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("ESP32Client")) {
            Serial.println("connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    float temp = dht.readTemperature();
    
    if (!isnan(temp)) {
        char tempString[8];
        dtostrf(temp, 1, 2, tempString);
        client.publish("sensor/temperature", tempString);  // Publish to MQTT topic
        Serial.print("Temperature Sent: ");
        Serial.println(tempString);
    } else {
        Serial.println("Failed to read from DHT sensor!");
    }

    delay(5000); // Send data every 5 seconds
}
