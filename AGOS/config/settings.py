import cv2

class Settings:
    # Camera
    CAMERA_ID = 0
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS_TARGET = 30
    
    # Hand Tracking
    MAX_NUM_HANDS = 1
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.7
    MODEL_COMPLEXITY = 1  # 0 or 1. 1 is more accurate but slower.
    
    # Smoothing
    SMOOTHING_FACTOR = 0.5  # For mouse movement (exponential moving average)
    
    # Gestures
    GESTURE_CONFIRMATION_FRAMES = 5  # Number of frames a gesture must be held to be valid (temporal stability)
    ACTION_COOLDOWN_MS = 500  # Cooldown between triggers like clicks
    
    # Mouse Control
    MOUSE_SENSITIVITY = 1.5
    CLICK_THRESHOLD_DIST = 0.05  # Normalized distance for pinch
    SCROLL_SENSITIVITY = 30
    
    # Interface
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    TEXT_COLOR = (255, 255, 255)  # White
    TEXT_THICKNESS = 1
    BOX_COLOR = (0, 255, 0)      # Green

    # Application
    APP_NAME = "AGOS - Air Gesture Operating System"
