import pika
import cv2
import numpy as np
import pyautogui

# RabbitMQ configuration
rabbitmq_host = 'localhost'
rabbitmq_queue = 'camera_frames'

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue)

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Calculate the position to display the image at the bottom-right corner
image_width, image_height = 0, 0  # Initialize image dimensions

bCenter = True

# Callback function for receiving messages
def receive_message(ch, method, properties, body):
    global bCenter
    # Convert the received byte array to an image
    nparr = np.frombuffer(body, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display the image at the bottom-right corner of the screen
    cv2.imshow('Received Image', image)

    if bCenter:
        # Update image dimensions
        image_height, image_width = image.shape[:2]

        # Calculate position to display the image at the bottom-right corner
        x = screen_width - image_width
        y = screen_height - image_height
        cv2.moveWindow('Received Image', x, y)
        bCenter = False

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()

# Consume messages from RabbitMQ
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=receive_message, auto_ack=True)

# Start consuming
channel.start_consuming()
