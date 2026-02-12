# AGOS - Air Gesture Operating System

A touchless system control application using OpenCV and MediaPipe.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Controls

- **P (Keyboard)**: Toggle System Control (Pause/Resume).
- **Q (Keyboard)**: Quit application.

## Gestures

| Gesture | Action |
|---------|--------|
| **Open Palm** | Idle / Tracking |
| **Index Finger** | Move Cursor |
| **Pinch** (Index+Thumb) | Left Click |
| **Two Fingers** | Scroll (Up/Down) |
| **Fist** | Lock Screen |
| **Thumbs Up** | Volume Up |
| **Thumbs Down** | Volume Down |
| **Swipe Left/Right** | Switch Tabs |

## Configuration

Adjust sensitivity and camera settings in `config/settings.py`.
