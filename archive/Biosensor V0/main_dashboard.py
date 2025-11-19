import time
import RPi.GPIO as GPIO
import ADS1256
import DAC8532
import tkinter as tk
from tkinter import ttk
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gui_styles
import datetime

# GPIO setup
LED_PIN = 14
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# GUI Setup
root = tk.Tk()
root.title("Raspberry Pi Dashboard")
root.configure(bg='white')
gui_styles.apply_styles()

# Setup DAC and ADC
ADC = ADS1256.ADS1256()
DAC = DAC8532.DAC8532()
ADC.ADS1256_init()

DAC.DAC8532_Out_Voltage(0x30, 3)
DAC.DAC8532_Out_Voltage(0x34, 3)

collecting_data = False

# Global duration in seconds (default to None)
duration = None

# Cleanup operations
def close_program():
    GPIO.cleanup()
    root.destroy()
    print ("\r\nProgram end")
    exit()

# Global Variables
all_datasets = []
times = []
voltages1 = []
voltages2 = []
voltages3 = []
currents4 = []
currents5 = []
currents6 = []
line = None
line2 = None

start_time = None
current_step = 0

# Add these global variables near the other global declarations
sweep_start_voltage = 0.0
sweep_end_voltage = 5.0
sweep_step_voltage = 0.1
steps_taken = 0
current_sweep_voltage = sweep_start_voltage

# Set all duration buttons to default state and the selected one to the highlighted state.
def toggle_duration_button_state(button=None):
    short_btn.configure(style='TButton')
    medium_btn.configure(style='TButton')
    long_btn.configure(style='TButton')

    if button:
        button.configure(style='Selected.TButton')

# Set the global duration based on the button pressed.
def set_duration(value):
    global duration
    if value == "short":
        duration = 60
        toggle_duration_button_state(short_btn)
    elif value == "medium":
        duration = 180
        toggle_duration_button_state(medium_btn)
    elif value == "long":
        duration = 360
        toggle_duration_button_state(long_btn)

# Setup openpyxl workbook and worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet.title = "Data Collection"
worksheet.append(['Time', 'V1 (V)', 'V2 (V)', 'V3 (V)', 'I4 (A)', 'I5 (A)', 'I6 (A)'])

# Your matplotlib setup for the graph might look like this now
fig, ax = plt.subplots(figsize=(5, 4))
ax.set_xlabel('Voltage (V)')
ax.set_ylabel('Current (A)')
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)
line, = ax.plot([], [], 'r-', label='Y1-axis')  # Primary Y-axis line in red
line2, = ax.plot([], [], 'b-', label='Y2-axis')  # Secondary Y2-axis line in blue

# Define a mapping from combobox values to dataset keys
axis_key_mapping = {
    'V1 (V)': 'voltages1',
    'V2 (V)': 'voltages2',
    'V3 (V)': 'voltages3',
    'I4 (A)': 'currents4',
    'I5 (A)': 'currents5',
    'I6 (A)': 'currents6',
}

# Dynamic Graph being displayed
def update_graph():
    global all_datasets, ax, canvas, x_axis_combobox, y_axis_combobox, y2_axis_combobox

    # Clear the axes for the new plot
    ax.clear()

    # Get the selected channels for the axes from the comboboxes
    x_axis_selection = axis_key_mapping[x_axis_combobox.get()]
    y_axis_selection = axis_key_mapping[y_axis_combobox.get()]
    y2_axis_selection = axis_key_mapping[y2_axis_combobox.get()]

    # Iterate over each dataset and plot it
    for i, dataset in enumerate(all_datasets):
        x_data = dataset[x_axis_selection]  # Data for X-axis
        y_data = dataset[y_axis_selection]  # Data for Y1-axis
        y2_data = dataset[y2_axis_selection]  # Data for Y2-axis

        # Plot each dataset with a unique label
        ax.plot(x_data, y_data, label=f'{y_axis_combobox.get()} Run {i+1}')
        ax.plot(x_data, y2_data, label=f'{y2_axis_combobox.get()} Run {i+1}', linestyle='--')

    # Update labels and axis limits
    ax.set_xlabel(x_axis_combobox.get())
    ax.set_ylabel(f"{y_axis_combobox.get()} / {y2_axis_combobox.get()}")
    ax.legend()
    ax.relim()
    ax.autoscale_view()

    # Redraw the canvas
    canvas.draw_idle()
    fig.tight_layout()
    canvas.draw()

    
