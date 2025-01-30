import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt


def plot_tab(tab_plot):
    # Left Frame for data setup, console log, and controls
    left_frame_plot = tk.Frame(tab_plot, width=250, bg="lightgrey")
    left_frame_plot.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

    # Notebook for inner tabs
    notebook_plot = ttk.Notebook(left_frame_plot)
    notebook_plot.pack(fill="both", expand=True)

    # Add components
    create_data_setup_frame(notebook_plot)
    create_console_log_frame(notebook_plot)
    create_controls_frame(notebook_plot)

    # Plot Frame for Plot tab on the right
    plot_frame_plot = tk.Frame(tab_plot)
    plot_frame_plot.pack(fill="both", expand=True, side=tk.RIGHT)
    create_plot_frame(plot_frame_plot)


def create_console_log_frame(parent):
    frame_output = tk.LabelFrame(
        parent, text="Console Log", relief=tk.SUNKEN, borderwidth=2
    )
    frame_output.pack(fill="both", padx=10, pady=5, expand=True)

    output_text = tk.Text(frame_output, height=10, width=45, wrap="none", bg="white")
    scrollbar = tk.Scrollbar(
        frame_output, orient=tk.VERTICAL, command=output_text.yview
    )
    output_text.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


def create_controls_frame(parent):
    frame_controls = tk.LabelFrame(
        parent, text="Controls", relief=tk.SUNKEN, borderwidth=2
    )
    frame_controls.pack(fill="x", padx=10, pady=5)

    run_button = tk.Button(frame_controls, text="Run", width=15)
    run_button.pack(padx=5, pady=10)


def create_data_setup_frame(parent):
    frame_data_setup = tk.LabelFrame(
        parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2
    )
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    def select_folder():
        folder_path = filedialog.askdirectory(
            initialdir="/home/pi/Desktop/Biosensor V2/data",  # Set the default path here
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


def create_plot_frame(parent, total_plots=5):
    current_plot = [1]  # Track the current plot index

    # Container for plot navigation and display
    plot_container = tk.Frame(parent)
    plot_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Navigation function to switch plots
    def switch_plot(direction):
        if direction == "previous" and current_plot[0] > 1:
            current_plot[0] -= 1
        elif direction == "next" and current_plot[0] < total_plots:
            current_plot[0] += 1

        # Update plot with dummy data for demonstration
        ax.cla()
        ax.plot(
            [0, 1, 2, 3],
            [i * current_plot[0] for i in [0, 1, 4, 9]],
            label=f"Plot {current_plot[0]}",
        )
        ax.set_xlabel("X-axis Label")
        ax.set_ylabel("Y-axis Label")
        ax.legend()
        canvas.draw()

        # Update the image label to show the current plot number
        image_label.config(text=f"Image {current_plot[0]} of {total_plots}")

    # Previous and Next buttons for plot navigation
    prev_button = tk.Button(
        plot_container, text="◀", command=lambda: switch_plot("previous")
    )
    prev_button.pack(side=tk.LEFT, padx=5, pady=5)

    next_button = tk.Button(
        plot_container, text="▶", command=lambda: switch_plot("next")
    )
    next_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Plot area setup
    plot_area = tk.Frame(plot_container)
    plot_area.pack(fill="both", expand=True, side=tk.LEFT)

    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3], [0, 1, 4, 9], label="Sample Plot")
    ax.set_xlabel("X-axis Label")
    ax.set_ylabel("Y-axis Label")
    ax.legend()

    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_area)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Interactive toolbar for plot
    toolbar = NavigationToolbar2Tk(canvas, parent)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Footer label to show the current image number
    image_label = tk.Label(
        parent, text=f"Image {current_plot[0]} of {total_plots}", font=("Arial", 12)
    )
    image_label.pack(side=tk.BOTTOM, pady=5)
