import time
import datetime
import os
import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import ttk
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from . import ADS1256
from . import DAC8532

LED_PIN = 14
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

ADC = ADS1256.ADS1256()
DAC = DAC8532.DAC8532()
ADC.ADS1256_init()
DAC.DAC8532_Out_Voltage(0x30, 3)
DAC.DAC8532_Out_Voltage(0x34, 3)

collecting_data = False
voltages1, voltages2, voltages3 = [], [], []
currents4, currents5, currents6 = [], [], []


def collect_tab(tab_collect, root):
    left_frame_collect = tk.Frame(tab_collect, width=250, bg="lightgrey")
    left_frame_collect.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

    notebook_collect = ttk.Notebook(left_frame_collect)
    notebook_collect.pack(fill="both", expand=True)

    chip_name_entry, trial_name_entry = create_data_setup_frame(notebook_collect)
    params_entries = create_params_frame(notebook_collect)
    create_console_log_frame(notebook_collect)
    create_controls_frame(
        notebook_collect, chip_name_entry, trial_name_entry, params_entries, root
    )

    plot_frame_collect = tk.Frame(tab_collect, width=750)
    plot_frame_collect.pack(fill="both", expand=True, side=tk.RIGHT)

    create_plot_frame(plot_frame_collect)


def create_controls_frame(
    parent, chip_name_entry, trial_name_entry, params_entries, root
):
    frame_controls = tk.LabelFrame(
        parent, text="Controls", relief=tk.SUNKEN, borderwidth=2
    )
    frame_controls.pack(fill="x", padx=10, pady=5)

    def on_run():
        global collecting_data
        sweep_start = float(params_entries["sweep_min"].get())
        sweep_end = float(params_entries["sweep_max"].get())
        sweep_step = float(params_entries["sweep_step"].get())
        interval = float(params_entries["step_interval"].get())
        duration = (
            float(params_entries["duration"].get())
            if "duration" in params_entries
            else 120
        )

        dac1_voltage_values = [
            float(v.strip()) for v in params_entries["dac1_voltage"].get().split(",")
        ]

        collecting_data = True
        perform_data_collection(
            sweep_start,
            sweep_end,
            sweep_step,
            interval,
            duration,
            dac1_voltage_values,
            root,
        )

    def on_end():
        global collecting_data
        collecting_data = False

    def on_save():
        chip_name = chip_name_entry.get()
        trial_name = trial_name_entry.get()
        save_data(chip_name, trial_name)

    def on_reset():
        global voltages1, voltages2, voltages3, currents4, currents5, currents6
        voltages1, voltages2, voltages3 = [], [], []
        currents4, currents5, currents6 = [], [], []
        reset_plot()
        reset_parameters(params_entries)

    run_button = tk.Button(frame_controls, text="Run", width=15, command=on_run)
    run_button.grid(row=0, column=0, padx=5, pady=5)

    end_button = tk.Button(frame_controls, text="End", width=15, command=on_end)
    end_button.grid(row=0, column=1, padx=5, pady=5)

    save_button = tk.Button(frame_controls, text="Save", width=15, command=on_save)
    save_button.grid(row=1, column=0, padx=5, pady=5)

    reset_button = tk.Button(frame_controls, text="Reset", width=15, command=on_reset)
    reset_button.grid(row=1, column=1, padx=5, pady=5)


plot_colors = ["blue", "green", "red", "orange", "purple", "brown", "cyan", "magenta"]

data_by_dac1 = {}


