import tkinter as tk

def create_test_controls_frame(parent):
    frame_controls = tk.LabelFrame(parent, text="Test Controls", relief=tk.SUNKEN, borderwidth=2)
    frame_controls.pack(fill="x", padx=10, pady=5)

    run_button = tk.Button(frame_controls, text="Run", width=10)
    run_button.grid(row=0, column=0, padx=5, pady=5)
    pause_button = tk.Button(frame_controls, text="Pause/Resume", width=10)
    pause_button.grid(row=0, column=1, padx=5, pady=5)
    end_button = tk.Button(frame_controls, text="End", width=10)
    end_button.grid(row=0, column=2, padx=5, pady=5)
