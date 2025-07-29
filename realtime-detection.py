import cv2
from ultralytics import YOLO
import torch
import yaml
import os

# Load the custom-trained YOLOv8 model
custom_model_path = r'C:\Users\shash\Desktop\College Files\LiCam\VS code codes\realtime\yolov8n_pothole_74.pt'
model = YOLO(custom_model_path)

# Function to detect potholes in real-time from webcam
def detect_realtime(class_names):
    # Open the default webcam (index 0)
    cap = cv2.VideoCapture(1)  # Use 0 for default camera, change index if needed

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Press 'q' to quit the real-time detection.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Resize frame to match model's input size (use training size for better accuracy)
        resized_frame = cv2.resize(frame, (720, 720))

        # Perform inference with a lower confidence threshold for higher sensitivity
        results = model(resized_frame, conf=0.2)  # Adjust confidence threshold

        # Create a copy of the frame to draw on
        result_frame = resized_frame.copy()

        pothole_detected = False  # Flag to check if any potholes are detected

        # Process each detection
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            label = int(box.cls[0]) if isinstance(box.cls[0], torch.Tensor) else box.cls[0]
            conf = float(box.conf[0])

            # Filter small bounding boxes or low-confidence detections
            if conf < 0.2 or (x2 - x1) < 30 or (y2 - y1) < 30:
                continue

            # Draw bounding box and label on the image
            color = (0, 255, 0)  # Green color for bounding box
            cv2.rectangle(result_frame, (x1, y1), (x2, y2), color, 2)
            label_text = f"{class_names[label]}: {conf:.2f}"
            cv2.putText(result_frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Check if the detected object is a pothole
            if class_names[label] == "pothole":
                pothole_detected = True

        # If pothole detected, give a voice prompt
        if pothole_detected:
            print("Pothole detected!")
            os.system("say 'Pothole detected!'")  # Voice alert (for macOS); replace with suitable command on Windows/Linux

        # Display the result frame
        cv2.imshow("Real-Time Pothole Detection", cv2.resize(result_frame, (frame_width, frame_height)))

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

# Load class names from data.yaml
data_yaml_path = r'c:\Users\shash\Downloads\data.yaml'
with open(data_yaml_path, 'r') as file:
    data_config = yaml.safe_load(file)
class_names = data_config['names']

# Run real-time pothole detection
detect_realtime(class_names)
