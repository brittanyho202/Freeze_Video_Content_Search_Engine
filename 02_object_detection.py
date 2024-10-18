import os
import cv2
from ultralytics import YOLO


# Function to perform object detection on each frame
def detect_objects_in_frames(model, input_folder, output_folder, detected_folder):
    # Create output and detected folders if they don't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(detected_folder):
        os.makedirs(detected_folder)

    # Iterate through all images in the input folder
    for frame_file in os.listdir(input_folder):
        # Ensure the file is an image (you can filter by extension if needed)
        frame_path = os.path.join(input_folder, frame_file)
        if os.path.isfile(frame_path):
            # Load the image
            img = cv2.imread(frame_path)

            # Perform object detection using YOLOv8
            results = model(img)

            # Draw bounding boxes and labels on the image
            annotated_img = results[0].plot()

            # Save the annotated image to the output folder
            output_path = os.path.join(output_folder, frame_file)
            cv2.imwrite(output_path, annotated_img)
            print(f"Processed and saved: {output_path}")

            # If objects were detected in the frame, save it to the detected_folder as well
            if len(results[0].boxes) > 0:  # Check if any objects were detected
                detected_output_path = os.path.join(detected_folder, frame_file)
                cv2.imwrite(detected_output_path, annotated_img)
                print(f"Objects detected, saved to: {detected_output_path}")


# Initialize YOLOv8 model (pre-trained on COCO dataset)
model = YOLO('yolov8m.pt')  # Use 'yolov8n.pt', 'yolov8s.pt', etc., for different model sizes

# Input and output directories
input_folder = "extracted_frames"
output_folder = "annotated_frames"
detected_folder = "frames_with_objects"  # New folder for frames with detected objects

# Perform object detection on each extracted frame
detect_objects_in_frames(model, input_folder, output_folder, detected_folder)
