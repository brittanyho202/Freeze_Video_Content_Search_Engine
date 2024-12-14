Here's the revised and more detailed `README.md`, including a comprehensive list of required packages and a step-by-step guide to set up PostgreSQL:

---

# Freeze: Video Content Search Engine

**Freeze** is a video content search engine designed to analyze and extract insights from video files using advanced object detection and scene segmentation techniques. This tool leverages YOLO models for object recognition and Streamlit for an interactive web-based interface.

---

## Features

- **Video Upload and Processing**: Upload video files and analyze them seamlessly.
- **Object Detection**: Uses YOLOv8 for identifying objects in video frames.
- **Scene Segmentation**: Identifies scene changes using `scenedetect` for better content organization.
- **Database Integration**: Saves video metadata to a PostgreSQL database for efficient querying and retrieval.
- **Interactive Interface**: Streamlit-powered UI for uploading videos, viewing results, and interacting with the system.

---

## Requirements

### Python Packages

Install these required Python libraries:

- `streamlit`: For building the interactive web application.
- `ultralytics`: To utilize YOLO models for object detection.
- `opencv-python-headless`: For processing video files.
- `scenedetect`: For detecting scene transitions in videos.
- `psycopg2`: For PostgreSQL database integration.
- `moviepy`: For advanced video processing.
- `torch`: PyTorch library for backend computations.
- `tqdm`: For progress bar display during video processing.

Install all dependencies by running:

```bash
pip install -r requirements.txt
```

Here’s an example `requirements.txt` file:

```
streamlit
ultralytics
opencv-python-headless
scenedetect
psycopg2
moviepy
torch
tqdm
```

### Additional Tools

- **PostgreSQL**: Database management system for storing video metadata.
- **FFmpeg**: Required for video processing by MoviePy and OpenCV. Install it using your system's package manager:
  - On macOS: `brew install ffmpeg`
  - On Ubuntu/Debian: `sudo apt install ffmpeg`
  - On Windows: Download from [FFmpeg](https://ffmpeg.org).

---

## Setting up PostgreSQL

### Step 1: Install PostgreSQL
- **On macOS**: Use Homebrew:
  ```bash
  brew install postgresql
  brew services start postgresql
  ```
- **On Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  ```
  Start PostgreSQL:
  ```bash
  sudo systemctl start postgresql
  ```
- **On Windows**: Download and install from the [official PostgreSQL website](https://www.postgresql.org/download/).

### Step 2: Configure PostgreSQL Database
1. Open the PostgreSQL shell or use a database client like pgAdmin.
2. Create a new user with a password:
   ```sql
   CREATE USER video_user_1 WITH PASSWORD 'user1password';
   ```
3. Create a database:
   ```sql
   CREATE DATABASE video_metadata;
   ```
4. Grant the user access to the database:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE video_metadata TO video_user_1;
   ```

### Step 3: Update Database Details
Update the database connection details in `streamlit3_location.py`:

```python
DB_HOST = "localhost"
DB_NAME = "video_metadata"
DB_USER = "video_user_1"
DB_PASS = "user1password"
```

---

## Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/freeze-video-search-engine.git
   cd freeze-video-search-engine
   ```

2. Download YOLOv8 weights:
   Place the `YOLOv8x.pt` model in the `yolo_models/` directory.

3. Launch the Streamlit app:
   ```bash
   streamlit run streamlit3_location.py
   ```

4. Upload a video file in the app and view results, including object detections and scene transitions.

---

## Usage

- **Video Upload**: Upload your video for analysis.
- **Object Detection**: Detect objects in each frame using YOLOv8.
- **Scene Segmentation**: Identify scene changes using `scenedetect`.
- **Database Storage**: Save and retrieve metadata via PostgreSQL.

---

## Directory Structure

```
.
├── yolo_models/
│   └── YOLOv8x.pt          # YOLO model weights
├── streamlit3_location.py  # Main Streamlit application
├── pyscene_optimized_location.py  # Backend video processing
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## Troubleshooting

- Ensure PostgreSQL is running before launching the app.
- Check the YOLO model weights path and file name (`yolo_models/YOLOv8x.pt`).
- If FFmpeg errors occur, verify its installation using `ffmpeg -version`.

---

## Contributors

- **Brittany** - Developer and Project Lead

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

Let me know if you need further refinements!