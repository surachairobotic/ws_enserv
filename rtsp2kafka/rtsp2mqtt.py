import paho.mqtt.client as mqtt
import cv2, time
import numpy as np
from datetime import datetime

# RTSP camera configuration
rtsp_url = 'rtsp://admin:P@ssw0rd1339@192.168.110.11:554/cam/realmonitor?channel=1&subtype=0'

# MQTT configuration
mqtt_broker = '10.10.10.26'
mqtt_port = 1883
mqtt_topic = 'video_stream'
mqtt_username = 'mqttclient'
mqtt_password = '%139User'

# Connect to the MQTT broker
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Connect to the RTSP camera stream
cap = cv2.VideoCapture(rtsp_url)

# Variables for FPS calculation
fps_start_time = time.time()
fps_frame_count = 0
ratio = 4
fps = -1

# Continuously read frames from the camera and publish them to MQTT
while True:
    # Read frame from the camera
    ret, frame = cap.read()

    if not ret:
        break

    # Increment frame count for FPS calculation
    fps_frame_count += 1

    # Calculate elapsed time since the last FPS calculation
    elapsed_time = time.time() - fps_start_time

    # Update FPS every second
    if elapsed_time >= 1.0:
        fps = fps_frame_count / elapsed_time
        fps_frame_count = 0
        fps_start_time = time.time()

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    # Draw FPS on the frame
    cv2.putText(frame, "{} --> FPS: {:.2f}".format(date_time, fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    dim = (int(frame.shape[1]/ratio), int(frame.shape[0]/ratio))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    # Display the frame
    cv2.imshow('RTSP Stream', frame)

    # Convert the frame to a byte array
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

    # Publish the frame to MQTT
    mqtt_client.publish(mqtt_topic, frame_bytes, qos=0)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cap.release()
mqtt_client.disconnect()