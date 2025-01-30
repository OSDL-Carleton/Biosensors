import os
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


chip_files = {
    "5WT1": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT2": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT3": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT4": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT5": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT6": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT7": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
}


def analyze_tab(tab_analyze):
    folder_path = tk.StringVar()
    average_isd_values = {}
    current_plot = [1]

    left_frame_analyze = tk.Frame(tab_analyze, width=250, bg="lightgrey")
    left_frame_analyze.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

    notebook_analyze = ttk.Notebook(left_frame_analyze)
    notebook_analyze.pack(fill="both", expand=True)

    create_data_setup_frame(notebook_analyze, folder_path)
    output_text = create_console_log_frame(notebook_analyze)

    plot_frame_analyze = tk.Frame(tab_analyze, width=750)
    plot_frame_analyze.pack(fill="both", expand=True, side=tk.RIGHT)
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame_analyze)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    toolbar = NavigationToolbar2Tk(canvas, plot_frame_analyze)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    prev_button = tk.Button(
        plot_frame_analyze,
        text="◀",
        command=lambda: switch_plot(
            "previous", current_plot, average_isd_values, ax, canvas
        ),
    )
    next_button = tk.Button(
        plot_frame_analyze,
        text="▶",
        command=lambda: switch_plot(
            "next", current_plot, average_isd_values, ax, canvas
        ),
    )
    prev_button.pack(side=tk.LEFT, padx=5, pady=5)
    next_button.pack(side=tk.RIGHT, padx=5, pady=5)

    create_controls_frame(
        notebook_analyze, folder_path, average_isd_values, output_text, ax, canvas
    )


def create_data_setup_frame(parent, folder_path):
    frame_data_setup = tk.LabelFrame(
        parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2
    )
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    def select_folder():
        selected_folder = filedialog.askdirectory(
            title="Select a Folder", initialdir="/home/pi/Desktop/Biosensor V2/data"
        )
        if selected_folder:
            folder_path.set(selected_folder)

    tk.Label(frame_data_setup, text="Select Folder:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    select_folder_button = tk.Button(
        frame_data_setup, text="Browse", command=select_folder
    )
    select_folder_button.grid(row=0, column=1, padx=5, pady=5)

    folder_label = tk.Label(
        frame_data_setup,
        textvariable=folder_path,
        wraplength=200,
        anchor="w",
        justify="left",
        bg="lightgrey",
    )
    folder_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)


def create_console_log_frame(parent):
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

    return output_text


def create_controls_frame(parent, folder_path, avg_isd_dict, log_widget, ax, canvas):
    frame_controls = tk.LabelFrame(
        parent, text="Controls", relief=tk.SUNKEN, borderwidth=2
    )
    frame_controls.pack(fill="x", padx=10, pady=5)

    run_button = tk.Button(
        frame_controls,
        text="Run Analysis",
        width=15,
        command=lambda: run_analysis(
            folder_path.get(), avg_isd_dict, log_widget, ax, canvas
        ),
    )
    run_button.pack(padx=5, pady=10)


def run_analysis(folder, avg_isd_dict, log_widget, ax, canvas):
    if not folder:
        log_widget.insert(tk.END, "Please select a folder first!\n")
        return

    avg_isd_dict.clear()
    for tool, files in chip_files.items():
        vd_vals, vgs_vals, avg_isd = compute_average_isd(folder, tool, files)
        if avg_isd is not None:
            avg_isd_dict[tool] = (vd_vals, vgs_vals, avg_isd)
            log_widget.insert(tk.END, f"Processed {tool} with {len(files)} files.\n")
        else:
            log_widget.insert(tk.END, f"Error processing {tool}.\n")

    log_widget.insert(tk.END, "Analysis complete.\n")
    log_widget.see(tk.END)
    plot_part1(avg_isd_dict, ax, canvas)


def switch_plot(direction, current_plot, avg_isd_values, ax, canvas):
    if direction == "previous":
        current_plot[0] = 2 if current_plot[0] == 1 else current_plot[0] - 1
    elif direction == "next":
        current_plot[0] = 1 if current_plot[0] == 2 else current_plot[0] + 1

    if current_plot[0] == 1:
        plot_part1(avg_isd_values, ax, canvas)
    elif current_plot[0] == 2:
        plot_part2(avg_isd_values, ax, canvas)


