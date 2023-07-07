import time
import sys
import cv2

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers='10.2.253.109:9092')
topic = 'my-topic'


def emit_video(path_to_video):
    print('start')

    video = cv2.VideoCapture("rtsp://admin:P@ssw0rd1339@192.168.110.11:554/cam/realmonitor?channel=1&subtype=0")

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # png might be too large to emit
        data = cv2.imencode('.jpeg', frame)[1].tobytes()

        future = producer.send(topic, data)
        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break

        print('.', end='', flush=True)

emit_video(0)
# zero is for open webcam or usb webcam
# can play a video just add video file in emit_video function
# rtsp camera stream add rtsp feed in emit_video function