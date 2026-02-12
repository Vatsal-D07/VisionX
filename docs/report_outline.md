# College Project Report: Object Detection System

## 1. Abstract
This project presents a real-time Object Detection System developed using the YOLOv8 (You Only Look Once) architecture and Convolutional Neural Networks (CNNs). The system is capable of detecting and classifying multiple objects in static images, video files, and live webcam feeds with high accuracy and speed. The primary goal is to provide a beginner-friendly yet robust computer vision solution suitable for academic demonstration and practical applications like surveillance and traffic monitoring.

## 2. Problem Statement
Traditional image classification models can only identify what is in an image but not where it is located. In many real-world scenarios—such as autonomous driving, security monitoring, and robotics—it is crucial to not only classify objects but also localize them with bounding boxes. This project aims to solve this problem by implementing a fast and efficient object detection pipeline accessible on standard hardware.

## 3. Objectives
- To understand and implement CNN-based object detection.
- To utilize the YOLOv8 architecture for real-time inference.
- To develop Python scripts for image, video, and webcam detection.
- To create a user-friendly Graphical User Interface (GUI) using Streamlit.
- To evaluate the system's performance in varied lighting and environmental conditions.

## 4. Methodology
### 4.1 System Architecture
Input (Image/Video) --> Preprocessing (Resize/Normalization) --> YOLOv8 Model (Feature Extraction & Prediction) --> Post-processing (NMS) --> Output (Bounding Boxes + Labels).

### 4.2 Algorithms Used
- **CNN (Convolutional Neural Network):** for feature extraction.
- **YOLOv8:** An anchor-free, single-stage detector that predicts bounding boxes and class probabilities directly from full images in a single evaluation.

### 4.3 Tools & Libraries
- Python 3.9+
- OpenCV (Computer Vision)
- Ultralytics YOLO (Model Inference)
- Streamlit (UI)

## 5. Results
The system successfully detects 80 standard object classes (from the COCO dataset) including persons, vehicles, and animals.
- **Inference Speed:** achieved ~30 FPS on standard generic CPU/GPU.
- **Accuracy:** High confidence scores (>0.8) for distinct objects.

## 6. Limitations
- Performance may drop in low-light conditions or with heavy occlusion.
- Dependent on the pre-trained COCO dataset classes (unless fine-tuned).
- Requires decent hardware for high-resolution real-time processing.

## 7. Future Scope
- **Custom Dataset Training:** Extending the model to detect specific custom objects (e.g., potholes, specific tools).
- **Mobile App Integration:** Deploying the model to Android/iOS using TFLite.
- **Advanced Tracking:** Implementing object tracking (e.g., DeepSORT) to assign IDs to objects in video.

## 8. Conclusion
The project successfully demonstrates the power of modern deep learning techniques in computer vision. By leveraging YOLOv8, we created a system that balances speed and accuracy, making it suitable for real-time applications. The addition of a Streamlit UI makes the technology accessible to non-technical users.