def perform_data_collection(
    sweep_start, sweep_end, sweep_step, interval, duration, dac1_voltage_values, root
):
    global voltages1, voltages2, voltages3, currents4, currents5, currents6, data_by_dac1
    global collecting_data, current_voltage, steps_taken, dac_index

    data_by_dac1 = {
        v: {
            "voltages1": [],
            "voltages2": [],
            "voltages3": [],
            "currents4": [],
            "currents5": [],
            "currents6": [],
        }
        for v in dac1_voltage_values
    }

    number_of_steps = int((sweep_end - sweep_start) / sweep_step) + 1

    dac_index = 0

    def collect_data_for_dac1(dac1_voltage):
        global collecting_data, current_voltage, steps_taken

        current_voltage = sweep_start
        steps_taken = 0
        end_time = time.time() + duration

        while (
            collecting_data and steps_taken < number_of_steps and time.time() < end_time
        ):

            DAC.DAC8532_Out_Voltage(DAC8532.channel_B, dac1_voltage)
            DAC.DAC8532_Out_Voltage(DAC8532.channel_A, current_voltage)
            GPIO.output(LED_PIN, GPIO.HIGH)

            ADC_Value = ADC.ADS1256_GetAll()

            v1 = ADC_Value[1] * 5.0 / 0x7FFFFF
            v2 = ADC_Value[2] * 5.0 / 0x7FFFFF
            v3 = ADC_Value[3] * 5.0 / 0x7FFFFF

            shunt_voltage4 = ADC_Value[4] * 5.0 / 0x7FFFFF
            shunt_voltage5 = ADC_Value[5] * 5.0 / 0x7FFFFF
            shunt_voltage6 = ADC_Value[6] * 5.0 / 0x7FFFFF
            current4 = shunt_voltage4 / 10.0
            current5 = shunt_voltage5 / 10.0
            current6 = shunt_voltage6 / 10.0

            voltages1.append(v1)
            voltages2.append(v2)
            voltages3.append(v3)
            currents4.append(current4)
            currents5.append(current5)
            currents6.append(current6)

            data_by_dac1[dac1_voltage]["voltages1"].append(v1)
            data_by_dac1[dac1_voltage]["voltages2"].append(v2)
            data_by_dac1[dac1_voltage]["voltages3"].append(v3)
            data_by_dac1[dac1_voltage]["currents4"].append(current4)
            data_by_dac1[dac1_voltage]["currents5"].append(current5)
            data_by_dac1[dac1_voltage]["currents6"].append(current6)

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_plot(dac1_voltage)

            log_entry = (
                f"Time: {current_time}\n"
                f"V1: {v1:.5f} V, V2: {v2:.5f} V, V3: {v3:.5f} V\n"
                f"I4: {current4:.5f} A, I5: {current5:.5f} A, I6: {current6:.5f} A\n"
                "-----------------------------------------\n"
            )
            output_text.insert(tk.END, log_entry)
            output_text.see(tk.END)

            GPIO.output(LED_PIN, GPIO.LOW)

            current_voltage += sweep_step
            steps_taken += 1

            if collecting_data:
                root.after(int(interval * 1000), lambda: None)

        time.sleep(5)

    for dac1_voltage in dac1_voltage_values:
        if not collecting_data:
            break
        collect_data_for_dac1(dac1_voltage)

    collecting_data = False


def save_data(chip_name, trial_name):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Data Collection"

    worksheet.append(
        ["DAC1 Voltage", "V1 (V)", "V2 (V)", "V3 (V)", "I4 (A)", "I5 (A)", "I6 (A)"]
    )

    for dac1_voltage, data in data_by_dac1.items():
        for i in range(len(data["voltages1"])):
            worksheet.append(
                [
                    dac1_voltage,
                    data["voltages1"][i],
                    data["voltages2"][i],
                    data["voltages3"][i],
                    data["currents4"][i],
                    data["currents5"][i],
                    data["currents6"][i],
                ]
            )

    base_dir = "/home/pi/Desktop/Biosensor V2/data"
    chip_path = os.path.join(base_dir, chip_name)
    if not os.path.exists(chip_path):
        os.makedirs(chip_path)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    trial_folder_name = f"{trial_name} - {timestamp}"
    trial_path = os.path.join(chip_path, trial_folder_name)
    os.makedirs(trial_path, exist_ok=True)

    filename = os.path.join(trial_path, f"{trial_name}_{timestamp}.xlsx")
    workbook.save(filename)
    print(f"Data saved to {filename}")


def reset_plot():
    global ax, canvas
    ax.clear()
    ax.set_xlabel("V2 (Voltage)")
    ax.set_ylabel("I4 (Current)")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1)
    canvas.draw_idle()


def reset_parameters(params_entries):
    params_entries["duration"].delete(0, tk.END)
    params_entries["duration"].insert(0, "120")

    params_entries["sweep_min"].delete(0, tk.END)
    params_entries["sweep_min"].insert(0, "0.0")

    params_entries["sweep_max"].delete(0, tk.END)
    params_entries["sweep_max"].insert(0, "3.0")

    params_entries["sweep_step"].delete(0, tk.END)
    params_entries["sweep_step"].insert(0, "0.1")

    params_entries["step_interval"].delete(0, tk.END)
    params_entries["step_interval"].insert(0, "1")

    params_entries["dac1_voltage"].delete(0, tk.END)
    params_entries["dac1_voltage"].insert(0, "0.5")


