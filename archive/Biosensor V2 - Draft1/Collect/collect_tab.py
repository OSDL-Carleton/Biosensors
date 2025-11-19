import tkinter as tk
from tkinter import ttk
from collect.data_setup_frame import create_data_setup_frame
from collect.test_params_frame import create_test_params_frame
from collect.console_log_frame import create_console_log_frame
from collect.test_controls_frame import create_test_controls_frame
from collect.plot_frame import create_plot_frame

def collect_tab(tab_collect):
    # Frame for parameters and controls on the left side in Collect Tab
    left_frame_collect = tk.Frame(tab_collect, width=250, bg='lightgrey')
    left_frame_collect.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

    # Notebook for inner tabs in the Collect left frame
    notebook_collect = ttk.Notebook(left_frame_collect)
    notebook_collect.pack(fill="both", expand=True)

    # Add components
    create_data_setup_frame(notebook_collect)
    create_test_params_frame(notebook_collect)
    create_console_log_frame(notebook_collect)
    create_test_controls_frame(notebook_collect)

    # Plot Frame for Collect tab to the right
    plot_frame_collect = tk.Frame(tab_collect, width=750)
    plot_frame_collect.pack(fill="both", expand=True, side=tk.RIGHT)
    create_plot_frame(plot_frame_collect)  # Add the plot frame
