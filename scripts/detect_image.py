#!/usr/bin/env python
"""
Detect objects in a single image using YOLOv8.

Usage:
    python scripts/detect_image.py <path_to_image> --out <output_path> --conf <confidence>

Example:
    python scripts/detect_image.py data/sample.jpg --out output.jpg
"""

import argparse
import cv2
import os
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 image detection")
    parser.add_argument("image_path", help="Path to input image")
    parser.add_argument(
        "--out", default="output.jpg", help="Path to save the annotated image"
    )
    parser.add_argument(
        "--conf", type=float, default=0.25, help="Confidence threshold (0-1)"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    # check input file
    if not os.path.exists(args.image_path):
        print(f"Error: File {args.image_path} not found.")
        return

    print("Loading model...")
    # Load the pre-trained YOLOv8 model (downloads if not present)
    model = YOLO("yolov8n.pt")          # tiny model - fast for demo

    print(f"Processing {args.image_path}...")
    # Read image (OpenCV loads BGR)
    img = cv2.imread(args.image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read {args.image_path}")

    # Run inference - results is a list with one element per image
    results = model(img, conf=args.conf)

    # Render bounding boxes onto the original image (in-place)
    # .plot() returns a BGR numpy array
    annotated = results[0].plot()

    # Save output
    cv2.imwrite(args.out, annotated)
    print(f"Success! Annotated image saved to {args.out}")

if __name__ == "__main__":
    main()
