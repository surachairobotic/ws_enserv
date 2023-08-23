import cv2
from fpdf import FPDF
from PIL import Image

# Global variables to store corner points
top_left = None
top_right = None
bottom_right = None
bottom_left = None

# Create a class that inherits from FPDF
class PDF(FPDF):
    def header(self):
        pass
    
    def footer(self):
        pass
    
    def chapter_title(self, title):
        '''
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
        '''
        pass
    
    def chapter_body(self, image_path):
        print(type(image_path))
        A4w = self.w
        A4h = self.h

        # Get the size of the image
        image = Image.open(image_path)
        image_width, image_height = image.size
        print([A4w, A4h])
        print([image_width, image_height])

        # Calculate the center position for the image in the height
        #image = self.image(image_path, x=0, y=0, w=A4w)
        #print(type(self.image))
        newImageHeight = (image_height / image_width) * A4w
        newY = (A4h - newImageHeight) / 2
        image = self.image(image_path, x=0, y=newY, w=A4w)

# Function to handle mouse click event
def onclick(event, x, y, flags, param):
    global top_left, top_right, bottom_right, bottom_left

    if event == cv2.EVENT_LBUTTONDOWN:
        if top_left is None:
            top_left = (x, y)
            print("Top left corner selected:", top_left)
        elif top_right is None:
            top_right = (x, y)
            print("Top right corner selected:", top_right)
        elif bottom_right is None:
            bottom_right = (x, y)
            print("Bottom right corner selected:", bottom_right)
        elif bottom_left is None:
            bottom_left = (x, y)
            print("Bottom left corner selected:", bottom_left)
            cv2.destroyAllWindows()

# Function to get user input for four corner points by clicking on the image
def get_corner_points(image_path):
    image = cv2.imread(image_path)
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", onclick)
    cv2.waitKey(0)

# Function to crop the image based on corner points
def crop_image(image_path, top_left, top_right, bottom_right, bottom_left):
    image = cv2.imread(image_path)
    cropped_image = image[top_left[1]:bottom_left[1], top_left[0]:top_right[0]]
    cv2.imwrite("cropped_image.png", cropped_image)
    cv2.imshow("Cropped Image", cropped_image)
    cv2.waitKey(0)

# Function to convert the cropped image to PDF
def convert_to_pdf(image_path):
    pdf = PDF()
    pdf.add_page()
    #pdf.chapter_title("Converted Image")
    pdf.chapter_body(image_path)
    pdf.output(image_path.split('.')[0] + ".pdf")

# Main program
def main():
    globalPath = "C:\\Users\\surachair\\Pictures\\"
    savePath = "D:/ws_enserv/"
    image_path = ["ss01.jpg",
                  "ss02.jpg",
                  "ss03.jpg",
                  "ss04.jpg",
                  "ss05.jpg",
                  "ss06.jpg",
                  "ii01.jpg",
                  "ii02.jpg",
                  "ii03.jpg"]

    #image_path = "input_image.jpg"  # Replace with the path to your input image
    #get_corner_points(globalPath + image_path)
    #crop_image(globalPath + image_path, top_left, top_right, bottom_right, bottom_left)
    for x in image_path:
        convert_to_pdf(globalPath + x)

if __name__ == "__main__":
    main()

