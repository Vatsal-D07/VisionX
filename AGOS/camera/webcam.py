import cv2
import time
from AGOS.config.settings import Settings
from AGOS.utils.logger import log

class WebcamStream:
    def __init__(self):
        self.cap = cv2.VideoCapture(Settings.CAMERA_ID)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Settings.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Settings.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, Settings.FPS_TARGET)
        
        if not self.cap.isOpened():
            log.error("Could not open webcam.")
            raise IOError("Cannot open webcam")
        
        log.info(f"Webcam started: {Settings.FRAME_WIDTH}x{Settings.FRAME_HEIGHT} @ {Settings.FPS_TARGET}FPS")

    def read(self):
        """
        Reads a frame from the webcam.
        Returns:
            frame: The captured frame (BGR)
            success: Boolean indicating success
        """
        success, frame = self.cap.read()
        if not success:
            log.warning("Failed to read frame")
            return None, False
        
        # Mirror flip for natural interaction
        frame = cv2.flip(frame, 1)
        return frame, True

    def release(self):
        self.cap.release()
        log.info("Webcam released")
