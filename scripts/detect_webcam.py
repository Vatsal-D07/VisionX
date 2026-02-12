#!/usr/bin/env python
"""
Real-time object detection from webcam using YOLOv8.

Usage:
    python scripts/detect_webcam.py
"""
import torch
from ultralytics.nn.tasks import DetectionModel

torch.serialization.add_safe_globals([DetectionModel])

from ultralytics import YOLO
import cv2


def main():
    print("Loading model...")
    model = YOLO("yolov8n.pt")
    
    print("Opening webcam...")
    cap = cv2.VideoCapture(0)  # 0 = default webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam started. Press 'ESC' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Inference
        results = model(frame, conf=0.25)
        
        # Visualize
        annotated = results[0].plot()

        cv2.imshow("YOLOv8 Real-Time Detection", annotated)

        # Press ESC to exit
        if cv2.waitKey(1) == 27:
            result_str = "Exiting..."
            print(result_str)
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
