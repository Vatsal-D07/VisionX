import pyautogui

class SystemControl:
    @staticmethod
    def volume_up():
        pyautogui.press('volumeup')
        
    @staticmethod
    def volume_down():
        pyautogui.press('volumedown')
        
    @staticmethod
    def lock_screen():
        # Windows specific
        pyautogui.hotkey('win', 'l')
        
    @staticmethod
    def switch_tab_right():
        # Ctrl + Tab
        pyautogui.hotkey('ctrl', 'tab')
        
    @staticmethod
    def switch_tab_left():
        # Ctrl + Shift + Tab
        pyautogui.hotkey('ctrl', 'shift', 'tab')
