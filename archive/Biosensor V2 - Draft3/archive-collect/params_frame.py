import tkinter as tk

def create_params_frame(parent):
    frame_params = tk.LabelFrame(parent, text="Parameters", relief=tk.SUNKEN, borderwidth=2)
    frame_params.pack(fill="x", padx=10, pady=10)

    entry_width = 20

    tk.Label(frame_params, text="Time limit (sec):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    time_limit_entry = tk.Entry(frame_params, width=entry_width)
    time_limit_entry.grid(row=0, column=1, columnspan=3, pady=5, sticky="w")
    time_limit_entry.insert(0, "120")

    tk.Label(frame_params, text="Sweep Voltage (V):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    sweep_min_entry = tk.Entry(frame_params, width=8)
    sweep_min_entry.grid(row=1, column=1, padx=(0, 2), pady=5, sticky="w")
    sweep_min_entry.insert(0, "0.0")
    tk.Label(frame_params, text="to").grid(row=1, column=2, padx=(2, 2), sticky="w")
    sweep_max_entry = tk.Entry(frame_params, width=8)
    sweep_max_entry.grid(row=1, column=3, padx=(2, 5), pady=5, sticky="w")
    sweep_max_entry.insert(0, "5.0")

    tk.Label(frame_params, text="Sweep Step Voltage (V):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    sweep_step_voltage_entry = tk.Entry(frame_params, width=entry_width)
    sweep_step_voltage_entry.grid(row=2, column=1, columnspan=3, pady=5, sticky="w")
    sweep_step_voltage_entry.insert(0, "0.1")

    tk.Label(frame_params, text="Step Interval (s):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    step_interval_entry = tk.Entry(frame_params, width=entry_width)
    step_interval_entry.grid(row=3, column=1, columnspan=3, pady=5, sticky="w")
    step_interval_entry.insert(0, "1")

    tk.Label(frame_params, text="DAC1 Voltage (V):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    dac1_voltage_entry = tk.Entry(frame_params, width=entry_width)
    dac1_voltage_entry.grid(row=4, column=1, columnspan=3, pady=5, sticky="w")
    dac1_voltage_entry.insert(0, "0.5")
