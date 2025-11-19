import tkinter as tk
from tkinter import ttk


def settings_tab(tab_settings):
    # Frame for Axis Selector inside the 'Plot Settings' tab
    frame_axis_selector = tk.LabelFrame(
        tab_settings, text="Axis Selector", relief=tk.SUNKEN, borderwidth=2
    )
    frame_axis_selector.pack(fill="x", padx=10, pady=10)

    # Dropdowns for X-axis, Y1-axis, Y2-axis, and Y3-axis
    axes_options = [
        "V1 (V)",
        "V2 (V)",
        "V3 (V)",
        "I1 (A)",
        "I2 (A)",
        "I3 (A)",
        "I4 (A)",
        "I5 (A)",
        "I6 (A)",
        "None",
    ]

    tk.Label(frame_axis_selector, text="X-axis:").grid(
        row=0, column=0, padx=5, pady=5, sticky="e"
    )
    x_axis_dropdown = ttk.Combobox(frame_axis_selector, values=axes_options)
    x_axis_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    x_axis_dropdown.set("V2 (V)")

    tk.Label(frame_axis_selector, text="Y1-axis:").grid(
        row=1, column=0, padx=5, pady=5, sticky="e"
    )
    y1_axis_dropdown = ttk.Combobox(frame_axis_selector, values=axes_options)
    y1_axis_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    y1_axis_dropdown.set("I4 (A)")

    tk.Label(frame_axis_selector, text="Y2-axis:").grid(
        row=2, column=0, padx=5, pady=5, sticky="e"
    )
    y2_axis_dropdown = ttk.Combobox(frame_axis_selector, values=axes_options)
    y2_axis_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    y2_axis_dropdown.set("I6 (A)")

    tk.Label(frame_axis_selector, text="Y3-axis:").grid(
        row=3, column=0, padx=5, pady=5, sticky="e"
    )
    y3_axis_dropdown = ttk.Combobox(frame_axis_selector, values=axes_options)
    y3_axis_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    y3_axis_dropdown.set("None")

    # Frame for Axis Range inside the 'Plot Settings' tab
    frame_axis_range = tk.LabelFrame(
        tab_settings, text="Axis Range", relief=tk.SUNKEN, borderwidth=2
    )
    frame_axis_range.pack(fill="x", padx=10, pady=10)

    # Axis range inputs for X and Y axis
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
