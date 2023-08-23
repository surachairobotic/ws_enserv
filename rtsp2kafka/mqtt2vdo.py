import paho.mqtt.client as mqtt
import cv2
import numpy as np

# MQTT configuration
mqtt_broker = '10.10.10.26'
mqtt_port = 1883
mqtt_topic = 'video_stream'
mqtt_username = 'mqttclient'
mqtt_password = '%139User'

# Callback function for MQTT message reception
def on_message(client, userdata, msg):
    # Convert the received byte array to an image
    nparr = np.frombuffer(msg.payload, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display the image
    cv2.imshow('Received Image', image)
    cv2.waitKey(1)

# Connect to the MQTT broker
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Set up the MQTT message reception callback
mqtt_client.on_message = on_message

# Subscribe to the MQTT topic
mqtt_client.subscribe(mqtt_topic)

# Start the MQTT network loop
mqtt_client.loop_start()

# Keep the client running until interrupted
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Stop the MQTT network loop and disconnect
mqtt_client.loop_stop()
mqtt_client.disconnect()
cv2.destroyAllWindows()
