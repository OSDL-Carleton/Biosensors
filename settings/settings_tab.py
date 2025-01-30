import tkinter as tk
from tkinter import ttk


def settings_tab(tab_settings):

    frame_axis_range = tk.LabelFrame(
        tab_settings, text="Axis Range", relief=tk.SUNKEN, borderwidth=2
    )
    frame_axis_range.pack(fill="x", padx=10, pady=10)

    tk.Label(frame_axis_range, text="X range:").grid(
        row=0, column=0, padx=5, pady=5, sticky="e"
    )
    x_min_entry = tk.Entry(frame_axis_range, width=10)
    x_min_entry.grid(row=0, column=1, padx=(0, 2), pady=5, sticky="w")
    x_min_entry.insert(0, "0")
    tk.Label(frame_axis_range, text="to").grid(row=0, column=2, padx=(2, 2), sticky="w")
    x_max_entry = tk.Entry(frame_axis_range, width=10)
    x_max_entry.grid(row=0, column=3, padx=(2, 5), pady=5, sticky="w")
    x_max_entry.insert(0, "3")

    tk.Label(frame_axis_range, text="Y range:").grid(
        row=1, column=0, padx=5, pady=5, sticky="e"
    )
    y_min_entry = tk.Entry(frame_axis_range, width=10)
    y_min_entry.grid(row=1, column=1, padx=(0, 2), pady=5, sticky="w")
    y_min_entry.insert(0, "0")
    tk.Label(frame_axis_range, text="to").grid(row=1, column=2, padx=(2, 2), sticky="w")
    y_max_entry = tk.Entry(frame_axis_range, width=10)
    y_max_entry.grid(row=1, column=3, padx=(2, 5), pady=5, sticky="w")
    y_max_entry.insert(0, "5")
