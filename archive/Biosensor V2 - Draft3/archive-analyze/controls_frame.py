import tkinter as tk

def create_controls_frame(parent):
    frame_controls = tk.LabelFrame(parent, text="Controls", relief=tk.SUNKEN, borderwidth=2)
    frame_controls.pack(fill="x", padx=10, pady=5)

    run_button = tk.Button(frame_controls, text="Run", width=15)
    run_button.pack(padx=5, pady=10)
