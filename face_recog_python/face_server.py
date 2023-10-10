from fastapi import FastAPI, File, UploadFile, HTTPException
import face_recognition
import os

app = FastAPI()

# Directory where the database images are stored
DATABASE_FOLDER = "./people/"

# Initialize the known face encodings and names
def initialize_database():
    known_face_encodings = []
    known_face_names = []

    for root, dirs, files in os.walk(DATABASE_FOLDER):
        for name in dirs:
            person_folder = os.path.join(root, name)
            for filename in os.listdir(person_folder):
                if filename.endswith(".jpg"):
                    image = face_recognition.load_image_file(os.path.join(person_folder, filename))
                    face_encoding = face_recognition.face_encodings(image)[0]
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(name)

    return known_face_encodings, known_face_names

# Recognize faces in the uploaded image
def recognize_faces(known_face_encodings, known_face_names, image_path):
    results = []

    unknown_image = face_recognition.load_image_file(image_path)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)

    if len(unknown_face_encodings) == 0:
        return []

    for unknown_face_encoding in unknown_face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        results.append(name)

    return results

@app.post("/face_recog/")
async def face_recognition_endpoint(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    try:
        with open("uploaded_image.jpg", "wb") as image_file:
            image_file.write(file.file.read())

        known_face_encodings, known_face_names = initialize_database()
        names = recognize_faces(known_face_encodings, known_face_names, "uploaded_image.jpg")
        return {"names": names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
