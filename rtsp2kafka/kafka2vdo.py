from kafka import KafkaConsumer
import cv2
import numpy as np
import time

# Initialize Kafka consumer
#consumer = KafkaConsumer('video_topic', bootstrap_servers='localhost:9092')
consumer = KafkaConsumer('video_topic', bootstrap_servers='10.10.10.25:9092',
                         group_id='my-consumer-group',
                         auto_offset_reset='latest',
                         api_version=(2,0,2))

# Initialize variables for FPS calculation
start_time = time.time()
frame_count = 0

# Consume and process video frames
for message in consumer:
    frame = cv2.imdecode(np.frombuffer(message.value, dtype=np.uint8), -1)

    # Perform any processing on the frame as needed
    # You can add your logic here to verify and process the received video frames

    # Calculate FPS
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # Add FPS text to the image
    fps_text = f"FPS: {fps:.2f}"
    cv2.putText(frame, fps_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
