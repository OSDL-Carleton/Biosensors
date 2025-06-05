import tkinter as tk
from tkinter import ttk, filedialog
import openpyxl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import os


def plot_tab(tab_plot):
    left_frame_plot = tk.Frame(tab_plot, width=250, bg="lightgrey")
    left_frame_plot.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

    notebook_plot = ttk.Notebook(left_frame_plot)
    notebook_plot.pack(fill="both", expand=True)

    create_data_setup_frame(notebook_plot)
    create_console_log_frame(notebook_plot)
    create_controls_frame(notebook_plot)

    plot_frame_plot = tk.Frame(tab_plot)
    plot_frame_plot.pack(fill="both", expand=True, side=tk.RIGHT)
    create_plot_frame(plot_frame_plot)


def create_console_log_frame(parent):
    global output_text

    frame_output = tk.LabelFrame(
        parent, text="Console Log", relief=tk.SUNKEN, borderwidth=2
    )
    frame_output.pack(fill="both", padx=10, pady=5, expand=True)

    output_text = tk.Text(frame_output, height=10, width=40, wrap="none", bg="white")
    scrollbar = tk.Scrollbar(
        frame_output, orient=tk.VERTICAL, command=output_text.yview
    )
    output_text.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


def create_controls_frame(parent):
    global selected_file

    frame_controls = tk.LabelFrame(
        parent, text="Controls", relief=tk.SUNKEN, borderwidth=2
    )
    frame_controls.pack(fill="x", padx=10, pady=5)

    selected_file = None

    def run_plot():
        if selected_file:
            output_text.insert(tk.END, f"Plotting data from: {selected_file}\n")
            output_text.see(tk.END)
            plot_from_file(selected_file)
        else:
            output_text.insert(
                tk.END, "No file selected. Please select a file first.\n"
            )
            output_text.see(tk.END)

    run_button = tk.Button(frame_controls, text="Run", width=15, height=2, command=run_plot)
    run_button.pack(padx=5, pady=10)


def create_data_setup_frame(parent):
    global selected_file, file_label

    frame_data_setup = tk.LabelFrame(
        parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2
    )
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    def select_file():
        global selected_file
        selected_file = filedialog.askopenfilename(
            initialdir="/home/pi/Desktop/Biosensor V2/data",
            title="Select an ISID Excel File",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")),
        )
        if selected_file:
            file_label.config(text=selected_file)
            output_text.insert(tk.END, f"Selected file: {selected_file}\n")
            output_text.see(tk.END)

    tk.Label(frame_data_setup, text="Select File:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    select_file_button = tk.Button(frame_data_setup, text="Browse", width=15 ,height=2, command=select_file)
    select_file_button.grid(row=0, column=1, padx=5, pady=5)

    file_label = tk.Label(
        frame_data_setup,
        text="No file selected",
        wraplength=200,
        anchor="w",
        justify="left",
        bg="lightgrey",
    )
    file_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)


def create_plot_frame(parent):
    global fig, ax, canvas

    plot_container = tk.Frame(parent)
    plot_container.pack(fill="both", expand=True, padx=10, pady=10)

    fig, ax = plt.subplots()
    ax.set_xlabel("V2 (Sweep Voltage)")
    ax.set_ylabel("I4 (Current)")
    canvas = FigureCanvasTkAgg(fig, master=plot_container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    toolbar = NavigationToolbar2Tk(canvas, plot_container)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)


def plot_from_file(file_path):
    global ax, canvas, output_text

    workbook = openpyxl.load_workbook(file_path, data_only=True)
    sheet = workbook.active

    dac1_values = [cell.value for cell in sheet[5][1:]]
    v2_values = []

    if not dac1_values:
        output_text.insert(tk.END, "No DAC1 values found in the file headers.\n")
        output_text.see(tk.END)
        return

    ax.clear()
    colors = plt.cm.get_cmap("tab10", len(dac1_values))

    for idx, dac1_value in enumerate(dac1_values[: len(dac1_values) // 2]):
        current_column = idx + 1

        v2_values = []
        i4_values = []

        for row in sheet.iter_rows(min_row=6, values_only=True):
            if row[0] is not None and row[current_column] is not None:
                v2_values.append(row[0])
                i4_values.append(row[current_column])

        ax.plot(v2_values, i4_values, label=f"DAC1 = {dac1_value}", color=colors(idx))

    # Sweep voltage label
    filename = os.path.basename(file_path).upper()
    if "IG" in filename:
        ax.set_xlabel("VG (Gate Voltage)")
    elif "ID" in filename:
        ax.set_xlabel("VD (Drain Voltage)")
    else:
        ax.set_xlabel("V2 (Sweep Voltage)")

    ax.set_ylabel("I4 (Current)")
    ax.legend(title="DAC1 Values")
    ax.relim()
    ax.autoscale_view()
    canvas.draw_idle()

    output_text.insert(tk.END, f"Plotted data from {file_path} with DAC1 values.\n")
    output_text.see(tk.END)