# Read and display data
def collect_data():
    global collecting_data, steps_taken, number_of_steps
    global current_step, current_sweep_voltage, sweep_step_voltage
    global all_datasets  # Include the global reference to all_datasets

    if collecting_data and steps_taken < number_of_steps:
        # Get the current dataset
        current_dataset = all_datasets[-1]

        # Set the current voltage on DAC0
        DAC.DAC8532_Out_Voltage(DAC8532.channel_A, current_sweep_voltage)
            
        GPIO.output(LED_PIN, GPIO.HIGH)
     
        ADC_Value = ADC.ADS1256_GetAll()

        voltage1 = ADC_Value[1]*5.0/0x7fffff
        voltage2 = ADC_Value[2]*5.0/0x7fffff
        voltage3 = ADC_Value[3]*5.0/0x7fffff
        
        shunt_voltage4 = ADC_Value[4]*5.0/0x7fffff
        shunt_voltage5 = ADC_Value[5]*5.0/0x7fffff
        shunt_voltage6 = ADC_Value[6]*5.0/0x7fffff
        
        shunt_resistor = 10
        
        current4 = shunt_voltage4 / shunt_resistor
        current5 = shunt_voltage5 / shunt_resistor
        current6 = shunt_voltage6 / shunt_resistor

        GPIO.output(LED_PIN, GPIO.LOW)

        voltage1_label.config(text=f"Voltage from probe 1: {voltage1:.5f} V")
        voltage2_label.config(text=f"Voltage from probe 2: {voltage2:.5f} V")
        voltage3_label.config(text=f"Voltage from probe 3: {voltage3:.5f} V")
        
        current4_label.config(text=f"Current from probe 4: {current4:.5f} A")
        current5_label.config(text=f"Current from probe 5: {current5:.5f} A")
        current6_label.config(text=f"Current from probe 6: {current6:.5f} A")

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        # Append data to the current dataset instead of global lists
        current_dataset["times"].append(current_time)
        current_dataset["voltages1"].append(voltage1)
        current_dataset["voltages2"].append(voltage2)
        current_dataset["voltages3"].append(voltage3)
        current_dataset["currents4"].append(current4)
        current_dataset["currents5"].append(current5)
        current_dataset["currents6"].append(current6)

        update_graph()

        current_step += 1

        # Increment the steps taken
        steps_taken += 1

        # Increment the sweep voltage
        current_sweep_voltage += sweep_step_voltage
        if steps_taken >= number_of_steps:
            stop_data_collection()
            return
        
        # Continue data collection after the interval
        root.after(int(float(step_entry.get())) * 1000, collect_data)
    else:
        # If we've reached the number of steps or collecting_data is False, stop the collection
        stop_data_collection()

# Starting the data collection
def start_data_collection():
    global all_datasets, collecting_data, start_time, current_step, current_sweep_voltage
    global sweep_start_voltage, sweep_end_voltage, sweep_step_voltage, number_of_steps

    
    # Read DAC1 voltage from the entry and set it
    dac1_voltage = float(dac1_voltage_entry.get())
    DAC.DAC8532_Out_Voltage(DAC8532.channel_B, dac1_voltage)
    
    # Set the sweep parameters from the user inputs
    sweep_start_voltage = float(sweep_start_entry.get())
    sweep_end_voltage = float(sweep_end_entry.get())
    sweep_step_voltage = float(sweep_step_voltage_entry.get())
    
    # Calculate the number of steps
    number_of_steps = int((sweep_end_voltage - sweep_start_voltage) / sweep_step_voltage) + 1
     
    
    new_dataset = {
        "times": [],
        "voltages1": [],
        "voltages2": [],
        "voltages3": [],
        "currents4": [],
        "currents5": [],
        "currents6": [],
    }
    all_datasets.append(new_dataset)

    collecting_data = True
    start_time = time.time()
    current_step = 0
    current_sweep_voltage = sweep_start_voltage
    
    DAC.DAC8532_Out_Voltage(DAC8532.channel_A, current_sweep_voltage)
    collect_data()
    toggle_button_state(collect_btn)


# Set all buttons to default state, then when pressed
def toggle_button_state(button):
    collect_btn.configure(style='TButton')
    stop_btn.configure(style='TButton')
    if button:
        button.configure(style='Selected.TButton')

# Stop the data collection
def stop_data_collection():
    global collecting_data
    collecting_data = False
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'data_collection_{timestamp}.xlsx'
    workbook.save(filename)
    toggle_button_state(stop_btn)
    
