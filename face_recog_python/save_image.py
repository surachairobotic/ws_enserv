import cv2
import os

def resize(img, scale_percent):
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)
  
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized


# Initialize the camera
cap = cv2.VideoCapture(0)

# Ensure the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    frame = resize(frame, 0.25)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if ret:
        # Display the captured frame
        cv2.imshow('Camera Feed', frame)

        # Wait for the user to press Enter (ASCII code 13)
        key = cv2.waitKey(1)
        if key == 13:  # Enter key pressed
            # Ask the user for a name
            name = input("Enter a name for the person: ")

            # Ensure the name is not empty
            if name.strip() == "":
                print("Name cannot be empty. Please try again.")
            else:
                # Create the directory if it doesn't exist
                if not os.path.exists(f'./people/{name}'):
                    os.makedirs(f'./people/{name}')

                # Find the next available number for the image
                image_number = 1
                while os.path.exists(f'./people/{name}/{image_number}.jpg'):
                    image_number += 1

                # Save the captured image
                image_path = f'./people/{name}/{image_number}.jpg'
                cv2.imwrite(image_path, frame)
                print(f"Image saved as {image_path}")
                break

# Release the camera and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
