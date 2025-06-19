import time
import cv2
import ctypes


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

class Capture:
    def __init__(self, window_name = ""):
        self.window_name = window_name
        pass