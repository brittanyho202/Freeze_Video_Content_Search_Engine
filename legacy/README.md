# FREEZE: Video Content Search Engine

## Overview

**FREEZE** is a video content search engine designed to bring ‘Ctrl + F’ functionality to video content. Whether you're editing videos, studying from recorded lectures, or analyzing security footage, FREEZE enables you to quickly find specific scenes or objects within video files.

## Features

- **Object Detection**: Identifies objects within video frames using pre-trained models like YOLOv5.
- **Scene Segmentation**: Organizes video frames into searchable scenes using tools like PySceneDetect.
- **Searchable Metadata**: Generates and indexes metadata, allowing users to search video content efficiently.
- **User Interface**: A web-based interface built with Flask or Django for seamless interaction with the system.

## Technology Stack

- **Programming Language**: Python
- **Object Detection Models**: YOLOv5 or Faster R-CNN
- **Scene Segmentation**: OpenCV, PySceneDetect
- **Search Engine**: Elasticsearch or Whoosh
- **Web Framework**: Flask or Django

## Installation

### Prerequisites

- Python 3.11 or later
- pip (Python package installer)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/brittanyho202/Freeze_Video_Content_Search_Engine.git
   cd Freeze_Video_Content_Search_Engine
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the initial setup script (if available):**

   ```bash
   python setup.py
   ```

## Usage

1. **Upload a Video:**
   - Start the web interface by running the Flask/Django server.
   - Upload a video file through the provided interface.

2. **Search Content:**
   - After the video is processed, use the search bar to find specific scenes or objects.

3. **View Results:**
   - The results will display timestamps and thumbnails of the relevant video scenes.

## Development Roadmap

- **Week 1-2**: Research and environment setup.
- **Week 3-4**: Implement frame extraction and object detection.
- **Week 5-6**: Scene segmentation and metadata generation.
- **Week 7-8**: Develop and integrate search functionality.
- **Week 9-12**: System testing, UI development, and documentation.

## Contact

For any questions or feedback, please contact Brittany Ho at t_ho20@u.pacific.edu
