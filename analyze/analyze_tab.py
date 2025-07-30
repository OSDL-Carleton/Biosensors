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
    # folder_path is now specifically for the selected directory for processing
    folder_path = tk.StringVar()
    # selected_folder_display will be for showing the folder name in the UI
    selected_folder_display = tk.StringVar(value="No file selected")

    average_isd_values = {}
    current_plot = [1]

    tab_analyze.grid_rowconfigure(0, weight=1)
    tab_analyze.grid_columnconfigure(0, weight=0, minsize=250)
    tab_analyze.grid_columnconfigure(1, weight=1)

    left_frame_analyze = tk.Frame(tab_analyze, bg="lightgrey")
    left_frame_analyze.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
    left_frame_analyze.pack_propagate(False)

    notebook_analyze = ttk.Notebook(left_frame_analyze)
    notebook_analyze.pack(fill="both", expand=True)

    # Pass selected_folder_display to create_data_setup_frame for Analyze tab
    create_data_setup_frame(notebook_analyze, folder_path, selected_folder_display)
    output_text = create_console_log_frame(notebook_analyze)

    plot_frame_analyze = tk.Frame(tab_analyze)
    plot_frame_analyze.grid(row=0, column=1, sticky="nswe")

    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15) # Default adjustments
    canvas = FigureCanvasTkAgg(fig, master=plot_frame_analyze)
    canvas_widget = canvas.get_tk_widget()
    toolbar = NavigationToolbar2Tk(canvas, plot_frame_analyze)
    toolbar.update()

    toolbar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    canvas.draw()

    # Pass fig, ax, canvas to controls frame for Analyze tab
    create_controls_frame(
        notebook_analyze, folder_path, average_isd_values, output_text, ax, canvas, fig
    )

    button_frame = tk.Frame(plot_frame_analyze)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False, pady=5)

    prev_button = tk.Button(
        button_frame,
        text="◀",
        command=lambda: switch_plot(
            "previous", current_plot, average_isd_values, ax, canvas, fig
        ),
    )
    next_button = tk.Button(
        button_frame,
        text="▶",
        command=lambda: switch_plot(
            "next", current_plot, average_isd_values, ax, canvas, fig
        ),
    )
    prev_button.pack(side=tk.LEFT, padx=5)
    next_button.pack(side=tk.RIGHT, padx=5)


# Modified create_data_setup_frame for Analyze tab
def create_data_setup_frame(parent, folder_path_var, selected_folder_display_var):
    frame_data_setup = tk.LabelFrame(
        parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2
    )
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    def select_folder():
        selected_folder = filedialog.askdirectory(
            title="Select a Folder", initialdir="/home/pi/Desktop/Biosensor V2/data"
        )
        if selected_folder:
            folder_path_var.set(selected_folder)
            # Display only the base name of the folder, but use the full path for processing
            selected_folder_display_var.set(os.path.basename(selected_folder))
            output_text_analyze.insert(tk.END, f"Selected folder: {selected_folder}\n")
            output_text_analyze.see(tk.END)

    tk.Label(frame_data_setup, text="Select Folder:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    select_folder_button = tk.Button(
        frame_data_setup, text="Browse", width=8, height=1, command=select_folder # Shrunk button
    )
    select_folder_button.grid(row=0, column=1, padx=5, pady=5)

    # Label to display the selected folder path
    folder_display_label = tk.Label(
        frame_data_setup,
        textvariable=selected_folder_display_var, # Use the StringVar
        wraplength=200,
        anchor="w",
        justify="left",
        bg="lightgrey",
    )
    folder_display_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

# Global variable for analyze tab's output text for logging
output_text_analyze = None

def create_console_log_frame(parent):
    global output_text_analyze # Use the global variable for analyze tab

    frame_output = tk.LabelFrame(
        parent, text="Console Log", relief=tk.SUNKEN, borderwidth=2
    )
    frame_output.pack(fill="both", padx=10, pady=5, expand=True)

    output_text_analyze = tk.Text(frame_output, height=10, width=40, wrap="none", bg="white")
    scrollbar = tk.Scrollbar(
        frame_output, orient=tk.VERTICAL, command=output_text_analyze.yview, width=20
    )
    output_text_analyze.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text_analyze.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    return output_text_analyze


# Modified create_controls_frame for Analyze tab
def create_controls_frame(parent, folder_path, avg_isd_dict, log_widget, ax, canvas, fig):
    frame_controls = tk.LabelFrame(
        parent, text="Controls", relief=tk.SUNKEN, borderwidth=2
    )
    frame_controls.pack(fill="x", padx=10, pady=5)

    run_button = tk.Button(
        frame_controls,
        text="Run",
        width=15, # Set width to 15
        height=2, # Set height to 2
        command=lambda: run_analysis(
            folder_path.get(), avg_isd_dict, log_widget, ax, canvas, fig
        ),
    )
    run_button.pack(padx=5, pady=10)