def create_data_setup_frame(parent):
    frame_data_setup = tk.LabelFrame(
        parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2
    )
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    tk.Label(frame_data_setup, text="Chip Name:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    chip_name_entry = tk.Entry(frame_data_setup, width=20)
    chip_name_entry.grid(row=0, column=1, padx=5, pady=5)
    chip_name_entry.insert(0, "Default Chip")

    tk.Label(frame_data_setup, text="Trial Name:").grid(
        row=1, column=0, sticky="e", padx=5, pady=5
    )
    trial_name_entry = tk.Entry(frame_data_setup, width=20)
    trial_name_entry.grid(row=1, column=1, padx=5, pady=5)
    trial_name_entry.insert(0, "Trial 1")

    return chip_name_entry, trial_name_entry


def create_params_frame(parent):
    frame_params = tk.LabelFrame(
        parent, text="Parameters", relief=tk.SUNKEN, borderwidth=2
    )
    frame_params.pack(fill="x", padx=10, pady=10)

    params_entries = {}

    tk.Label(frame_params, text="Duration (s):").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    duration_entry = tk.Entry(frame_params, width=20)
    duration_entry.grid(row=0, column=1, columnspan=3, pady=5, sticky="w")
    duration_entry.insert(0, "120")
    params_entries["duration"] = duration_entry

    tk.Label(frame_params, text="Sweep Voltage (V):").grid(
        row=1, column=0, sticky="e", padx=5, pady=5
    )
    sweep_min_entry = tk.Entry(frame_params, width=8)
    sweep_min_entry.grid(row=1, column=1, padx=(0, 2), pady=5, sticky="w")
    sweep_min_entry.insert(0, "0.0")
    params_entries["sweep_min"] = sweep_min_entry
    tk.Label(frame_params, text="to").grid(row=1, column=2, padx=(2, 2), sticky="w")
    sweep_max_entry = tk.Entry(frame_params, width=8)
    sweep_max_entry.grid(row=1, column=3, padx=(2, 5), pady=5, sticky="w")
    sweep_max_entry.insert(0, "3.0")
    params_entries["sweep_max"] = sweep_max_entry

    tk.Label(frame_params, text="Step Voltage (V):").grid(
        row=2, column=0, sticky="e", padx=5, pady=5
    )
    sweep_step_entry = tk.Entry(frame_params, width=20)
    sweep_step_entry.grid(row=2, column=1, columnspan=3, pady=5, sticky="w")
    sweep_step_entry.insert(0, "0.1")
    params_entries["sweep_step"] = sweep_step_entry

    tk.Label(frame_params, text="Step Interval (s):").grid(
        row=3, column=0, sticky="e", padx=5, pady=5
    )
    step_interval_entry = tk.Entry(frame_params, width=20)
    step_interval_entry.grid(row=3, column=1, columnspan=3, pady=5, sticky="w")
    step_interval_entry.insert(0, "1")
    params_entries["step_interval"] = step_interval_entry

    tk.Label(frame_params, text="DAC1 Voltage (V):").grid(
        row=4, column=0, sticky="e", padx=5, pady=5
    )
    dac1_voltage_entry = tk.Entry(frame_params, width=20)
    dac1_voltage_entry.grid(row=4, column=1, columnspan=3, pady=5, sticky="w")
    dac1_voltage_entry.insert(0, "0.5")
    params_entries["dac1_voltage"] = dac1_voltage_entry

    return params_entries


def create_plot_frame(parent):
    global fig, ax, canvas

    fig, ax = plt.subplots()
    ax.set_xlabel("V2 (Voltage)")
    ax.set_ylabel("I4 (Current)")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1)
    ax.legend(["I4 vs V2"], loc="upper left")

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    toolbar = NavigationToolbar2Tk(canvas, parent)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)


def update_plot(dac1_voltage):
    global fig, ax, canvas, voltages1, voltages2, currents4, plot_colors, data_by_dac1

    ax.clear()

    for i, dac1 in enumerate(data_by_dac1):
        color = plot_colors[i % len(plot_colors)]
        ax.plot(
            data_by_dac1[dac1]["voltages2"],
            data_by_dac1[dac1]["currents4"],
            label=f"DAC1 = {dac1:.2f} V",
            color=color,
        )

    ax.set_xlabel("V2 (Voltage)")
    ax.set_ylabel("I4 (Current)")
    ax.legend(loc="upper left")
    ax.relim()
    ax.autoscale_view()

    canvas.draw_idle()


def create_console_log_frame(parent):
    frame_output = tk.LabelFrame(
        parent, text="Console Log", relief=tk.SUNKEN, borderwidth=2
    )
    frame_output.pack(fill="both", padx=10, pady=0, expand=True)

    global output_text
    output_text = tk.Text(frame_output, height=3, width=40, wrap="none", bg="white")
    scrollbar = tk.Scrollbar(
        frame_output, orient=tk.VERTICAL, command=output_text.yview
    )
    output_text.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    return output_text
