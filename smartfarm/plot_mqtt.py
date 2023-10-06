import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# MQTT Settings
mqtt_ip = "10.2.253.115"
mqtt_port = 1883
mqtt_username = "mqttclient"
mqtt_password = "%139User"
mqtt_topic = "outTopic"
mqtt_qos = 0

# Variables for real-time plotting
t = 0
x = []
y = [[] for _ in range(16)]  # Assuming there are 16 values in the message
show_limit = 30

# Callback when a message is received
def on_message(client, userdata, message):
    global x, y, t, show_limit
    payload = message.payload.decode("utf-8")
    #print(payload)
    if payload.startswith("#"):
        payload = payload.split(':')[1][:-2]  # Get values part after ":"
        #print(payload)
        values = payload.split(',')
        #print(values)
        values = [int(val) for val in values]
        x.append(t + 1)  # Packet number as x-axis
        t=t+1
        if len(x) > show_limit:
            x = x[-show_limit:]
        for i in range(len(values)):
            y[i].append(values[i])
            if len(y[i]) > show_limit:
                y[i] = y[i][-show_limit:]
            

# MQTT Client Setup
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_ip, mqtt_port, keepalive=60)
client.subscribe(mqtt_topic, mqtt_qos)
client.on_message = on_message

# Function to update the plot
def update_plot(frame):
    global x, y
    #print("==============")
    #print(x)
    #print(y)
    #print("--------------")
    plt.clf()
    for i in range(len(y)):
        plt.plot(x, y[i], label=f"Value {i+1}")
    plt.xlabel("Time (Second)")
    plt.ylabel("Values (0-1024)")
    plt.legend(loc='upper left')

# Start the MQTT loop
client.loop_start()

# Create an initial empty plot
plt.ion()
plt.figure(figsize=(10, 6))
plt.xlabel("Time (Second)")
plt.ylabel("Values (0-1024)")
plt.title("Real-time MQTT Data Plot")
plt.grid(True)

# Animate the plot
ani = FuncAnimation(plt.gcf(), update_plot, interval=100)

# Keep the program running
try:
    while True:
        plt.pause(1)
except KeyboardInterrupt:
    # Close the MQTT client and the plot
    client.loop_stop()
    client.disconnect()
    plt.ioff()
    plt.show()
