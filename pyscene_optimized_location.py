import os
import cv2
import datetime
from tqdm import tqdm
from ultralytics import YOLO
from scenedetect import SceneManager, open_video
from scenedetect.detectors import ContentDetector
import time
from datetime import timedelta
import psycopg2
import json
from moviepy.video.io.VideoFileClip import VideoFileClip
import torch

# Base line version of Streamlit
print(torch.backends.mps.is_available())

def get_video_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps

def detect_scenes_and_objects(model, video_path, base_output_folder, fps, metadata_file_prefix="video_metadata", frame_skip = 24):
    """
    Optimized function for scene detection and object detection using PySceneDetect and YOLOv8.

    Args:
        model (YOLO): Pre-trained YOLOv8 model for object detection.
        video_path (str): Path to the input video file.
        base_output_folder (str): Base path for output folders and metadata files.
        fps (int): Frames per second of the original video.
        metadata_file_prefix (str): Prefix for the metadata file.
        frame_skip (int): Number of frames to skip during object detection.

    Returns:
        None
    """
    print("fps:" , fps)
    # Start timing
    exec_start_time = time.time()

    # Create output folders
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    annotated_folder = os.path.join(base_output_folder, f"annotated_frames_{timestamp}")
    detected_folder = os.path.join(base_output_folder, f"frames_with_objects_{timestamp}")
    metadata_json_path = os.path.join(base_output_folder, f"{metadata_file_prefix}_{timestamp}.json")

    os.makedirs(annotated_folder, exist_ok=True)
    os.makedirs(detected_folder, exist_ok=True)

    # Initialize PySceneDetect for scene detection
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=30.0))  # Adjust threshold as needed
    scene_manager.detect_scenes(video)
    scene_list = scene_manager.get_scene_list()

    scene_metadata = []

    print("Processing scenes...")
    cap = cv2.VideoCapture(video_path)

    for i, scene in enumerate(tqdm(scene_list)):
        start_time, end_time = scene
        scene_data = {
            "scene": i + 1,
            # "start_time": str(start_time.get_seconds()),
            # "end_time": str(end_time.get_seconds()),
            "start_time": str(timedelta(seconds=start_time.get_seconds())),
            "end_time": str(timedelta(seconds=end_time.get_seconds())),
            "objects": [],
            "class_counts": {}  # New field to store object counts
        }

        # Get frame ranges
        start_frame = start_time.get_frames()
        end_frame = end_time.get_frames()
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        frame_index = start_frame

        while frame_index < end_frame:
            # # Skip frames for faster processing
            # if (frame_index - start_frame) % frame_skip != 0:
            #     frame_index += 1
            #     cap.read()  # Move to the next frame
            #     continue
            # Directly set the video capture to the desired frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

            ret, frame = cap.read()
            if not ret:
                print(f"Warning: Unable to read frame {frame_index}. Skipping...")
                break

            frame_file = f"scene_{i + 1}_frame_{frame_index}.jpg"
            frame_path = os.path.join(detected_folder, frame_file)

            detected_objects = []

            # Perform object detection
            try:
                results = model(frame, device="mps")
                for box in results[0].boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]  # Map class ID to real-world name
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()
                    detected_objects.append({
                        # "class_id": class_id,
                        "class_name": class_name,
                        "confidence": confidence,
                        "bbox": {
                            "x1": float(bbox[0]),
                            "y1": float(bbox[1]),
                            "x2": float(bbox[2]),
                            "y2": float(bbox[3]),
                        },
                    })
                    # Update class count
                    if class_name not in scene_data["class_counts"]:
                        scene_data["class_counts"][class_name] = 0
                    scene_data["class_counts"][class_name] += 1
            except Exception as e:
                print(f"Detection error: {e}")

            # Annotate and save frame if objects are detected
            if detected_objects:
                annotated_img = results[0].plot()
                annotated_path = os.path.join(annotated_folder, frame_file)
                cv2.imwrite(annotated_path, annotated_img)
                cv2.imwrite(frame_path, frame)

                # Append detected objects to scene metadata
                scene_data["objects"].extend(detected_objects)
            # Skip frames directly by updating frame index
            frame_index += frame_skip

        scene_metadata.append(scene_data)

    cap.release()

    # Save metadata to JSON
    with open(metadata_json_path, 'w') as json_file:
        json.dump(scene_metadata, json_file, indent=4)

    # End timing
    exec_end_time = time.time()
    print(f"Scene detection and object detection completed. Metadata saved to {metadata_json_path}")
    # Calculate total processing time
    total_time = exec_end_time - exec_start_time
    # print(f"Total time: {total_time}")
    # Convert total time to hours, minutes, seconds
    hours, remainder = divmod(total_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Total processing time: {int(hours)}h {int(minutes)}m {seconds:.2f}s")
    return metadata_json_path

# Database connection details
DB_HOST = "localhost"
DB_NAME = "video_metadata"
DB_USER = "video_user_1"
DB_PASS = "user1password"

def insert_metadata_into_db(json_file_path):
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM video_metadata")
    # Load JSON metadata
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Insert each scene into the database
    for scene in data:
        if not all(key in scene for key in ["scene", "start_time", "end_time", "objects", "class_counts"]):
            raise ValueError(
                "Invalid JSON format. Ensure all scenes contain 'scene', 'start_time', 'end_time', 'objects', and 'class_counts'.")
        cursor.execute(
            """
            INSERT INTO video_metadata (scene, start_time, end_time, objects, class_counts)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (scene['scene'],
             scene['start_time'],
             scene['end_time'],
             json.dumps(scene['objects']),
             json.dumps(scene['class_counts'])) # Convert dictionary to JSON
        )

    # Commit and close connection
    conn.commit()
    cursor.close()
    conn.close()

def fetch_scenes_from_db(object_class=None, confidence_threshold=50, location=None, min_class_counts=None):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    query = """
        SELECT scene, start_time, end_time
        FROM video_metadata
        WHERE 1=1
    """
    params = []

    if object_class:
        query += """
            AND jsonb_path_exists(
                objects,
                %s
            )
        """
        params.append(f'$[*] ? (@.class_name == "{object_class}")')

    if confidence_threshold is not None:
        query += """
            AND jsonb_path_exists(
                objects,
                %s
            )
        """
        params.append(f'$[*] ? (@.confidence >= {confidence_threshold})')

    if location:
        # Normalize bounding box filtering
        if location == "top-left":
            query += """
                AND jsonb_path_exists(
                    objects,
                    %s
                )
            """
            # Filter for bounding boxes fully within the top-left quadrant
            params.append('$[*] ? (@.bbox.x1 <= 0.5 && @.bbox.y1 <= 0.5 && @.bbox.x2 <= 0.5 && @.bbox.y2 <= 0.5)')
        # Add other quadrants here (e.g., top-right, bottom-left, bottom-right)

    if min_class_counts:
        for class_name, min_count in min_class_counts.items():
            query += """
                    AND COALESCE((class_counts->>%s)::int, 0) >= %s
                """
            params.extend([class_name, min_count])

    cursor.execute(query, params)
    scenes = cursor.fetchall()

    scene_list = [
        {
            "scene": row[0],
            "start_time": row[1].strftime("%H:%M:%S"),
            "end_time": row[2].strftime("%H:%M:%S")
        }
        for row in scenes
    ]

    cursor.close()
    conn.close()
    return scene_list



def create_subclips(video_file, scenes):
    video = VideoFileClip(video_file)

    for scene in scenes:
        # Parse start and end times
        start_parts = list(map(float, scene["start_time"].split(":")))
        end_parts = list(map(float, scene["end_time"].split(":")))

        # Convert to seconds
        start_seconds = start_parts[0] * 3600 + start_parts[1] * 60 + start_parts[2]
        end_seconds = end_parts[0] * 3600 + end_parts[1] * 60 + end_parts[2]

        # Extract subclip
        clip = video.subclipped(start_seconds, end_seconds)
        output_file = f"05_02_clips/scene_{scene['scene']}.mp4"
        print(f"Creating clip: {output_file}")
        clip.write_videofile(output_file, codec="libx264", audio=True, audio_codec="aac")
        return output_file



# if __name__ == "__main__":
#     # Parameters
#     video_path = "resources/new_york.mp4"  # Replace with your video path
#     base_output_folder = "05_output_metadata"
#     fps = get_video_fps(video_path)
#     frame_skip = 24  # Skip every 5th frame for faster processing
#
#     # Load YOLOv8 model for object detection
#     model = YOLO("yolo_models/YOLOv8x.pt")  # Replace with your YOLOv8 weights path
#
#     # Run scene and object detection
#     metadata = detect_scenes_and_objects(model, video_path, base_output_folder, fps, frame_skip=frame_skip)
#
#     # Step 1: Insert metadata into the database
#     insert_metadata_into_db(metadata)
#     # Step 2: Fetch scenes from the database
#     scenes = fetch_scenes_from_db(object_class="person", confidence_threshold=0.80, min_class_counts={"person": 20 })
#     # Step 3: Extract subclips from the video
#     create_subclips(video_path, scenes)
