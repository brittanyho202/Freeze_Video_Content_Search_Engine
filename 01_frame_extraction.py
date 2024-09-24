import cv2
import os

# Function to extract frames
def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0

    # Loop through all frames in the video
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If ret is False, it means we've reached the end of the video
        if not ret:
            break

        # Save the current frame as an image file
        frame_file = os.path.join(output_folder, f"frame_{frame_count:05d}.jpg")
        cv2.imwrite(frame_file, frame)
        print(f"Extracted {frame_file}")

        frame_count += 1

    # When everything is done, release the capture
    cap.release()
    print(f"Total frames extracted: {frame_count}")


video_path = "building.mp4"
output_folder = "extracted_frames"
extract_frames(video_path, output_folder)
