import tkinter as tk
from tkinter import ttk
from .data_setup_frame import create_data_setup_frame
from .console_log_frame import create_console_log_frame
from .controls_frame import create_controls_frame
from .plot_frame import create_plot_frame

def analyze_tab(tab_analyze):
    # Left Frame for data setup, console log, and controls
    left_frame_analyze = tk.Frame(tab_analyze, width=250, bg='lightgrey')
    left_frame_analyze.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

    # Notebook for inner tabs
    notebook_analyze = ttk.Notebook(left_frame_analyze)
    notebook_analyze.pack(fill="both", expand=True)

    # Add components
    create_data_setup_frame(notebook_analyze)
    create_console_log_frame(notebook_analyze)
    create_controls_frame(notebook_analyze)

    # Plot Frame for Analyze tab on the right
    plot_frame_analyze = tk.Frame(tab_analyze)
    plot_frame_analyze.pack(fill="both", expand=True, side=tk.RIGHT)
    create_plot_frame(plot_frame_analyze)
