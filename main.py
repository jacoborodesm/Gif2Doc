import keyboard
import tkinter as tk
from recorder import ScreenRecorder
from gif_generator import save_as_gif
import threading
import mss

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder GIF")
        self.recorder = ScreenRecorder()
        self.is_recording = False
        
        self.label = tk.Label(root, text="Selecciona la pantalla principal a grabar:")
        self.label.pack(pady=5)
        
        self.screen_var = tk.IntVar()
        self.screen_var.set(1)
        
        self.screens = mss.mss().monitors
        for i in range(1, len(self.screens)):
            tk.Radiobutton(root, text=f"Pantalla {i}", variable=self.screen_var, value=i).pack()
        
        self.start_label = tk.Label(root, text="Presiona 'F9' para iniciar/detener la grabación.")
        self.start_label.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Esperando...", fg="blue")
        self.status_label.pack(pady=10)
        
        keyboard.add_hotkey("f9", self.toggle_recording)
        keyboard.add_hotkey("esc", self.exit_app)
    
    def toggle_recording(self):
        if self.is_recording:
            self.status_label.config(text="Guardando GIF...", fg="orange")
            self.is_recording = False
            frames = self.recorder.stop_recording()
            if frames:
                filename = self.get_filename()
                if filename:
                    save_as_gif(frames, filename)
                    self.status_label.config(text=f"GIF guardado en output/{filename}.gif", fg="green")
                else:
                    self.status_label.config(text="Guardado cancelado", fg="red")
            else:
                self.status_label.config(text="No se capturaron frames", fg="red")
        else:
            self.recorder.set_screen(self.screen_var.get())
            self.status_label.config(text="Grabando...", fg="red")
            self.is_recording = True
            threading.Thread(target=self.recorder.start_recording, daemon=True).start()
    
    def get_filename(self):
        popup = tk.Toplevel(self.root)
        popup.title("Nombre del archivo")
        tk.Label(popup, text="Ingrese el nombre del archivo:").pack()
        entry = tk.Entry(popup)
        entry.pack()
        
        def save():
            self.filename = entry.get()
            popup.destroy()
        
        tk.Button(popup, text="Guardar", command=save).pack()
        self.root.wait_window(popup)
        return self.filename if hasattr(self, 'filename') else None
    
    def exit_app(self):
        self.root.quit()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()