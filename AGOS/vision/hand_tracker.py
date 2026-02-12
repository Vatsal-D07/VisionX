import cv2
import mediapipe as mp
import time
import os
from AGOS.config.settings import Settings
from AGOS.utils.logger import log

class HandTracker:
    def __init__(self):
        # New Tasks API setup
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        self.HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        # Model path
        model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')

        # State storage for callback
        self.latest_result = None

        def result_callback(result, output_image, timestamp_ms):
            self.latest_result = result

        options = self.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=Settings.MAX_NUM_HANDS,
            min_hand_detection_confidence=Settings.MIN_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=Settings.MIN_DETECTION_CONFIDENCE, # Approximation for tracking
            min_tracking_confidence=Settings.MIN_TRACKING_CONFIDENCE,
            result_callback=result_callback
        )
        
        self.landmarker = HandLandmarker.create_from_options(options)
        self.mp_draw = mp.solutions.drawing_utils if hasattr(mp, 'solutions') else None 
        # Note: mp.solutions might be missing, so we might need a custom drawer or try to import it if it exists elsewhere. 
        # But we know mp.solutions is missing on this system.
        # We will implement a simple drawer manually if needed or skip drawing for now to avoid crash.
        
    def process(self, frame):
        """
        Process the frame and find hands.
        Returns:
            results: Object with .hand_landmarks (list of lists)
        """
        # Convert BGR to RGB
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Current timestamp in ms
        timestamp_ms = int(time.time() * 1000)
        
        # Async detect
        self.landmarker.detect_async(mp_image, timestamp_ms)
        
        # Return latest available result
        return self.latest_result

    def draw_landmarks(self, frame):
        """
        Draws landmarks on the frame.
        Manual implementation since mp.solutions.drawing_utils depends on solutions.
        """
        if self.latest_result and self.latest_result.hand_landmarks:
            for hand_landmarks in self.latest_result.hand_landmarks:
                # hand_landmarks is a list of NormalizedLandmark
                h, w, _ = frame.shape
                
                # Draw connections (simple)
                # We need definitions of connections. 
                # Standard MediaPipe connections:
                CONNECTIONS = [
                    (0,1), (1,2), (2,3), (3,4), # Thumb
                    (0,5), (5,6), (6,7), (7,8), # Index
                    (5,9), (9,10), (10,11), (11,12), # Middle
                    (9,13), (13,14), (14,15), (15,16), # Ring
                    (13,17), (17,18), (18,19), (19,20), # Pinky
                    (0,17) # Wrist to Pinky Base
                ]
                
                # Draw lines
                for start_idx, end_idx in CONNECTIONS:
                    start = hand_landmarks[start_idx]
                    end = hand_landmarks[end_idx]
                    pt1 = (int(start.x * w), int(start.y * h))
                    pt2 = (int(end.x * w), int(end.y * h))
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
                
                # Draw points
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

        return frame

    def get_landmarks(self):
        """
        Returns the first hand's landmarks wrapper to match old API if possible.
        The old API returned an object where .landmark was the list.
        The new API result.hand_landmarks[0] IS the list.
        """
        if self.latest_result and self.latest_result.hand_landmarks:
            # Wrap it in an object with .landmark attribute to avoid rewriting all other code
            class LandmarkWrapper:
                def __init__(self, landmarks):
                    self.landmark = landmarks
            return LandmarkWrapper(self.latest_result.hand_landmarks[0])
        return None
