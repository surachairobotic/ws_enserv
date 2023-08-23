import pika
import cv2, time
import numpy as np
from datetime import datetime

# RabbitMQ configuration
rabbitmq_host = 'localhost'
rabbitmq_queue = 'camera_frames'

# Camera configuration
camera_url = 'rtsp://admin:P@ssw0rd1339@192.168.110.11:554/cam/realmonitor?channel=1&subtype=0'

# Variables for FPS calculation
fps_start_time = time.time()
fps_frame_count = 0
ratio = 4
fps = -1

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue)

# Connect to the camera stream
cap = cv2.VideoCapture(camera_url)

# Continuously read frames from the camera and publish them to RabbitMQ
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

    # Publish the frame to RabbitMQ
    channel.basic_publish(exchange='',
                          routing_key=rabbitmq_queue,
                          body=frame_bytes)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the resources
cap.release()
connection.close()
