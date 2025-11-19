import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

# Create main window
root = tk.Tk()
root.title("Scale Block Wizard")
root.geometry("1000x600")  # Adjust window size
root.configure(bg='lightgrey')

# Create Notebook for tabs in the main window
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Main Tab
tab_main = ttk.Frame(notebook)
notebook.add(tab_main, text="Main")

# Welcome message in Main Tab
main_label = tk.Label(tab_main, text="Welcome Home", font=("Arial", 24))
main_label.pack(expand=True, pady=20)

# Collect Tab
tab_collect = ttk.Frame(notebook)
notebook.add(tab_collect, text="Collect")

# Frame for parameters and controls on the left side in Collect Tab
left_frame_collect = tk.Frame(tab_collect, width=250, bg='lightgrey')
left_frame_collect.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

# Notebook for inner tabs in the Collect left frame
notebook_collect = ttk.Notebook(left_frame_collect)
notebook_collect.pack(fill="both", expand=True)

# Data Setup Frame
frame_data_setup = tk.LabelFrame(notebook_collect, text="Data Setup", relief=tk.SUNKEN, borderwidth=2)
frame_data_setup.pack(fill="x", padx=10, pady=10)

# Chip Name input
tk.Label(frame_data_setup, text="Chip Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
chip_name_entry = tk.Entry(frame_data_setup, width=20)
chip_name_entry.grid(row=0, column=1, padx=5, pady=5)
chip_name_entry.insert(0, "Default Chip")

# Trial Name input
tk.Label(frame_data_setup, text="Trial Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
trial_name_entry = tk.Entry(frame_data_setup, width=20)
trial_name_entry.grid(row=1, column=1, padx=5, pady=5)
trial_name_entry.insert(0, "Trial 1")

# Test Parameters Frame
frame_params = tk.LabelFrame(notebook_collect, text="Test Parameters", relief=tk.SUNKEN, borderwidth=2)
frame_params.pack(fill="x", padx=10, pady=10)

# Set a uniform width for all Entry fields
entry_width = 20

# Time Limit in seconds
tk.Label(frame_params, text="Time limit (sec):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
time_limit = tk.Entry(frame_params, width=entry_width)
time_limit.grid(row=0, column=1, columnspan=3, pady=5, sticky="w")
time_limit.insert(0, "120")  # Default to 2 minutes

# Sweep Voltage inputs
tk.Label(frame_params, text="Sweep Voltage (V):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
sweep_min_entry = tk.Entry(frame_params, width=8)
sweep_min_entry.grid(row=1, column=1, padx=(0, 2), pady=5, sticky="w")
sweep_min_entry.insert(0, "0.0")
tk.Label(frame_params, text="to").grid(row=1, column=2, padx=(2, 2), sticky="w")
sweep_max_entry = tk.Entry(frame_params, width=8)
sweep_max_entry.grid(row=1, column=3, padx=(2, 5), pady=5, sticky="w")
sweep_max_entry.insert(0, "5.0")

# Sweep Step Voltage
tk.Label(frame_params, text="Sweep Step Voltage (V):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
failing_pressure = tk.Entry(frame_params, width=entry_width)
failing_pressure.grid(row=2, column=1, columnspan=3, pady=5, sticky="w")
failing_pressure.insert(0, "0.1")

# Step Interval
tk.Label(frame_params, text="Step Interval (s):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
chemical = tk.Entry(frame_params, width=entry_width)
chemical.grid(row=3, column=1, columnspan=3, pady=5, sticky="w")
chemical.insert(0, "1")

# DAC1 Voltage
tk.Label(frame_params, text="DAC1 Voltage (V):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
concentration = tk.Entry(frame_params, width=entry_width)
concentration.grid(row=4, column=1, columnspan=3, pady=5, sticky="w")
concentration.insert(0, "0.5")

# Frame for displaying console log inside the 'Collect' tab
frame_output = tk.LabelFrame(notebook_collect, text="Console Log", relief=tk.SUNKEN, borderwidth=2)
frame_output.pack(fill="both", padx=10, pady=5, expand=True)

# Adding a scrollbar
output_text = tk.Text(frame_output, height=10, width=45, wrap="none", bg='white')
scrollbar = tk.Scrollbar(frame_output, orient=tk.VERTICAL, command=output_text.yview)
output_text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frame for test controls inside the 'Collect' tab
frame_controls = tk.LabelFrame(notebook_collect, text="Test controls", relief=tk.SUNKEN, borderwidth=2)
frame_controls.pack(fill="x", padx=10, pady=5)

run_button = tk.Button(frame_controls, text="Run", width=10)
run_button.grid(row=0, column=0, padx=5, pady=5)
pause_button = tk.Button(frame_controls, text="Pause/Resume", width=10)
pause_button.grid(row=0, column=1, padx=5, pady=5)
end_button = tk.Button(frame_controls, text="End", width=10)
end_button.grid(row=0, column=2, padx=5, pady=5)

# Plot Frame for Collect tab to the right
plot_frame_collect = tk.Frame(tab_collect, width=750)
plot_frame_collect.pack(fill="both", expand=True, side=tk.RIGHT)

# Create a sample plot in the Collect tab
fig_collect, ax_collect = plt.subplots()
ax_collect.plot([0, 1, 2, 3], [0, 1, 4, 9], label="Sample Line")
ax_collect.set_xlabel("X-axis Label")
ax_collect.set_ylabel("Y-axis Label")
ax_collect.legend()

# Embed the plot in Tkinter
canvas_collect = FigureCanvasTkAgg(fig_collect, master=plot_frame_collect)
canvas_collect.draw()
canvas_collect.get_tk_widget().pack(fill="both", expand=True)

# Adding interactive toolbar for zoom and pan
toolbar_collect = NavigationToolbar2Tk(canvas_collect, plot_frame_collect)
toolbar_collect.update()
toolbar_collect.pack(side=tk.BOTTOM, fill=tk.X)

# Analyze Tab
tab_analyze = ttk.Frame(notebook)
notebook.add(tab_analyze, text="Analyze")

# Left Frame for file selection message in Analyze tab
left_frame_analyze = tk.Frame(tab_analyze, width=250, bg='lightgrey')
left_frame_analyze.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

# Label in Analyze left frame for file selection area
file_selection_label = tk.Label(left_frame_analyze, text="This is where the file selection goes", bg='lightgrey', font=("Arial", 12))
file_selection_label.pack(expand=True, pady=20)

# Plot Frame for Analyze tab to the right
plot_frame_analyze = tk.Frame(tab_analyze, width=750, bg='white')
plot_frame_analyze.pack(fill="both", expand=True, side=tk.RIGHT)

# Empty plot area message in Analyze tab
analyze_plot_label = tk.Label(plot_frame_analyze, text="This is where a plot goes", font=("Arial", 16))
analyze_plot_label.pack(expand=True, pady=20)

# Plot Settings Tab
tab_plot_settings = ttk.Frame(notebook)
notebook.add(tab_plot_settings, text="Plot Settings")

# Frame for Axis Selector inside the 'Plot Settings' tab
frame_axis_selector = tk.LabelFrame(tab_plot_settings, text="Axis Selector", relief=tk.SUNKEN, borderwidth=2)
frame_axis_selector.pack(fill="x", padx=10, pady=10)

# Dropdowns for X-axis, Y1-axis, Y2-axis, and Y3-axis
axes_options = ["V1 (V)", "V2 (V)", "V3 (V)", "I1 (A)", "I2 (A)", "I3 (A)", "I4 (A)", "I5 (A)", "I6 (A)", "None"]

tk.Label(frame_axis_selector, text="X-axis:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
x_axis_dropdown = ttk.Combobox(frame_axis_selector, values=axes_options)
x_axis_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
x_axis_dropdown.set("V2 (V)")

tk.Label(frame_axis_selector, text="Y1-axis:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
y1_axis_dropdown = ttk.Combobox(frame_axis_selector, values=axes_options)
y1_axis_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
y1_axis_dropdown.set("I4 (A)")

tk.Label(frame_axis_selector, text="Y2-axis:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
y2_axis_dropdown = ttk.Combobox(frame_axis_selector, values=axes_options)
y2_axis_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
y2_axis_dropdown.set("I6 (A)")

tk.Label(frame_axis_selector, text="Y3-axis:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
y3_axis_dropdown = ttk.Combobox(frame_axis_selector, values=axes_options)
y3_axis_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
y3_axis_dropdown.set("None")

# Frame for Axis Range inside the 'Plot Settings' tab
frame_axis_range = tk.LabelFrame(tab_plot_settings, text="Axis Range", relief=tk.SUNKEN, borderwidth=2)
frame_axis_range.pack(fill="x", padx=10, pady=10)

# Axis range inputs for X and Y axis
tk.Label(frame_axis_range, text="X range:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
x_min_entry = tk.Entry(frame_axis_range, width=10)
x_min_entry.grid(row=0, column=1, padx=(0, 2), pady=5, sticky="w")
x_min_entry.insert(0, "0")
tk.Label(frame_axis_range, text="to").grid(row=0, column=2, padx=(2, 2), sticky="w")
x_max_entry = tk.Entry(frame_axis_range, width=10)
x_max_entry.grid(row=0, column=3, padx=(2, 5), pady=5, sticky="w")
x_max_entry.insert(0, "3")

tk.Label(frame_axis_range, text="Y range:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
y_min_entry = tk.Entry(frame_axis_range, width=10)
y_min_entry.grid(row=1, column=1, padx=(0, 2), pady=5, sticky="w")
y_min_entry.insert(0, "0")
tk.Label(frame_axis_range, text="to").grid(row=1, column=2, padx=(2, 2), sticky="w")
y_max_entry = tk.Entry(frame_axis_range, width=10)
y_max_entry.grid(row=1, column=3, padx=(2, 5), pady=5, sticky="w")
y_max_entry.insert(0, "5")

# Run the application
root.mainloop()
