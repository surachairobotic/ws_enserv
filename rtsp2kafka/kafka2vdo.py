from kafka import KafkaConsumer
import cv2
import numpy as np
import time, copy

# Initialize Kafka consumer
#consumer = KafkaConsumer('video_topic', bootstrap_servers='localhost:9092')
'''
consumer = KafkaConsumer('video_topic', bootstrap_servers='10.10.10.25:9092',
                         group_id='my-consumer-group',
                         auto_offset_reset='latest',
                         max_poll_records=1,
                         api_version=(2,0,2))
'''
consumer = KafkaConsumer(
    'video_topic',
    bootstrap_servers='10.10.10.25:9092',
    group_id='my-consumer-group',
    auto_offset_reset='latest',
    api_version=(2, 0, 2),
    max_poll_records=1  # Limit to fetching only 1 record
)

# Initialize variables for FPS calculation
fps_start_time = time.time()
fps_frame_count = 0
fps = -1

# Consume and process video frames
for message in consumer:
    frame = copy.deepcopy(cv2.imdecode(np.frombuffer(message.value, dtype=np.uint8), -1))

    new_frame = cv2.resize(frame, (960, 540), interpolation=cv2.INTER_AREA)

    # Perform any processing on the frame as needed
    # You can add your logic here to verify and process the received video frames

    # Calculate FPS
    fps_frame_count += 1
    elapsed_time = time.time() - fps_start_time

    # Update FPS every second
    if elapsed_time >= 0.25:
        fps = fps_frame_count / elapsed_time
        fps_frame_count = 0
        fps_start_time = time.time()

    # Add FPS text to the image
    fps_text = f"FPS: {fps:.2f}"
    cv2.putText(new_frame, fps_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Video', new_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
