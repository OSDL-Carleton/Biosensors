import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import os

def analyze_tab(tab_analyze):
    # Dummy data: Define the total number of plots available
    total_plots = 5
    current_plot = [1]  # Use a list to keep track of the current plot index in a mutable way

    # Left Frame for chip selection, console log, and controls in Analyze Tab
    left_frame_analyze = tk.Frame(tab_analyze, width=250, bg='lightgrey')
    left_frame_analyze.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

    # Notebook for inner tabs in the Analyze left frame
    notebook_analyze = ttk.Notebook(left_frame_analyze)
    notebook_analyze.pack(fill="both", expand=True)

    # Data Setup Frame with Folder Selection Button
    frame_data_setup = tk.LabelFrame(notebook_analyze, text="Data Setup", relief=tk.SUNKEN, borderwidth=2)
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    # Function to open folder dialog and update the label
    def select_folder():
        folder_path = filedialog.askdirectory(initialdir=os.path.join(os.path.expanduser("~"), "Desktop"), title="Select a Folder")
        if folder_path:
            folder_label.config(text=folder_path)

    # Folder Selection button
    tk.Label(frame_data_setup, text="Select Folder:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    select_folder_button = tk.Button(frame_data_setup, text="Browse", command=select_folder)
    select_folder_button.grid(row=0, column=1, padx=5, pady=5)

    # Label to display the selected folder path
    folder_label = tk.Label(frame_data_setup, text="No folder selected", wraplength=200, anchor="w", justify="left", bg="lightgrey")
    folder_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    # Console Log Frame
    frame_output = tk.LabelFrame(notebook_analyze, text="Console Log", relief=tk.SUNKEN, borderwidth=2)
    frame_output.pack(fill="both", padx=10, pady=5, expand=True)

    # Adding a scrollbar
    output_text = tk.Text(frame_output, height=10, width=45, wrap="none", bg='white')
    scrollbar = tk.Scrollbar(frame_output, orient=tk.VERTICAL, command=output_text.yview)
    output_text.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Frame for test controls inside the 'Analyze' tab with only the Run button
    frame_controls = tk.LabelFrame(notebook_analyze, text="Test Controls", relief=tk.SUNKEN, borderwidth=2)
    frame_controls.pack(fill="x", padx=10, pady=5)

    run_button = tk.Button(frame_controls, text="Run", width=15)
    run_button.pack(padx=5, pady=10)

    # Plot Frame for Analyze tab to the right
    plot_frame_analyze = tk.Frame(tab_analyze)
    plot_frame_analyze.pack(fill="both", expand=True, side=tk.RIGHT)

    # Create a frame to hold the plot and navigation arrows
    plot_container = tk.Frame(plot_frame_analyze)
    plot_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Navigation arrows for switching between plots
    def switch_plot(direction):
        # Update the current plot index
        if direction == "previous" and current_plot[0] > 1:
            current_plot[0] -= 1
        elif direction == "next" and current_plot[0] < total_plots:
            current_plot[0] += 1

        # Update plot with dummy data for demonstration
        ax_analyze.cla()  # Clear current plot
        ax_analyze.plot([0, 1, 2, 3], [i * current_plot[0] for i in [0, 1, 4, 9]], label=f"Plot {current_plot[0]}")
        ax_analyze.set_xlabel("X-axis Label")
        ax_analyze.set_ylabel("Y-axis Label")
        ax_analyze.legend()
        canvas_analyze.draw()

        # Update the image label to show the current plot number
        image_label.config(text=f"Image {current_plot[0]} of {total_plots}")

    # Create the Previous button and position it to the left of the plot
    prev_button = tk.Button(plot_container, text="◀", command=lambda: switch_plot("previous"))
    prev_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Create the Next button and position it to the right of the plot
    next_button = tk.Button(plot_container, text="▶", command=lambda: switch_plot("next"))
    next_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Create a frame for the plot itself within the plot container, between the buttons
    plot_area = tk.Frame(plot_container)
    plot_area.pack(fill="both", expand=True, side=tk.LEFT)

    # Create a sample plot in the Analyze tab
    fig_analyze, ax_analyze = plt.subplots()
    ax_analyze.plot([0, 1, 2, 3], [0, 1, 4, 9], label="Sample Plot")
    ax_analyze.set_xlabel("X-axis Label")
    ax_analyze.set_ylabel("Y-axis Label")
    ax_analyze.legend()

    # Embed the plot in Tkinter
    canvas_analyze = FigureCanvasTkAgg(fig_analyze, master=plot_area)
    canvas_analyze.draw()
    canvas_analyze.get_tk_widget().pack(fill="both", expand=True)

    # Adding interactive toolbar for zoom and pan
    toolbar_analyze = NavigationToolbar2Tk(canvas_analyze, plot_frame_analyze)
    toolbar_analyze.update()
    toolbar_analyze.pack(side=tk.BOTTOM, fill=tk.X)

    # Footer label for showing the current image number
    image_label = tk.Label(plot_frame_analyze, text=f"Image {current_plot[0]} of {total_plots}", font=("Arial", 12))
    image_label.pack(side=tk.BOTTOM, pady=5)
