import pyshark
import pandas as pd

# Define the network interface (e.g., 'eth0' for Ethernet)
INTERFACE = 'wlan0'

# Capture network packets
print("Starting packet capture... Press Ctrl+C to stop.")
capture = pyshark.LiveCapture(interface=INTERFACE)

# Store captured data
captured_data = []

try:
    for packet in capture.sniff_continuously():
        if 'IP' in packet:
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            host = packet.get_multiple_layers('http.host')
            host = host[0] if host else 'N/A'
            print(f"Source: {src_ip}, Destination: {dst_ip}, Host: {host}")
            captured_data.append([src_ip, dst_ip, host])

except KeyboardInterrupt:
    print("\nPacket capture stopped.")

# Save data to a CSV file
df = pd.DataFrame(captured_data, columns=['Source IP', 'Destination IP', 'Host'])
df.to_csv('network_traffic.csv', index=False)
print("Captured data saved to network_traffic.csv.")
