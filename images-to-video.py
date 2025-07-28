import cv2
import os

# Paths in Google Drive
path = '/content/drive/MyDrive/Pothole-codes/test/images'  # Path to your images folder
out_path = '/content/drive/MyDrive/Pothole-codes/output_video/'  # Path to save the output video
out_video_name = '1fpscombinedimages.mp4'  # Output video name
out_video_full_path = out_path + out_video_name  # Full output path

# Ensure output directory exists
if not os.path.exists(out_path):
    os.makedirs(out_path)

# List image files in the directory and sort them
pre_imgs = os.listdir(path)
pre_imgs.sort()  # Ensure images are in the correct order
img = []

# Collect full paths of images
for i in pre_imgs:
    img_path = os.path.join(path, i)
    img.append(img_path)

# Define the codec for mp4
cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Read the first image to get the frame size
frame = cv2.imread(img[0])
if frame is None:
    print(f"Error reading the first image: {img[0]}")
    exit()

size = list(frame.shape)
del size[2]  # Remove the color channels dimension
size.reverse()  # Reverse to get (width, height)

# Create the video writer
video = cv2.VideoWriter(out_video_full_path, cv2_fourcc, 1, size)  # 1 fps

# Loop through the images and write each to the video
for i in range(len(img)):
    frame = cv2.imread(img[i])
    if frame is None:
        print(f"Error reading image: {img[i]}")
        continue  # Skip the image if it can't be read
    video.write(frame)
    print('Frame', i + 1, 'of', len(img))

# Release the video writer
video.release()

# Check the output video file size
if os.path.exists(out_video_full_path):
    print('Video created successfully and saved to:', out_video_full_path)
    print('File size:', os.path.getsize(out_video_full_path), 'bytes')
else:
    print('Failed to create video.')
