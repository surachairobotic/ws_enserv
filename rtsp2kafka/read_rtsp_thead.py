import cv2
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError

import kafka
print(kafka.__version__)

fps = -1
producer = KafkaProducer(bootstrap_servers='10.10.10.25:9092', api_version=(2,0,2))
topic = 'video_topic'
ratio = 4

# RTSP URL
rtsp_url = "rtsp://admin:P@ssw0rd1339@192.168.110.11:554/cam/realmonitor?channel=1&subtype=0"

# Create a VideoCapture object
cap = cv2.VideoCapture(rtsp_url)

# Check if the video capture is successfully opened
if not cap.isOpened():
    print("Failed to open RTSP stream.")
    exit()

# Variables for FPS calculation
fps_start_time = time.time()
fps_frame_count = 0

# Read and display frames until 'q' is pressed
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Check if the frame is successfully read
    if not ret:
        print("Failed to read frame from the video stream.")
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

    # Draw FPS on the frame
    cv2.putText(frame, "FPS: {:.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    dim = (int(frame.shape[1]/ratio), int(frame.shape[0]/ratio))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    # Display the frame
    cv2.imshow('RTSP Stream', frame)

    # png might be too large to emit
    data = cv2.imencode('.jpeg', frame)[1].tobytes()

    future = producer.send(topic, data)
    try:
        future.get(timeout=10)
    except KafkaError as e:
        print(e)
        break

    print('.', end='', flush=True)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close any open windows
cap.release()
cv2.destroyAllWindows()
