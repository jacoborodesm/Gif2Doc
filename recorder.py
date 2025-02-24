# recorder.py
import mss
import time
import numpy as np
import cv2
import pyautogui

class ScreenRecorder:
    def __init__(self, screen_index=1):
        self.frames = []
        self.recording = False
        self.screen_index = screen_index

    def set_screen(self, screen_index):
        self.screen_index = screen_index

    def start_recording(self):
        self.recording = True
        self.frames = []
        with mss.mss() as sct:
            monitor = sct.monitors[self.screen_index]  # Selecciona la pantalla específica
            screen_width, screen_height = pyautogui.size()  # Resolución lógica de la pantalla
            capture_width, capture_height = monitor["width"], monitor["height"]
            scale_x = capture_width / screen_width
            scale_y = capture_height / screen_height
            
            while self.recording:
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
                
                # Obtener la posición del cursor y ajustarla con la escala
                cursor_x, cursor_y = pyautogui.position()
                if monitor["left"] <= cursor_x <= monitor["left"] + monitor["width"] and monitor["top"] <= cursor_y <= monitor["top"] + monitor["height"]:
                    cursor_x = int((cursor_x - monitor["left"]) * scale_x)
                    cursor_y = int((cursor_y - monitor["top"]) * scale_y)
                    cv2.circle(frame, (cursor_x, cursor_y), 10, (255, 0, 0), -1)  # Dibuja el cursor en rojo
                
                self.frames.append(frame)
                time.sleep(0.1)  # Capturar a ~10 FPS

    def stop_recording(self):
        self.recording = False
        return self.frames
