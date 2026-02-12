import mediapipe as mp
from AGOS.vision.landmark_utils import LandmarkUtils
from AGOS.config.settings import Settings
from AGOS.gestures.gesture_labels import Gestures

class GestureRules:
    def __init__(self):
        # MediaPipe Landmark Indices
        self.WRIST = 0
        self.THUMB_CMC = 1
        self.THUMB_MCP = 2
        self.THUMB_IP = 3
        self.THUMB_TIP = 4
        self.INDEX_FINGER_MCP = 5
        self.INDEX_FINGER_PIP = 6
        self.INDEX_FINGER_DIP = 7
        self.INDEX_FINGER_TIP = 8
        self.MIDDLE_FINGER_MCP = 9
        self.MIDDLE_FINGER_PIP = 10
        self.MIDDLE_FINGER_DIP = 11
        self.MIDDLE_FINGER_TIP = 12
        self.RING_FINGER_MCP = 13
        self.RING_FINGER_PIP = 14
        self.RING_FINGER_DIP = 15
        self.RING_FINGER_TIP = 16
        self.PINKY_MCP = 17
        self.PINKY_PIP = 18
        self.PINKY_DIP = 19
        self.PINKY_TIP = 20

    def detect_static_gesture(self, landmarks):
        """
        Classifies the static gesture from landmarks.
        """
        if not landmarks:
            return Gestures.IDLE

        lm = landmarks.landmark
        
        # Check Hand Orientation (Upright vs Inverted)
        # Upright: Wrist Y > Middle Finger MCP Y (since Y increases downwards)
        is_upright = lm[self.WRIST].y > lm[self.MIDDLE_FINGER_MCP].y
        
        # Finger states (True = extended, False = folded)
        fingers = self._get_finger_states(landmarks, is_upright)
        
        # Pinch check (Thumb and Index tips close)
        pinch_dist = LandmarkUtils.calculate_distance(
            lm[self.THUMB_TIP],
            lm[self.INDEX_FINGER_TIP]
        )

        is_pinch = pinch_dist < Settings.CLICK_THRESHOLD_DIST

        # --- Logic ---

        # 1. Pinch Detection (High Priority)
        # Prioritize pinch if index/thumb are interacting, regardless of other fingers mostly
        if is_pinch:
            return Gestures.PINCH
        
        # 2. Open Palm: All fingers extended
        if all(fingers):
            return Gestures.OPEN_PALM
        
        # 3. Index Finger (Pointing)
        # Index extended, others folded. Thumb can be loose.
        if fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
            return Gestures.INDEX_FINGER

        # 4. Two Fingers (Victory/Peace)
        # Index & Middle extended, others folded.
        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            return Gestures.TWO_FINGERS
            
        # 5. Thumbs Up / Thumbs Down / Fist
        # Common trait: Fingers (Index-Pinky) are folded.
        if not any(fingers[1:]): # Index, Middle, Ring, Pinky are folded
            
            # Analyze Thumb
            thumb_tip_y = lm[self.THUMB_TIP].y
            thumb_ip_y = lm[self.THUMB_IP].y
            thumb_mcp_y = lm[self.THUMB_MCP].y
            
            # Helper to check if thumb is significantly pointing vertical
            # Threshold to ensure it's not just "kinda" up
            vertical_diff = abs(thumb_tip_y - thumb_mcp_y)
            is_vertical_thumb = vertical_diff > 0.05 # Threshold in normalized units

            # Thumbs Up: Tip is ABOVE IP (smaller Y)
            if thumb_tip_y < thumb_ip_y and is_upright:
                return Gestures.THUMBS_UP
            
            # Thumbs Down: Tip is BELOW IP (larger Y)
            # Usually happens when hand is inverted or rotated sideways
            # If inverted, Tip Y > IP Y naturally if pointing "down" (physically)
            if thumb_tip_y > thumb_ip_y: 
                # If hand is inverted, this is natural for extended thumb "up" (physically down)
                # If hand is upright, this is obscure.
                # Usually Thumbs Down involves rotating the hand 180 or 90 degrees.
                # If hand is inverted (is_upright=False), and thumb is "extended" relative to hand...
                # Let's rely on simple Y check: Is thumb pointing DOWN in the frame?
                return Gestures.THUMBS_DOWN
                
            # Fist: Thumb is not sticking out typically. 
            # Or if it is wrapped.
            # If we fall through here, it's a Fist.
            return Gestures.FIST
        
        # Default
        return Gestures.IDLE

    def _get_finger_states(self, landmarks, is_upright):
        """
        Returns list of booleans [Thumb, Index, Middle, Ring, Pinky]
        True if extended, False if folded.
        Adjusts logic based on hand orientation.
        """
        states = []
        lm = landmarks.landmark
        
        # Index (8), Middle (12), Ring (16), Pinky (20)
        # PIPs: 6, 10, 14, 18
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            if is_upright:
                # Upright: Extended if Tip Y < PIP Y (Tip above PIP)
                extended = lm[tip].y < lm[pip].y
            else:
                # Inverted: Extended if Tip Y > PIP Y (Tip below PIP)
                extended = lm[tip].y > lm[pip].y
            states.append(extended)
            
        # Thumb Logic:
        # Thumb doesn't follow strict Up/Down logic like fingers due to rotation.
        # We'll consider thumb "Extended" if it's far from the Palm Center (Index MCP roughly).
        # Or simpler: Is Tip further from MCP than IP is?
        # Let's use a generic openness check for the thumb.
        thumb_tip = lm[4]
        thumb_mcp = lm[2]
        thumb_ip = lm[3]
        pinky_mcp = lm[17]
        
        # Check distance from Pinky MCP (opposite side of palm)
        # If open, thumb tip is far from pinky. If closed (fist), it's closer.
        # This is robust to rotation.
        dist_tip_pinky = LandmarkUtils.calculate_distance(thumb_tip, pinky_mcp)
        dist_ip_pinky = LandmarkUtils.calculate_distance(thumb_ip, pinky_mcp)
        
        # If Tip is further away -> Extended.
        # But for "Thumbs Up", it might not be maximizing this distance.
        # Let's stick to the calling function handling specific Thumb Up/Down cases.
        # Here we just want a generic "Is Thumb participating in open hand?"
        # For "Open Palm", thumb is extended.
        
        thumb_extended = dist_tip_pinky > dist_ip_pinky
        
        return [thumb_extended] + states
