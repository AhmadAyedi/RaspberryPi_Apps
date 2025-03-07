#include <WiFi.h>
#include <DHT.h>
#include <HTTPClient.h>

#define DHTPIN 4      // GPIO where the DHT11 is connected
#define DHTTYPE DHT11 

const char* ssid = "TOPNET_21F8";
const char* password = "yp5qac98w8";
const char* influxdb_host = "http://192.168.1.21:8086";  // Replace with your InfluxDB server address
const char* bucket = "sensor_data";  // InfluxDB bucket
const char* org = "enis";  // Your organization name
const char* token = "u92w7MZDGwsyvEZb-6pN4nVCKmq1QT4EmTap2fLkr4wfqt3I0xIVZnyoqo9Q0VLMn3Xg3iFTf9Los7jnQByUWQ==";  // Your InfluxDB token

WiFiClient client;
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

    dht.begin();
}

void sendToInfluxDB(float temp) {
    HTTPClient http;
    
    String url = String(influxdb_host) + "/api/v2/write?org=" + org + "&bucket=" + bucket + "&precision=s";
    
    // Prepare the data in line protocol format for InfluxDB
    String data = "temperature,sensor=esp32 value=" + String(temp);
    
    http.begin(url);
    http.addHeader("Authorization", "Token " + String(token));
    http.addHeader("Content-Type", "text/plain; charset=utf-8");

    // Send the data to InfluxDB
    int httpCode = http.POST(data);

    if (httpCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpCode);
    } else {
        Serial.print("HTTP Request failed. Error: ");
        Serial.println(http.errorToString(httpCode).c_str());
    }

    http.end();
}

void loop() {
    float temp = dht.readTemperature();
    
    if (!isnan(temp)) {
        sendToInfluxDB(temp);  // Send the temperature data to InfluxDB
        Serial.print("Temperature Sent: ");
        Serial.println(temp);
    } else {
        Serial.println("Failed to read from DHT sensor!");
    }

    delay(5000); // Send data every 5 seconds
}
