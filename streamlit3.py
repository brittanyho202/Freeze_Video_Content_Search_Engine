import streamlit as st
import cv2
import tempfile
from pyscene_optimized import *
from ultralytics import YOLO
import os
import json
import shutil

# Load YOLO model
MODEL_PATH = "yolo_models/YOLOv8x.pt"
model = YOLO(MODEL_PATH)

# Initialize database connection details (update with your credentials)
DB_HOST = "localhost"
DB_NAME = "video_metadata"
DB_USER = "video_user_1"
DB_PASS = "user1password"

st.title("Freeze - Video Content Search Engine")

# Step 1: Upload Video
uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        video_path = temp_video.name

    st.video(video_path)

    # Step 2: Analyze Video
    if st.button("Analyze Video"):
        with st.spinner("Analyzing video..."):
            fps = get_video_fps(video_path)
            base_output_folder = "output_metadata"
            frame_skip = 24  # Default frame skipping value for faster processing

            # Run detection
            metadata_file = detect_scenes_and_objects(
                model=model,
                video_path=video_path,
                base_output_folder=base_output_folder,
                fps=fps,
                frame_skip=frame_skip
            )

            # Insert metadata into the database
            insert_metadata_into_db(metadata_file)

            st.success("Video analyzed and metadata stored successfully!")
            st.session_state["video_path"] = video_path

# Step 3: Search Functionality
if "video_path" in st.session_state:
    st.subheader("Search Scenes")
    object_class = st.text_input("Enter object class (e.g., person, car)")
    confidence_threshold = st.number_input("Confidence Threshold (0.0 to 1.0)", value=0.8, step=0.1)
    min_class_counts_input = st.text_input("Enter minimum class counts in JSON format (e.g., {\"person\": 2})")

    if st.button("Search"):
        with st.spinner("Fetching scenes..."):
            try:
                min_class_counts = json.loads(min_class_counts_input) if min_class_counts_input else None
                scenes = fetch_scenes_from_db(
                    object_class=object_class,
                    confidence_threshold=confidence_threshold,
                    min_class_counts=min_class_counts
                )
                st.session_state["scenes"] = scenes  # Save scenes to session state
                st.success("Scenes fetched successfully!")

            except Exception as e:
                st.error(f"Error fetching scenes: {str(e)}")

# Display and extract scenes if available
if "scenes" in st.session_state and st.session_state["scenes"]:
    scenes = st.session_state["scenes"]
    for scene in scenes:
        st.write(f"Scene {scene['scene']}: {scene['start_time']} - {scene['end_time']}")
        if st.button(f"Extract Scene {scene['scene']}"):
            with st.spinner(f"Extracting Scene {scene['scene']}..."):
                try:
                    video_path = st.session_state["video_path"]
                    # Temporary file to hold the extracted clip
                    temp_dir = tempfile.TemporaryDirectory()
                    clip_path = os.path.join(temp_dir.name, "extracted_scene.mp4")

                    # Create the subclip
                    output_path = create_subclips(video_path, [scene])  # Save the extracted clip

                    if os.path.exists(output_path):
                        # Copy the output to the temporary directory
                        shutil.copy(output_path, clip_path)

                        st.success(f"Scene {scene['scene']} extracted successfully!")
                        st.video(clip_path)
                    else:
                        st.error(f"Failed to extract scene {scene['scene']}. File not found.")
                except Exception as e:
                    st.error(f"Error extracting scene: {str(e)}")

# Display extracted clip if available
if "clip_path" in st.session_state and st.session_state["clip_path"]:
    st.video(st.session_state["clip_path"])
