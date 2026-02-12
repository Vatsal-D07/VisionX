import cv2
import time
import sys
import os

# Add project root to path if needed, though running as module is better
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AGOS.camera.webcam import WebcamStream
from AGOS.vision.hand_tracker import HandTracker
from AGOS.vision.fps_counter import FPSCounter
from AGOS.gestures.gesture_rules import GestureRules
from AGOS.gestures.gesture_state import GestureState
from AGOS.gestures.gesture_labels import Gestures
from AGOS.actions.action_mapper import ActionMapper
from AGOS.ui.overlay import Overlay
from AGOS.config.settings import Settings
from AGOS.utils.logger import log

def main():
    try:
        # Initialize Modules
        log.info("Initializing AGOS...")
        cam = WebcamStream()
        tracker = HandTracker()
        rules = GestureRules()
        state = GestureState()
        mapper = ActionMapper()
        ui = Overlay()
        fps_counter = FPSCounter()
        
        active_mode = True # Control vs Observation
        
        log.info("System Ready. Press 'q' to exit, 'p' to pause/resume control.")
        
        while True:
            # 1. Capture
            try:
                # Capture frame
                frame, success = cam.read()
                if not success or frame is None:
                    log.warning("Frame read unsuccessful, exiting.")
                    break
            except Exception as e:
                log.warning(f"Error reading from webcam: {e}")
                break


            
            # 2. Vision
            results = tracker.process(frame)
            landmarks = tracker.get_landmarks()
            
            gesture_name = "No Hand"
            final_gesture = Gestures.IDLE
            
            if landmarks:
                # 3. Recognition
                # Static
                raw_gesture = rules.detect_static_gesture(landmarks)
                confirmed_gesture = state.update_gesture(raw_gesture)
                
                # Dynamic (Swipe)
                swipe_gesture = state.check_swipe(landmarks)
                
                # Priority: Swipe > Confirmed Static
                final_gesture = swipe_gesture if swipe_gesture else confirmed_gesture
                gesture_name = final_gesture.value
                
                # 4. Action
                if active_mode:
                    mapper.execute(final_gesture, landmarks, state)
                
                # Visualization
                tracker.draw_landmarks(frame)
            
            # 5. UI & Performance
            fps = fps_counter.update()
            ui.draw(frame, gesture_name, fps, "Control" if active_mode else "Paused")
            
            # 6. Display
            cv2.imshow(Settings.APP_NAME, frame)
            
            # 7. Inputs
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                log.info("Exit requested.")
                break
            elif key == ord('p'):
                active_mode = not active_mode
                log.info(f"Mode switched to: {'Control' if active_mode else 'Paused'}")

    except Exception as e:
        log.error(f"Critical Error: {e}")
        raise e
    finally:
        if 'cam' in locals():
            cam.release()
        cv2.destroyAllWindows()
        log.info("AGOS Shutdown Complete.")

if __name__ == "__main__":
    main()
