import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from scapy.all import sniff
import nmap
import time
import threading
import dash

# Initialize Dash app
app = dash.Dash(__name__)

# Global variables for packet sizes and IP addresses
packet_sizes = []
timestamps = []
active_ips = []

# Scan the local network for active IPs
def scan_network():
    network = "192.168.1.0/24"  # Change to your local network
    nm = nmap.PortScanner()
    nm.scan(hosts=network, arguments="-sn")  # -sn is a ping scan to detect hosts
    active_ips = [host for host in nm.all_hosts() if nm[host].state() == "up"]
    return active_ips

# Packet capture callback function
def packet_callback(packet):
    # Only capture IP packets (filtering other protocols)
    if packet.haslayer('IP'):
        timestamp = time.time()
        packet_size = len(packet)
        timestamps.append(timestamp)
        packet_sizes.append(packet_size)

        # Limit the size of lists to avoid memory issues
        if len(timestamps) > 100:
            timestamps.pop(0)
            packet_sizes.pop(0)

# Start sniffing packets
def start_sniffing():
    sniff(prn=packet_callback, store=0, count=0)

# Start packet sniffing in a separate thread
def run_sniffing():
    sniff_thread = threading.Thread(target=start_sniffing)
    sniff_thread.daemon = True
    sniff_thread.start()

# Start Flask app in a separate thread
def run_flask():
    app.run_server(host='0.0.0.0', port=5000, debug=True)

# Dashboard layout
app.layout = html.Div([
    html.H1("Network Traffic Monitoring and IP Tracker"),
    dcc.Graph(id="network_graph"),
    html.Div(id="ip_list"),
    html.Button("Refresh IPs", id="refresh_button", n_clicks=0)
])

# Callback to update the graph
@app.callback(
    Output("network_graph", "figure"),
    [Input("refresh_button", "n_clicks")]
)
def update_graph(n_clicks):
    # Create the plotly graph for real-time traffic data
    trace = go.Scatter(
        x=timestamps,
        y=packet_sizes,
        mode="lines+markers",
        name="Packet Size Over Time"
    )
    return {
        "data": [trace],
        "layout": go.Layout(title="Network Traffic Over Time", xaxis={"title": "Time (seconds)"}, yaxis={"title": "Packet Size (bytes)"})
    }

# Callback to update the list of active IPs
@app.callback(
    Output("ip_list", "children"),
    [Input("refresh_button", "n_clicks")]
)
def update_ip_list(n_clicks):
    global active_ips
    active_ips = scan_network()
    return html.Ul([html.Li(ip) for ip in active_ips])

# Start both sniffing and Flask in parallel
if __name__ == "__main__":
    # Start sniffing in a separate thread
    sniff_thread = threading.Thread(target=run_sniffing)
    sniff_thread.daemon = True
    sniff_thread.start()

    # Start Flask app
    run_flask()
