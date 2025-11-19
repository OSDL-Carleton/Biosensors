import tkinter as tk
from tkinter import filedialog
import os


def create_data_setup_frame(parent):
    frame_data_setup = tk.LabelFrame(
        parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2
    )
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    def select_folder():
        folder_path = filedialog.askdirectory(
            initialdir=os.path.join(os.path.expanduser("~"), "Desktop"),
            title="Select a Folder",
        )
        if folder_path:
            folder_label.config(text=folder_path)

    tk.Label(frame_data_setup, text="Select Folder:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    select_folder_button = tk.Button(
        frame_data_setup, text="Browse", command=select_folder
    )
    select_folder_button.grid(row=0, column=1, padx=5, pady=5)

    folder_label = tk.Label(
        frame_data_setup,
        text="No folder selected",
        wraplength=200,
        anchor="w",
        justify="left",
        bg="lightgrey",
    )
    folder_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
