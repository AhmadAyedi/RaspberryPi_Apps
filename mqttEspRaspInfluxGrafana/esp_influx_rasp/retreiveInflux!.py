from influxdb_client import InfluxDBClient
import time  # Ensure the 'time' module is imported correctly

# Configuration variables
url = "http://192.168.1.21:8086"  # InfluxDB URL
token = "u92w7MZDGwsyvEZb-6pN4nVCKmq1QT4EmTap2fLkr4wfqt3I0xIVZnyoqo9Q0VLMn3Xg3iFTf9Los7jnQByUWQ=="  # Your token
org = "enis"  # Your organization name
bucket = "sensor_data"  # Your bucket name

# Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# Query API
query_api = client.query_api()

# Flux query to get the data from the last 1 hour
query = f'''
from(bucket: "{bucket}")
|> range(start: -1h)
|> filter(fn: (r) => r["_measurement"] == "temperature" and r["_field"] == "value")
'''

# Continuously track the data
while True:
    result = query_api.query(query=query)

    # Process and display the data
    for table in result:
        for record in table.records:
            time_data = record["_time"]  # Renamed variable to avoid conflict with time module
            value = record["_value"]
            print(f"Time: {time_data}, Temperature: {value} °C")

    # Wait for 5 seconds before running the query again
    time.sleep(5)

# Close the client (this line won't be reached in an infinite loop, but added for completeness)
client.close()
