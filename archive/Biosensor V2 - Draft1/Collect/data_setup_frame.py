import tkinter as tk

def create_data_setup_frame(parent):
    frame_data_setup = tk.LabelFrame(parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2)
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    # Chip Name input
    tk.Label(frame_data_setup, text="Chip Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    chip_name_entry = tk.Entry(frame_data_setup, width=20)
    chip_name_entry.grid(row=0, column=1, padx=5, pady=5)
    chip_name_entry.insert(0, "Default Chip")

    # Trial Name input
    tk.Label(frame_data_setup, text="Trial Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    trial_name_entry = tk.Entry(frame_data_setup, width=20)
    trial_name_entry.grid(row=1, column=1, padx=5, pady=5)
    trial_name_entry.insert(0, "Trial 1")