# Reset the module to another run
def reset_data_collection():
    global all_datasets, times, voltages1, voltages2, voltages3, currents4, currents5, currents6, current_step, start_time
    global line, line2  # Add these if they're not already global

    # Clear the data lists
    all_datasets.clear()
    times.clear()
    ax.clear()
    voltages1.clear()
    voltages2.clear()
    voltages3.clear()
    currents4.clear()
    currents5.clear()
    currents6.clear()

    # Reset the plot lines
    line.set_data([], [])
    line2.set_data([], [])

    # Reset the step counters
    current_step = 0
    steps_taken = 0  # Add this if you're using it to count the steps

    # Reset the starting time and duration
    start_time = None
    duration = None

    # Reset the sweep voltages
    current_sweep_voltage = sweep_start_voltage

    # Recompute the axis limits based on the cleared data
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)

    # Redraw the canvas
    canvas.draw_idle()
    fig.tight_layout()
    canvas.draw()

    # Clear any text or labels that display data
    voltage1_label.config(text="")
    voltage2_label.config(text="")
    voltage3_label.config(text="")
    current4_label.config(text="")
    current5_label.config(text="")
    current6_label.config(text="")

    # Reset any other GUI elements if necessary, like buttons or entries
    toggle_button_state(None)
    toggle_duration_button_state(None)

# Create main frames for graph and controls
graph_frame = tk.Frame(root, bg='white')
graph_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

controls_frame = tk.Frame(root, bg='white')
controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

# Embedding the Matplotlib figure in the Tkinter window within the graph_frame
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, padx=10, pady=10)

# Duration buttons frame within controls_frame
duration_frame = tk.Frame(controls_frame, bg='white')
duration_frame.grid(row=0, column=0, pady=10)

short_btn = ttk.Button(duration_frame, text="Short", command=lambda: set_duration("short"))
short_btn.grid(row=0, column=0, padx=5)

medium_btn = ttk.Button(duration_frame, text="Medium", command=lambda: set_duration("medium"))
medium_btn.grid(row=0, column=1, padx=5)

long_btn = ttk.Button(duration_frame, text="Long", command=lambda: set_duration("long"))
long_btn.grid(row=0, column=2, padx=5)

# Sweep Voltage Settings Frame
sweep_voltage_frame = tk.Frame(controls_frame, bg='white')
sweep_voltage_frame.grid(row=1, column=0, pady=10)

sweep_start_label = ttk.Label(sweep_voltage_frame, text="Sweep Start Voltage (V):", style='TLabel')
sweep_start_label.grid(row=0, column=0, padx=5)

sweep_start_entry = ttk.Entry(sweep_voltage_frame, width=10)
sweep_start_entry.grid(row=0, column=1)
sweep_start_entry.insert(0, "0.0")  # Default start voltage

sweep_end_label = ttk.Label(sweep_voltage_frame, text="Sweep End Voltage (V):", style='TLabel')
sweep_end_label.grid(row=1, column=0, padx=5)

sweep_end_entry = ttk.Entry(sweep_voltage_frame, width=10)
sweep_end_entry.grid(row=1, column=1)
sweep_end_entry.insert(0, "5.0")  # Default end voltage

# Step Settings Frame for sweep step voltage and step interval
step_settings_frame = tk.Frame(controls_frame, bg='white')
step_settings_frame.grid(row=2, column=0, pady=10)

# Label and Entry for Sweep Step Voltage
sweep_step_voltage_label = ttk.Label(step_settings_frame, text="Sweep Step Voltage (V):", style='TLabel')
sweep_step_voltage_label.grid(row=0, column=0, padx=5)

sweep_step_voltage_entry = ttk.Entry(step_settings_frame, width=10)
sweep_step_voltage_entry.grid(row=0, column=1, padx=5)
sweep_step_voltage_entry.insert(0, "0.1")  # Default value for the sweep step voltage

# Label and Entry for Step Interval
step_label = ttk.Label(step_settings_frame, text="Step Interval (s):", style='TLabel')
step_label.grid(row=1, column=0, padx=5)

step_entry = ttk.Entry(step_settings_frame, width=10)
step_entry.grid(row=1, column=1, padx=5)
step_entry.insert(0, "1.0")  # Default value for the step interval

# Add comboboxes for selecting channels for X and Y axes
channel_selection_frame = tk.Frame(controls_frame, bg='white')
channel_selection_frame.grid(row=4, column=0, pady=10)