def run_analysis(folder, avg_isd_dict, log_widget, ax, canvas, fig):
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
    plot_part1(avg_isd_dict, ax, canvas, fig)


def switch_plot(direction, current_plot, avg_isd_values, ax, canvas, fig):
    if direction == "previous":
        current_plot[0] = max(1, current_plot[0] - 1)
    elif direction == "next":
        current_plot[0] = min(2, current_plot[0] + 1)

    if current_plot[0] == 1:
        plot_part1(avg_isd_values, ax, canvas, fig)
    elif current_plot[0] == 2:
        plot_part2(avg_isd_values, ax, canvas, fig)


def plot_part1(avg_isd_values, ax, canvas, fig):
    if "5WT1" not in avg_isd_values:
        ax.clear()
        ax.set_title("No Data for Part 1 Plot")
        canvas.draw_idle()
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

    fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)

    canvas.draw_idle()


def plot_part2(avg_isd_values, ax, canvas, fig):
    if not avg_isd_values:
        ax.clear()
        ax.set_title("No Data for Part 2 Plot")
        canvas.draw_idle()
        return

    target_vd_values = [
        0.0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9,
        -1.0, -1.1, -1.2, -1.3, -1.4, -1.5, -1.6, -1.7, -1.8, -1.9,
        -2.0, -2.1, -2.2, -2.3, -2.4, -2.5, -2.6, -2.7, -2.8, -2.9,
        -3.0, -3.1, -3.2, -3.3, -3.4, -3.5,
    ]
    filtered_avg_isd_values = format_filtered_average_isd_abs(
        avg_isd_values, target_vd_values
    )

    x_values = [
        0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8,
    ]
    ax.clear()
    for vd_value, isd_values in filtered_avg_isd_values.items():
        plottable_isd_values = [val for val in isd_values if val is not None]
        plottable_x_values = x_values[:len(plottable_isd_values)]

        if plottable_isd_values:
            ax.plot(plottable_x_values, plottable_isd_values, label=f"Vd = {vd_value}")

    ax.set_xlabel("VSG (V)")
    ax.set_ylabel("Isd (A)")
    ax.legend(
        title="Vd values", loc="upper right", bbox_to_anchor=(1.05, 1), borderaxespad=0
    )
    ax.grid(True)
    ax.set_title("Part 2: Isd vs VSG")

    fig.subplots_adjust(left=0.15, right=0.8, top=0.9, bottom=0.15)

    canvas.draw_idle()


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
                print(f"Failed to extract values from {file_path}")
        else:
            print(f"File not found: {file_path}")
    if combined_isd is not None and len(files) > 0:
        return vd_values, vgs_values, combined_isd / len(files)
    return None, None, None


def extract_values(file_path):
    try:
        vgs_df = pd.read_csv(file_path, header=None, nrows=5)
        vgs_values = [val for val in vgs_df.iloc[4, 1:9].tolist() if pd.notna(val)]

        df = pd.read_csv(file_path, skiprows=5, header=None)

        vd_values = df.iloc[:, 0].tolist()
        is_values = df.iloc[:, 1:9]
        id_values = df.iloc[:, 9:17]

        isd_values = id_values.subtract(is_values.values)

        return vd_values, vgs_values, is_values, id_values, isd_values
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None, None, None, None


def format_filtered_average_isd_abs(average_isd_values, target_vd_values):
    if not average_isd_values:
        return {}

    first_tool_key = list(average_isd_values.keys())[0]
    vgs_list = average_isd_values[first_tool_key][1]

    total_avg_isd_per_vgs = {vgs: [] for vgs in vgs_list}

    for tool, (vd_values_tool, vgs_values_tool, avg_isd_df_tool) in average_isd_values.items():
        for vgs_idx, vgs in enumerate(vgs_list):
            if vgs_idx < avg_isd_df_tool.shape[1]:
                temp_series = pd.Series(avg_isd_df_tool.iloc[:, vgs_idx].values, index=vd_values_tool)

                filtered_isd_vals_for_vgs = temp_series.loc[temp_series.index.isin(target_vd_values)].tolist()

                total_avg_isd_per_vgs[vgs].append(filtered_isd_vals_for_vgs)

    formatted_dict = {}
    for i, vd_target in enumerate(target_vd_values):
        filtered_values_for_vd_target = []
        for vgs in vgs_list:
            isd_at_current_vd = []
            for tool_data_list in total_avg_isd_per_vgs[vgs]:
                if i < len(tool_data_list):
                    isd_at_current_vd.append(tool_data_list[i])

            if isd_at_current_vd:
                filtered_values_for_vd_target.append(np.mean(isd_at_current_vd))
            else:
                filtered_values_for_vd_target.append(None)

        formatted_dict[abs(vd_target)] = filtered_values_for_vd_target
    return formatted_dict