def plot_part1(avg_isd_values, ax, canvas):
    if "5WT1" not in avg_isd_values:
        return
    vd_values = avg_isd_values["5WT1"][0]
    ax.clear()
    for tool, (_, _, avg_isd) in avg_isd_values.items():
        mean_isd_vals = avg_isd.mean(axis=1).tolist()
        ax.plot(vd_values, mean_isd_vals, label=f"Average Isd for {tool}")
    ax.set_xlabel("Vd (V)")
    ax.set_ylabel("Average Isd (A)")
    ax.legend()
    ax.grid(True)
    ax.set_title("Part 1: Isd vs Vd")
    canvas.draw()


def plot_part2(avg_isd_values, ax, canvas):
    target_vd_values = [
        0.0,
        -0.1,
        -0.2,
        -0.3,
        -0.4,
        -0.5,
        -0.6,
        -0.7,
        -0.8,
        -0.9,
        -1.0,
        -1.1,
        -1.2,
        -1.3,
        -1.4,
        -1.5,
        -1.6,
        -1.7,
        -1.8,
        -1.9,
        -2.0,
        -2.1,
        -2.2,
        -2.3,
        -2.4,
        -2.5,
        -2.6,
        -2.7,
        -2.8,
        -2.9,
        -3.0,
        -3.1,
        -3.2,
        -3.3,
        -3.4,
        -3.5,
    ]
    filtered_avg_isd_values = format_filtered_average_isd_abs(
        avg_isd_values, target_vd_values
    )

    x_values = [
        0,
        0.4,
        0.8,
        1.2,
        1.6,
        2.0,
        2.4,
        2.8,
    ]
    ax.clear()
    for vd_value, isd_values in filtered_avg_isd_values.items():
        ax.plot(x_values, isd_values, label=f"Vd = {vd_value}")

    ax.set_xlabel("VSG (V)")
    ax.set_ylabel("Isd (A)")
    ax.legend(
        title="Vd values", loc="upper right", bbox_to_anchor=(1.05, 1), borderaxespad=0
    )
    ax.grid(True)
    ax.set_title("Part 2: Isd vs VSG")
    canvas.draw()


def compute_average_isd(folder, tool, files):
    combined_isd = None
    vgs_values = None
    vd_values = None
    for file_name in files:
        file_path = os.path.join(folder, tool, file_name)
        if os.path.exists(file_path):
            vd_vals, vgs_vals, _, _, isd_values = extract_values(file_path)
            if isd_values is not None:
                if combined_isd is None:
                    combined_isd = isd_values
                    vgs_values = vgs_vals
                    vd_values = vd_vals
                else:
                    combined_isd = combined_isd.add(isd_values, fill_value=0)
        else:
            print(f"File not found: {file_path}")
    if combined_isd is not None:
        return vd_values, vgs_values, combined_isd / len(files)
    return None, None, None


def extract_values(file_path):
    try:
        df = pd.read_csv(file_path, header=None)
        vgs_values = df.iloc[4, 1:9].tolist()
        df = pd.read_csv(file_path, skiprows=4)
        vd_values = df.iloc[:, 0].tolist()
        is_values = df.iloc[:, 1:9]
        id_values = df.iloc[:, 9:17]
        isd_values = id_values.subtract(is_values.values)
        return vd_values, vgs_values, is_values, id_values, isd_values
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None, None, None, None


def format_filtered_average_isd_abs(average_isd_values, target_vd_values):
    vgs_list = average_isd_values[list(average_isd_values.keys())[0]][1]
    formatted_dict = {}
    total_avg_isd = {vgs: [] for vgs in vgs_list}

    for vgs_idx, vgs in enumerate(vgs_list):
        combined_isd = []
        for tool, (vd_values, _, avg_isd) in average_isd_values.items():
            filtered_isd_vals_for_vgs = [
                avg_isd.iloc[i, vgs_idx]
                for i, vd in enumerate(vd_values)
                if vd in target_vd_values
            ]
            combined_isd.append(filtered_isd_vals_for_vgs)
        combined_isd = [
            np.array(isd_vals) for isd_vals in combined_isd if len(isd_vals) > 0
        ]
        if len(combined_isd) > 0:
            combined_isd_array = np.vstack(combined_isd)
            avg_isd_for_vgs = np.mean(combined_isd_array, axis=0)
            total_avg_isd[vgs] = avg_isd_for_vgs

    for i, vd in enumerate(target_vd_values):
        filtered_values = []
        for vgs in vgs_list:
            if i < len(total_avg_isd[vgs]):
                filtered_values.append(total_avg_isd[vgs][i])
            else:
                filtered_values.append(None)
        formatted_dict[abs(vd)] = filtered_values
    return formatted_dict