x_axis_label = ttk.Label(channel_selection_frame, text="X-axis:")
x_axis_label.grid(row=0, column=0, padx=5)
x_axis_channels = ['V1 (V)', 'V2 (V)', 'V3 (V)', 'I4 (A)', 'I5 (A)', 'I6 (A)']
x_axis_combobox = ttk.Combobox(channel_selection_frame, values=x_axis_channels)
x_axis_combobox.grid(row=0, column=1, padx=5)
x_axis_combobox.set('V2 (V)')

y_axis_label = ttk.Label(channel_selection_frame, text="Y1-axis:")
y_axis_label.grid(row=1, column=0, padx=5)
y_axis_channels = ['V1 (V)', 'V2 (V)', 'V3 (V)', 'I4 (A)', 'I5 (A)', 'I6 (A)']
y_axis_combobox = ttk.Combobox(channel_selection_frame, values=y_axis_channels)
y_axis_combobox.grid(row=1, column=1, padx=5)
y_axis_combobox.set('I4 (A)')

# Y2-axis Label and Combobox
y2_axis_label = ttk.Label(channel_selection_frame, text="Y2-axis:")
y2_axis_label.grid(row=2, column=0, padx=5)
y2_axis_channels = ['V1 (V)', 'V2 (V)', 'V3 (V)', 'I4 (A)', 'I5 (A)', 'I6 (A)']
y2_axis_combobox = ttk.Combobox(channel_selection_frame, values=y2_axis_channels)
y2_axis_combobox.grid(row=2, column=1, padx=5)
y2_axis_combobox.set('I5 (A)')  # Set default or just leave blank if no default is required

# Create DAC1 Voltage Settings Frame
dac1_voltage_frame = tk.Frame(controls_frame, bg='white')
dac1_voltage_frame.grid(row=3, column=0, pady=10)  # Adjust the row index as per layout

# Label and Entry for DAC1 Voltage
dac1_voltage_label = ttk.Label(dac1_voltage_frame, text="DAC1 Voltage (V):", style='TLabel')
dac1_voltage_label.grid(row=0, column=0, padx=5)

dac1_voltage_entry = ttk.Entry(dac1_voltage_frame, width=10)
dac1_voltage_entry.grid(row=0, column=1, padx=5)
dac1_voltage_entry.insert(0, "0.0")  # Default value for DAC1 voltage

# Button frame to hold both buttons within controls_frame
btn_frame = tk.Frame(controls_frame, bg='white')
btn_frame.grid(row=5, column=0, pady=20)

collect_btn = ttk.Button(btn_frame, text="Collect Data", command=start_data_collection)
collect_btn.grid(row=0, column=0, padx=10)

stop_btn = ttk.Button(btn_frame, text="Stop", command=stop_data_collection)
stop_btn.grid(row=0, column=1, padx=10)

reset_btn = ttk.Button(btn_frame, text="Reset", command=reset_data_collection)
reset_btn.grid(row=0, column=2, padx=10)

# The voltage and current labels within controls_frame
voltage1_label = ttk.Label(controls_frame, text="")
voltage1_label.grid(row=6, column=0, pady=10)

voltage2_label = ttk.Label(controls_frame, text="")
voltage2_label.grid(row=7, column=0, pady=10)

voltage3_label = ttk.Label(controls_frame, text="")
voltage3_label.grid(row=8, column=0, pady=10)

current4_label = ttk.Label(controls_frame, text="")
current4_label.grid(row=9, column=0, pady=10)

current5_label = ttk.Label(controls_frame, text="")
current5_label.grid(row=10, column=0, pady=10)

current6_label = ttk.Label(controls_frame, text="")
current6_label.grid(row=11, column=0, pady=10)

# Add entries for Y-axis limits
y_axis_limits_frame = tk.Frame(controls_frame, bg='white')
y_axis_limits_frame.grid(row=12, column=0, pady=10)

y_min_label = ttk.Label(y_axis_limits_frame, text="Y-axis Min:")
y_min_label.grid(row=0, column=0, padx=5)
y_min_entry = ttk.Entry(y_axis_limits_frame, width=10)
y_min_entry.grid(row=0, column=1, padx=5)
y_min_entry.insert(0, "0")  # Default minimum Y-axis

y_max_label = ttk.Label(y_axis_limits_frame, text="Y-axis Max:")
y_max_label.grid(row=1, column=0, padx=5)
y_max_entry = ttk.Entry(y_axis_limits_frame, width=10)
y_max_entry.grid(row=1, column=1, padx=5)
y_max_entry.insert(0, "5")  # Default maximum Y-axis

root.mainloop()
