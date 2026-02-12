import cv2
from AGOS.config.settings import Settings

class Overlay:
    def __init__(self):
        pass

    def draw(self, frame, gesture_name, fps, mode="Control"):
        """
        Draws the HUD overlay on the frame.
        """
        h, w, _ = frame.shape
        
        # 1. Background Panel for Text (Top Left)
        cv2.rectangle(frame, (0, 0), (250, 110), (0, 0, 0), -1)
        # Add transparency? (Simulated by blending, but plain black is faster/clearer for now, or just low alpha)
        # OpenCV doesn't do alpha rects easily without arithmetic. Stick to solid for clarity.
        
        # 2. Info Text
        self._put_text(frame, f"FPS: {int(fps)}", (10, 30))
        self._put_text(frame, f"Mode: {mode}", (10, 60), color=(0, 255, 255))
        self._put_text(frame, f"Gesture: {gesture_name}", (10, 90), color=(0, 255, 0) if gesture_name != "Idle" else (200, 200, 200))
        
        # 3. Safety/Active Indicator (Top Right)
        color = (0, 255, 0) if mode == "Control" else (0, 0, 255)
        cv2.circle(frame, (w - 30, 30), 10, color, -1)
        
        return frame

    def _put_text(self, frame, text, pos, color=Settings.TEXT_COLOR):
        cv2.putText(
            frame, 
            text, 
            pos, 
            Settings.FONT, 
            0.7, 
            color, 
            2, 
            cv2.LINE_AA
        )
