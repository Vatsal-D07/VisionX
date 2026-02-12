from AGOS.gestures.gesture_labels import Gestures
from AGOS.actions.mouse_control import MouseControl
from AGOS.actions.system_control import SystemControl
from AGOS.config.settings import Settings
import time

class ActionMapper:
    def __init__(self):
        self.mouse = MouseControl()
        self.system = SystemControl()
        self.prev_scroll_y = None
        
    def execute(self, gesture, landmarks, gesture_state):
        """
        Executes action based on gesture.
        gesture: Confirmed Gesture enum
        landmarks: MediaPipe landmarks
        gesture_state: GestureState object (for cooldowns)
        """
        
        # 1. Handle Navigation/System Swipes (High Priority, defined by dynamic state)
        # Check for swipes explicitly if passed or handled via separate channel? 
        # In main loop, we might check for swipes first. 
        # But here, let's assume 'gesture' accounts for static, and we check swipes if 'gesture' is IDLE or OPEN?
        # Actually user spec: "Swipe L/R -> Switch tabs".
        # If 'gesture' argument can be SWIPE, handle it.
        
        if gesture == Gestures.SWIPE_RIGHT:
            if not gesture_state.is_cooldown_active():
                # Map Swipe Right -> Next Tab
                self.system.switch_tab_right()
                gesture_state.trigger_action()
            return
            
        if gesture == Gestures.SWIPE_LEFT:
            if not gesture_state.is_cooldown_active():
                self.system.switch_tab_left()
                gesture_state.trigger_action()
            return
            
        # If no landmarks (e.g. swipe detected but lost hand?), return
        if not landmarks:
            return

        # 2. Continuous Actions (Mouse, Scroll)
        
        if gesture == Gestures.INDEX_FINGER:
            # Move Mouse
            # Use Index Finger Tip (8)
            tip = landmarks.landmark[8]
            self.mouse.move(tip.x, tip.y)
            self.prev_scroll_y = None # Reset scroll
            
        elif gesture == Gestures.TWO_FINGERS:
            # Scroll
            # Use Index Tip y or average of Index+Middle
            tip_y = landmarks.landmark[8].y
            
            if self.prev_scroll_y is not None:
                dy = self.prev_scroll_y - tip_y # Up movement -> Scroll Up?
                if abs(dy) > 0.01: # Noise threshold
                    self.mouse.scroll(dy)
            
            self.prev_scroll_y = tip_y
            
        elif gesture == Gestures.PINCH:
            # Click
            # Using cooldown to prevent double clicks
            if not gesture_state.is_cooldown_active():
                self.mouse.click()
                gesture_state.trigger_action()
            # Also allow movement while pinching? Drag and drop?
            # User: "Click: Triggered only on confirmed pinch". 
            # Doesn't explicitly say Drag. We'll just click.
            # To support Drag, we'd mouseDown on entry, mouseMove, mouseUp on exit.
            # Simplify for now: Click once.
            
            # Optional: Move while pinching (Drag)?
            if gesture == Gestures.PINCH:
                tip = landmarks.landmark[8]
                self.mouse.move(tip.x, tip.y)
        
        else:
            self.prev_scroll_y = None # Reset scroll anchor

        # 3. Discrete Actions (System)
        
        if gesture == Gestures.FIST:
            if not gesture_state.is_cooldown_active():
                self.system.lock_screen()
                gesture_state.trigger_action()
                
        elif gesture == Gestures.THUMBS_UP:
             # Volume is continuous or discrete?
             # "Thumbs Up -> Volume Up". Usually continuous if held.
             # We'll allow it every frame or throttle it?
             # Let's throttle slightly less than full cooldown, or standard cooldown.
             # If handled every frame, volume zooms up. 
             # Let's use a shorter cooldown or frame skip.
             # Actually, simpler: trigger once per Cooldown.
            if not gesture_state.is_cooldown_active():
                self.system.volume_up()
                # Short cooldown for volume?
                # gesture_state.trigger_action() # Uses 500ms default. Too slow for volume?
                # Hack: Manually set last_action time to allow 100ms?
                # Or just let it be slow and steady. 
                gesture_state.trigger_action()

        elif gesture == Gestures.THUMBS_DOWN:
            if not gesture_state.is_cooldown_active():
                self.system.volume_down()
                gesture_state.trigger_action()
