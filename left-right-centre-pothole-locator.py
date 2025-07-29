import cv2
from ultralytics import YOLO

# Load the trained YOLO model (replace 'model_path' with your actual model path)
model = YOLO('yolov8n_best-so-far-84.pt')

# Load image (replace 'image_path' with your actual image path)
image = cv2.imread(r'C:\Users\shash\Desktop\pothole_dark.jpg')
height, width, _ = image.shape

# Run detection on the image
results = model(image)

# Extract bounding boxes from results
for result in results[0].boxes:  # Iterate through detected boxes
    x_min, y_min, x_max, y_max = map(int, result.xyxy[0])  # Bounding box coordinates

    # Calculate the center of the bounding box
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2

    # Define threshold values
    threshold_left = 0.4 * width
    threshold_right = 0.6 * width

    # Draw the bounding box and center point
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Bounding box
    cv2.circle(image, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)  # Center point

    # Check the center position and print the prompt
    if center_x < threshold_left:
        prompt = "KEEP RIGHT"
    elif center_x > threshold_right:
        prompt = "KEEP LEFT"
    else:
        prompt = "POTHOLE IN THE MIDDLE"

    print(prompt)

# Display the image with bounding box (optional)
cv2.imshow("Pothole Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
