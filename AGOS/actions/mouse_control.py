import pyautogui
import numpy as np
from AGOS.config.settings import Settings

class MouseControl:
    def __init__(self):
        pyautogui.FAILSAFE = False # We handle safety manually
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = 0, 0
        
    def move(self, x, y):
        """
        Move mouse to normalized (x, y) coordinates with smoothing.
        x, y: 0.0 to 1.0
        """
        # Map to screen
        # Note: Webcam x is mirrored usually, handled in main or here?
        # Let's assume input x is already corrected or raw.
        # If we didn't flip in webcam, 0 is left. If flipped, 0 is right.
        # Webcam.py flips it! So 0 is left, 1 is right. Safe.
        
        target_x = int(x * self.screen_w)
        target_y = int(y * self.screen_h)
        
        # Smoothing
        curr_x = self.prev_x + (target_x - self.prev_x) / Settings.MOUSE_SENSITIVITY
        curr_y = self.prev_y + (target_y - self.prev_y) / Settings.MOUSE_SENSITIVITY
        
        # Clamping
        curr_x = np.clip(curr_x, 0, self.screen_w)
        curr_y = np.clip(curr_y, 0, self.screen_h)
        
        pyautogui.moveTo(curr_x, curr_y)
        
        self.prev_x, self.prev_y = curr_x, curr_y

    def click(self):
        pyautogui.click()
        
    def scroll(self, dy):
        """
        Scroll based on vertical movement difference.
        dy: change in y
        """
        # amplify
        scroll_amount = int(dy * Settings.SCROLL_SENSITIVITY * 100) # multiplier
        pyautogui.scroll(scroll_amount)
