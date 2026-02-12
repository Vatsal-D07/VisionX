# 🤖 Object Detection System using YOLOv8

**College Project Submission**  
*Computer Vision & Machine Learning*

## 📌 Project Overview
This project implements an **Object Detection System** capable of identifying and locating objects in:
1. Static Images 📸
2. Video Files 🎥
3. Real-time Webcam Feed 🔴

Built using **Python**, **YOLOv8**, and **OpenCV**.

---

## 🚀 Quick Start Guide

### 1. Environment Setup

It is recommended to use a virtual environment.

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### 2. Running the Detection Scripts

**A. Detect in an Image**
```bash
python scripts/detect_image.py data/sample.jpg --out result.jpg
```
*(Make sure to put a sample image in the data folder first!)*

**B. Detect in a Video**
```bash
python scripts/detect_video.py data/sample.mp4
```

**C. Real-time Webcam**
```bash
python scripts/detect_webcam.py
```

### 3. Launching the UI (Streamlit)

For a user-friendly graphical interface:

```bash
streamlit run ui/app_streamlit.py
```

---

## 📂 Project Structure

```
yolo_project/
│
├── data/                  # Store your input images/videos here
├── models/                # YOLOv8 weights (downloaded automatically)
├── scripts/               # Python processing scripts
│   ├── detect_image.py
│   ├── detect_video.py
│   └── detect_webcam.py
├── ui/                    # Streamlit Dashboard code
│   └── app_streamlit.py
├── docs/                  # Project documentation & reports
├── requirements.txt       # Python dependencies
└── README.md              # Project Guide
```

## 🛠️ Tech Stack
- **YOLOv8 (Ultralytics)**: State-of-the-art object detection model.
- **OpenCV**: Image and video processing.
- **Streamlit**: Interactive web-based UI.
- **Python 3.x**: Core programming language.

## 📝 Author
[Your Name]
[Your Roll Number]
