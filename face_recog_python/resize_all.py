from PIL import Image
import os

# Specify the folder where your images are located
folder_path = "./people/"

# Specify the output folder for resized images
output_folder = "./people_resized_25_gray/"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through the folders and subfolders
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith(".jpg"):
            # Get the full path of the image
            image_path = os.path.join(root, filename)

            # Open the image using Pillow
            img = Image.open(image_path)
            
            # Convert the image to grayscale
            img = img.convert("L")

            # Calculate the new dimensions (0.1 times the original)
            width, height = img.size
            new_width = int(width * 0.25)
            new_height = int(height * 0.25)

            # Resize the image
            resized_img = img.resize((new_width, new_height))

            # Get the relative path from the input folder
            relative_path = os.path.relpath(image_path, folder_path)

            # Define the output filename by joining with the output folder
            output_filename = os.path.join(output_folder, relative_path)

            # Create the folder structure if it doesn't exist
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)

            # Save the resized image with the new filename
            resized_img.save(output_filename)

            # Close the image
            img.close()
            #grayscale_img.close()

print("Images resized and saved successfully.")
