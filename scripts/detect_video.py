#!/usr/bin/env python
"""
Detect objects in a video file using YOLOv8.

Usage:
    python scripts/detect_video.py <path_to_video> --out <output_path>

Example:
    python scripts/detect_video.py data/sample.mp4 --out output.mp4
"""

import argparse
import cv2
import os
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 video detection")
    parser.add_argument("source", help="Path to video file")
    parser.add_argument(
        "--out", default="output.mp4", help="Path to save the annotated video"
    )
    parser.add_argument(
        "--conf", type=float, default=0.25, help="Confidence threshold (0-1)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: File {args.source} not found.")
        return

    print("Loading model...")
    model = YOLO("yolov8n.pt")

    print(f"Opening video {args.source}...")
    # Open video source
    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video source")

    # Get video properties for writer
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 30.0

    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_writer = cv2.VideoWriter(args.out, fourcc, fps, (width, height))

    print("Processing video frames... Press 'q' to stop early.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break # End of video

        # YOLO inference
        # persist=True helps if tracking is needed, but for simple detection simple call is fine
        results = model(frame, conf=args.conf)
        annotated = results[0].plot()

        out_writer.write(annotated)

        # Optional: show live preview
        cv2.imshow("YOLOv8 Video Detection", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Stopping early...")
            break

    cap.release()
    out_writer.release()
    cv2.destroyAllWindows()
    print(f"Done! Annotated video saved to {args.out}")

if __name__ == "__main__":
    main()
