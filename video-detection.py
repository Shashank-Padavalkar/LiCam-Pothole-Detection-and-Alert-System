import cv2
from ultralytics import YOLO
import os
import yaml
import torch

# Load the custom-trained YOLOv8 model
custom_model_path = r'/content/drive/MyDrive/Pothole-codes/yolov8n_best-so-far-84.pt'  # Update this path as necessary
model = YOLO(custom_model_path)

# Function to detect objects in a video and save the output
def detect_video(input_video_path, output_video_path, class_names):
    # Open the input video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video '{input_video_path}'")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object to save the output video in MP4 format
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Using 'mp4v' for MP4 format
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0  # Initialize frame count for logging

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break

        # Resize the frame to match YOLO input size
        resized_frame = cv2.resize(frame, (640, 640))

        # Perform inference on the frame using YOLOv8
        results = model(resized_frame)

        # Create a copy of the frame for drawing bounding boxes
        result_frame = resized_frame.copy()

        # Process each detection
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            label = int(box.cls[0]) if isinstance(box.cls[0], torch.Tensor) else box.cls[0]
            conf = float(box.conf[0])

            # Draw bounding box on the image
            color = (0, 255, 0)  # Green color for bounding box
            cv2.rectangle(result_frame, (x1, y1), (x2, y2), color, 2)
            label_text = f"{class_names[label]}: {conf:.2f}"
            cv2.putText(result_frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Resize result frame to match the output video size
        result_frame = cv2.resize(result_frame, (frame_width, frame_height))

        # Write the processed frame to the output video
        out.write(result_frame)
        frame_count += 1  # Increment frame count

    # Release the video capture and writer objects
    cap.release()
    out.release()
    print(f"Output video saved to '{output_video_path}' with {frame_count} frames.")

# Step 4: Define input and output video paths
input_video_path = r'/content/drive/MyDrive/Pothole-codes/pothole-road-video/input/pothole_video.mp4'  # Path to input video
output_video_path = r'/content/drive/MyDrive/Pothole-codes/pothole-road-video/output/output84.mp4'  # Path to output video in MP4 format

# Step 5: Load class names from data.yaml
data_yaml_path = r'/content/drive/MyDrive/Pothole-codes/data.yaml'
with open(data_yaml_path, 'r') as file:
    data_config = yaml.safe_load(file)
class_names = data_config['names']

# Step 6: Run object detection on video
detect_video(input_video_path, output_video_path, class_names)
