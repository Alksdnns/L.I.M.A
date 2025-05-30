import tkinter as tk
from tkinter import Canvas
import threading

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("L.I.M.A")
        self.root.geometry("400x500")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        header = tk.Label(self.root, text="L.I.M.A", bg="#000000", fg="white", font=("Helvetica", 16, "bold"))
        header.pack(pady=(10, 5))

        self.chat_frame = tk.Frame(self.root, bg="#000000")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.waveform_canvas = Canvas(self.root, width=360, height=100, bg="#000000", highlightthickness=0)
        self.waveform_canvas.pack(pady=10)
        self._draw_waveform()

        self.listen_label = tk.Label(self.root, text="Listening...", bg="#000000", fg="white", font=("Helvetica", 12, "italic"))
        self.listen_label.pack()

        self.mic_canvas = Canvas(self.root, width=60, height=60, bg="#000000", highlightthickness=0)
        self.mic_canvas.pack(pady=10)
        self.mic_canvas.create_oval(5, 5, 55, 55, fill="#333333", outline="")
        self.mic_canvas.create_text(30, 30, text="🎤", font=("Arial", 20), fill="white")

        self.gear_icon = Canvas(self.root, width=30, height=30, bg="#000000", highlightthickness=0)
        self.gear_icon.place(x=360, y=460)
        self.gear_icon.create_text(15, 15, text="⚙", font=("Arial", 14), fill="white")

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

    def _draw_waveform(self):
        bar_colors = ["#ff6b6b", "#feca57", "#48dbfb", "#1dd1a1", "#5f27cd", "#ff9ff3", "#54a0ff"]
        bar_heights = [10, 25, 40, 60, 40, 25, 10]
        x = 30
        for i in range(len(bar_heights)):
            self.waveform_canvas.create_line(x, 70, x, 70 - bar_heights[i],
                                             fill=bar_colors[i % len(bar_colors)], width=4, capstyle=tk.ROUND)
            x += 20

    def start(self):
        threading.Thread(target=self.root.mainloop, daemon=True).start()

    def add_user_message(self, text):
        msg = tk.Label(
            self.chat_frame,
            text=text,
            bg="#7E7B7B", fg="#ffffff", font=("Helvetica", 12),
            wraplength=300, justify="left", padx=12, pady=10
        )
        msg.pack(pady=5, padx=20, anchor="w")

    def add_assistant_message(self, text):
        msg = tk.Label(
            self.chat_frame,
            text=text,
            bg="#444444", fg="#ffffff", font=("Helvetica", 12),
            wraplength=300, justify="left", padx=12, pady=10
        )
        msg.pack(pady=5, padx=20, anchor="w")

    def update_listening_status(self, status):
        self.listen_label.config(text=status)
