import tkinter as tk
from tkinter import ttk, filedialog
import openpyxl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import os
import threading

# Global variable for plot tab's output text
output_text = None

# Global variables for Matplotlib objects in Plot tab
fig = None
ax = None
canvas = None
selected_file = None


def plot_tab(tab_plot):
    global fig, ax, canvas, selected_file
    
    tab_plot.grid_rowconfigure(0, weight=1)
    tab_plot.grid_columnconfigure(0, weight=0, minsize=250)
    tab_plot.grid_columnconfigure(1, weight=1)

    container = tk.Frame(tab_plot, bg="lightgrey")
    container.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
    container.pack_propagate(False)

    notebook_plot = ttk.Notebook(container)
    notebook_plot.pack(fill="both", expand=True)

    create_data_setup_frame(notebook_plot)
    create_console_log_frame(notebook_plot)

    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
    create_controls_frame(notebook_plot, tab_plot)

    plot_frame_plot = tk.Frame(tab_plot)
    plot_frame_plot.grid(row=0, column=1, sticky="nswe")
    create_plot_frame(plot_frame_plot)


def create_console_log_frame(parent):
    global output_text

    frame_output = tk.LabelFrame(
        parent, text="Console Log", relief=tk.SUNKEN, borderwidth=2
    )
    frame_output.pack(fill="both", padx=10, pady=5, expand=True)

    output_text = tk.Text(frame_output, height=10, width=40, wrap="none", bg="white")
    scrollbar = tk.Scrollbar(
        frame_output, orient=tk.VERTICAL, command=output_text.yview, width=20
    )
    output_text.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


def create_controls_frame(parent, main_tk_root):
    global selected_file

    frame_controls = tk.LabelFrame(
        parent, text="Controls", relief=tk.SUNKEN, borderwidth=2
    )
    frame_controls.pack(fill="x", padx=10, pady=5)

    if 'selected_file' not in globals() or selected_file is None:
        selected_file = None

    def threaded_plot_task():
        global output_text, selected_file, fig, ax, canvas
        if selected_file:
            try:
                plot_data_internal(selected_file, fig, ax)
                main_tk_root.after(10, lambda: update_plot_canvas(canvas, output_text, selected_file))
            except Exception as e:
                main_tk_root.after(10, lambda: output_text.insert(tk.END, f"Error in plotting thread: {e}\n"))
                main_tk_root.after(10, lambda: output_text.see(tk.END))
        else:
            main_tk_root.after(10, lambda: output_text.insert(tk.END, "No file selected. Please select a file first.\n"))
            main_tk_root.after(10, lambda: output_text.see(tk.END))

    def update_plot_canvas(canvas_obj, log_widget, file_path):
        canvas_obj.draw()
        log_widget.insert(tk.END, f"Plotted data from {file_path} with DAC1 values.\n")
        log_widget.see(tk.END)

    def run_plot_button_handler():
        global selected_file, output_text
        if selected_file:
            output_text.insert(tk.END, f"Initiating plot from: {selected_file}...\n")
            output_text.see(tk.END)
            plot_thread = threading.Thread(target=threaded_plot_task)
            plot_thread.daemon = True
            plot_thread.start()
        else:
            output_text.insert(
                tk.END, "No file selected. Please select a file first.\n"
            )
            output_text.see(tk.END)

    run_button = tk.Button(frame_controls, text="Run", width=15, height=2, command=run_plot_button_handler)
    run_button.pack(padx=5, pady=10)



def create_data_setup_frame(parent):
    global selected_file, file_label

    frame_data_setup = tk.LabelFrame(
        parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2
    )
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    # Configure columns within frame_data_setup
    # Column 0: "Select File:" label - give it no weight (it takes minimum space)
    frame_data_setup.grid_columnconfigure(0, weight=0)
    # Column 1: "Browse" button - give it no weight
    frame_data_setup.grid_columnconfigure(1, weight=0)
    # Column 2: This column will exist implicitly when columnspan is used,

    frame_data_setup.grid_columnconfigure(1, weight=1) # Let column 1 take available space


    def select_file():
        global selected_file
        selected_file = filedialog.askopenfilename(
            initialdir="/home/pi/Desktop/Biosensor V2/data",
            title="Select an ISID Excel File",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")),
        )
        if selected_file:

            file_label.config(text=os.path.basename(selected_file))
            output_text.insert(tk.END, f"Selected file: {selected_file}\n")
            output_text.see(tk.END)

    tk.Label(frame_data_setup, text="Select File:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    select_file_button = tk.Button(frame_data_setup, text="Browse", width=8, height=1, command=select_file)
    select_file_button.grid(row=0, column=1, padx=5, pady=5)

    file_label = tk.Label(
        frame_data_setup,
        text="No file selected",
        height=1,
        anchor="w",
        justify="left",
        bg="lightgrey",
    )

    file_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)


def create_plot_frame(parent):
    global canvas, fig, ax

    plot_area_frame = tk.Frame(parent)
    plot_area_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = FigureCanvasTkAgg(fig, master=plot_area_frame)
    canvas_widget = canvas.get_tk_widget()

    toolbar = NavigationToolbar2Tk(canvas, plot_area_frame)
    toolbar.update()

    toolbar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    ax.set_xlabel("V2 (Sweep Voltage)")
    ax.set_ylabel("I4 (Current)")
    fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
    canvas.draw()


def plot_data_internal(file_path, fig_obj, ax_obj):
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook.active
    except Exception as e:
        raise e

    dac1_values = [
        cell.value for cell in sheet[5][1:] if cell.value is not None
    ]

    if not dac1_values:
        raise ValueError("No DAC1 values found in the file headers.")

    ax_obj.clear()
    colors = plt.cm.get_cmap("tab10", len(dac1_values) // 2)

    for idx in range(len(dac1_values) // 2):
        current_column_index = idx + 1

        v2_values = []
        i4_values = []

        for row_idx, row_data in enumerate(sheet.iter_rows(min_row=6, values_only=True)):
            if len(row_data) > current_column_index and \
               row_data[0] is not None and row_data[current_column_index] is not None:
                try:
                    v2_values.append(float(row_data[0]))
                    i4_values.append(float(row_data[current_column_index]))
                except (ValueError, TypeError) as e:
                    continue

        if v2_values and i4_values:
            label_val = dac1_values[idx]
            ax_obj.plot(v2_values, i4_values, label=f"DAC1 = {label_val}", color=colors(idx))

    filename = os.path.basename(file_path).upper()
    if "IG" in filename:
        ax_obj.set_xlabel("VG (Gate Voltage)")
    elif "ID" in filename:
        ax_obj.set_xlabel("VD (Drain Voltage)")
    else:
        ax_obj.set_xlabel("V2 (Sweep Voltage)")

    ax_obj.set_ylabel("I4 (Current)")
    ax_obj.legend(title="DAC1 Values")
    ax_obj.relim()
    ax_obj.autoscale_view()

    fig_obj.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)