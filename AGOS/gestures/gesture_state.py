from collections import deque
import time
import numpy as np
from AGOS.gestures.gesture_labels import Gestures
from AGOS.config.settings import Settings

class GestureState:
    def __init__(self):
        self.history = deque(maxlen=Settings.GESTURE_CONFIRMATION_FRAMES)
        self.last_action_time = 0
        self.current_gesture = Gestures.IDLE
        self.palm_centroid_history = deque(maxlen=10) # For velocity/swipes
    
    def update_gesture(self, raw_gesture):
        """
        Updates the state with a new raw gesture classification.
        Returns the confirmed gesture.
        """
        self.history.append(raw_gesture)
        
        # Check stability
        if len(self.history) == Settings.GESTURE_CONFIRMATION_FRAMES:
            # If all recent frames match the raw gesture
            if all(g == raw_gesture for g in self.history):
                self.current_gesture = raw_gesture
        
        # Fallback to IDLE if inconsistent? Or just keep last valid?
        # User said "Gesture must persist for N frames". 
        # So we only switch IF persisted. Otherwise keep previous?
        # Better: Return confirmed gesture only if stable, else IDLE or previous.
        # Let's stick to: we only change State if new gesture is stable.
        
        return self.current_gesture

    def check_swipe(self, landmarks):
        """
        Check for dynamic swipes based on palm velocity.
        Returns Swipe Gesture or None.
        """
        if not landmarks:
            return None
            
        # Use Palm center (0)
        wrist = landmarks.landmark[0]
        current_time = time.time()
        self.palm_centroid_history.append((wrist.x, wrist.y, current_time))
        
        # Need enough history
        if len(self.palm_centroid_history) < 3:
            return None
            
        # Calculate velocity (dx/dt)
        # Look at start and end of the history buffer
        start = self.palm_centroid_history[0]
        end = self.palm_centroid_history[-1]
        
        dx = end[0] - start[0]
        dt = end[2] - start[2]
        
        if dt < 0.1: # Avoid division by tiny time or noise if duration is too short
            return None
        
        vx = dx / dt # units per second
        
        # Thresholds (tunable)
        # Reduced threshold to make it more responsive
        SWIPE_VELOCITY_THRESHOLD = 0.3 
        MIN_SWIPE_DIST = 0.15 # Must move at least 15% of screen width relative to start
        
        # Check if actual movement distance is significant
        if abs(dx) < MIN_SWIPE_DIST:
            return None
        
        if abs(vx) > SWIPE_VELOCITY_THRESHOLD:
            if vx > 0:
                # Moving Right (x increases)
                return Gestures.SWIPE_RIGHT
            else:
                return Gestures.SWIPE_LEFT
                
        return None

    def is_cooldown_active(self):
        """
        Checks if we are in cooldown period (e.g. after a click).
        """
        return (time.time() * 1000 - self.last_action_time) < Settings.ACTION_COOLDOWN_MS

    def trigger_action(self):
        """
        Call this when an action is performed to reset cooldown.
        """
        self.last_action_time = time.time() * 1000
