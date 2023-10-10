import os
import cv2, time, queue, threading, copy
import face_recognition

frame = None
gFace_locations = None
gNames = None
bThread = True

# Directory where the database images are stored
DATABASE_FOLDER = "./people_resized_25/"

# Initialize known face encodings and names
def initialize_database():
    known_face_encodings = []
    known_face_names = []

    for root, dirs, files in os.walk(DATABASE_FOLDER):
        print([root, dirs, files])
        for name in dirs:
            person_folder = os.path.join(root, name)
            print(os.listdir(person_folder))
            for filename in os.listdir(person_folder):
                print(filename)
                if filename.endswith(".jpg"):
                    print(os.path.join(person_folder, filename))
                    image = face_recognition.load_image_file(os.path.join(person_folder, filename))
                    print(image)
                    print(face_recognition.face_encodings(image))
                    
                    face_encoding = face_recognition.face_encodings(image)[0]
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(name)

    return known_face_encodings, known_face_names

# Recognize faces in the camera feed
def recognize_faces(known_face_encodings, known_face_names, frame):
    t1 = time.time()
    face_locations = face_recognition.face_locations(frame, number_of_times_to_upsample=1)
    t2 = time.time()
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    t3 = time.time()

    names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        names.append(name)
    t4 = time.time()

    #print("Detect: {:.3f}\tRecog: {:.2f}\tCompare: {:.4f}".format(t2-t1, t3-t2, t4-t3))
    return face_locations, names

def resize(img, percentage):
    width = int(img.shape[1] * percentage)
    height = int(img.shape[0] * percentage)
    dim = (width, height)
  
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def recognize_faces_thread():
    global gFace_locations, gNames, frame, known_face_encodings, known_face_names
    while bThread:
        if frame is not None:
            gFace_locations, gNames = recognize_faces(known_face_encodings, known_face_names, frame)

# Open the camera
cap = cv2.VideoCapture(0)

# Ensure the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

t1 = time.time()
# Initialize the known face encodings and names
known_face_encodings, known_face_names = initialize_database()
t2 = time.time()
print(t2-t1)

# Start a separate thread for face recognition
recognition_thread = threading.Thread(
    target=recognize_faces_thread
)
recognition_thread.start()


while True:
    t3 = time.time()
    # Capture a frame from the camera
    ret, local_frame = cap.read()
    #local_frame = cv2.cvtColor(local_frame, cv2.COLOR_BGR2GRAY)
    local_frame = resize(local_frame, 0.25)
    frame = copy.deepcopy(local_frame)

    t4 = time.time()    
    if gFace_locations:
        # Draw rectangles and names on the frame
        for (top, right, bottom, left), name in zip(gFace_locations, gNames):
            cv2.rectangle(local_frame, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(local_frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    t5 = time.time()

    # Display the frame with recognized faces
    cv2.imshow('Camera Feed', local_frame)
    t6 = time.time()

    print([t6-t3])
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        bThread = False
        break

bThread = False
recognition_thread.join()

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
