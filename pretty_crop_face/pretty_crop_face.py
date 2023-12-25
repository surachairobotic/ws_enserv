# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

def cut_bottom(image, bottom_cut):
    # Get the height and width of the image
    height, width = image.shape[:2]

    # Calculate the new height after cutting
    new_height = height - bottom_cut

    # Crop the image
    cropped_image = image[:new_height, :]

    return cropped_image

def merge_images_in_row(images):
    # Ensure all images have the same height
    max_height = max(img.shape[0] for img in images)
    images_resized = [cv2.resize(img, (int(img.shape[1] * max_height / img.shape[0]), max_height))
                      for img in images]

    # Concatenate images horizontally
    merged_image = np.concatenate(images_resized, axis=1)

    return merged_image

# Load the image
image_path = "test-1.jpg"

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
# load the input image, resize it, and convert it to grayscale
image = cv2.imread(image_path)
image = imutils.resize(image, width=1000)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# detect faces in the grayscale image
rects = detector(gray, 1)

desiredFaceHeight = 256
desiredFaceWidth = int(desiredFaceHeight/2)
desiredLeftEye = (0.3, 0.3)

best_crop = []

# loop over the face detections
for (i, rect) in enumerate(rects):
    # determine the facial landmarks for the face region, then
    # convert the landmark (x, y)-coordinates to a NumPy array
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    # loop over the face parts individually
    for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
        # loop over the subset of facial landmarks, drawing the
        # specific face part
        for (x, y) in shape[i:j]:
            cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
            
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
    
    leftEyePts = shape[lStart:lEnd]
    rightEyePts = shape[rStart:rEnd]
    
    # compute the center of mass for each eye
    leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
    rightEyeCenter = rightEyePts.mean(axis=0).astype("int")

    # compute the angle between the eye centroids
    dY = rightEyeCenter[1] - leftEyeCenter[1]
    dX = rightEyeCenter[0] - leftEyeCenter[0]
    angle = np.degrees(np.arctan2(dY, dX)) - 180

    # compute center (x, y)-coordinates (i.e., the median point)
    # between the two eyes in the input image
    eyesCenter = (int((leftEyeCenter[0] + rightEyeCenter[0]) // 2), int((leftEyeCenter[1] + rightEyeCenter[1]) // 2))
    cv2.circle(image, eyesCenter, 4, (0, 255, 0), -1)

    cv2.putText(image, str(angle), (eyesCenter[0], eyesCenter[1]+55), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    # compute the desired right eye x-coordinate based on the
    # desired x-coordinate of the left eye
    desiredRightEyeX = 1.0 - desiredLeftEye[0]

    # determine the scale of the new resulting image by taking
    # the ratio of the distance between eyes in the *current*
    # image to the ratio of distance between eyes in the
    # *desired* image
    dist = np.sqrt((dX ** 2) + (dY ** 2))
    desiredDist = (desiredRightEyeX - desiredLeftEye[0])
    desiredDist *= desiredFaceWidth
    scale = desiredDist / dist

    # grab the rotation matrix for rotating and scaling the face
    M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)

    # update the translation component of the matrix
    tX = desiredFaceWidth * 0.5
    tY = desiredFaceHeight * desiredLeftEye[1]
    M[0, 2] += (tX - eyesCenter[0])
    M[1, 2] += (tY - eyesCenter[1])

    # apply the affine transformation
    (w, h) = (desiredFaceWidth, desiredFaceHeight)
    output = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC)

    cropped_output = cut_bottom(output, int(desiredFaceWidth/2))
    
    best_crop.append(cropped_output)

merged_row_image = merge_images_in_row(best_crop)
cv2.imshow("merged_row_image", merged_row_image)

# visualize all facial landmarks with a transparent overlay
#output = face_utils.visualize_facial_landmarks(image, shape)
cv2.imshow("Image", image)
cv2.waitKey(0)