from PIL import Image

# Open the image
image = Image.open('D:/Datasets/CelebA_Spoof/CelebA_Spoof/Data/0/000047.jpg')
print(type(image))

# Calculate the scaling factors for width and height
width, height = image.size
new_width, new_height = 224, 224

width_ratio = new_width / width
height_ratio = new_height / height

# Use the minimum ratio to ensure the image fits within 224x224
min_ratio = min(width_ratio, height_ratio)

# Calculate the new size with the aspect ratio preserved
new_size = (int(width * min_ratio), int(height * min_ratio))

# Resize the image
resized_image = image.resize(new_size)

# Center-crop the resized image to 224x224
left = (new_size[0] - 224) / 2
top = (new_size[1] - 224) / 2
right = (new_size[0] + 224) / 2
bottom = (new_size[1] + 224) / 2

resized_image = resized_image.crop((left, top, right, bottom))

# Save the resized image
resized_image.save('resized_image.jpg')
