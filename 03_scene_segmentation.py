import os
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector


# Function to split the video into scenes and save them as separate video files
def split_video_into_scenes(video_path, output_folder, threshold=15.0):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video using PySceneDetect's `open_video`
    video = open_video(video_path)

    # Create a SceneManager instance
    scene_manager = SceneManager()

    # Add a ContentDetector algorithm to detect scenes based on content changes
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    # Detect the scenes in the video
    scene_manager.detect_scenes(video)

    # Get the list of detected scenes (timecodes)
    scene_list = scene_manager.get_scene_list()

    print(f"Detected {len(scene_list)} scenes in the video.")

    # Iterate over the scenes and split the video using ffmpeg
    for i, scene in enumerate(scene_list):
        start_time = scene[0].get_seconds()  # Start time of the scene
        end_time = scene[1].get_seconds()  # End time of the scene
        scene_filename = os.path.join(output_folder, f"scene_{i + 1}.mp4")

        # Call ffmpeg to extract the scene
        ffmpeg_command = (
            f"ffmpeg -i {video_path} -ss {start_time} -to {end_time} -c copy {scene_filename}"
        )

        # Execute the ffmpeg command
        os.system(ffmpeg_command)

        print(f"Scene {i + 1} saved: {scene_filename}")


# Input video and output folder
video_path = "duck.mp4"
output_folder = "03_scenes_segmented"

# Segment the video into scenes
split_video_into_scenes(video_path, output_folder)
