import os
import tkinter as tk
from tkinter import filedialog

class ModelLoader:
    def __init__(self):
        self.model_path = None

    def select_model(self):
        """Open file dialog to select a .gguf model file."""
        root = tk.Tk()
        root.withdraw()  # Don't show the main tkinter window
        model_path = filedialog.askopenfilename(
            title="Select LLaMA Model",
            filetypes=[("GGUF Files", "*.gguf")],
        )
        if model_path and os.path.exists(model_path):
            self.model_path = model_path
            print(f"Model loaded from: {self.model_path}")
        else:
            print("No model selected.")
        return self.model_path
