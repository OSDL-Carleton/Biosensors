import os
import tkinter as tk
from datetime import datetime

def create_controls_frame(parent, chip_name_entry, trial_name_entry):
    frame_controls = tk.LabelFrame(parent, text="Controls", relief=tk.SUNKEN, borderwidth=2)
    frame_controls.pack(fill="x", padx=10, pady=5)

    # Event handler for the Run button
    def on_run():
        # Define base directory
        base_dir = "/home/pi/Desktop/Biosensor V2/data"
        
        # Get Chip Name and Trial Name from entry widgets
        chip_name = chip_name_entry.get() if chip_name_entry else "Default Chip"
        trial_name = trial_name_entry.get() if trial_name_entry else "Trial 1"
        
        # Construct chip directory path
        chip_path = os.path.join(base_dir, chip_name)
        
        # Check if the Chip folder already exists
        if not os.path.exists(chip_path):
            try:
                os.makedirs(chip_path)
                print(f"Chip folder created: {chip_path}")
            except Exception as e:
                print(f"Failed to create chip folder: {e}")
                return
        else:
            print(f"Chip folder already exists: {chip_path}")
        
        # Add timestamp to trial name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trial_folder_name = f"{trial_name} - {timestamp}"
        trial_path = os.path.join(chip_path, trial_folder_name)
        
        # Create trial folder with the timestamped name
        try:
            os.makedirs(trial_path)
            print(f"Trial folder created: {trial_path}")
        except Exception as e:
            print(f"Failed to create trial folder: {e}")

    # Buttons
    run_button = tk.Button(frame_controls, text="Run", width=10, command=on_run)
    run_button.grid(row=0, column=0, padx=5, pady=5)
    pause_button = tk.Button(frame_controls, text="Pause/Resume", width=10)
    pause_button.grid(row=0, column=1, padx=5, pady=5)
    end_button = tk.Button(frame_controls, text="End", width=10)
    end_button.grid(row=0, column=2, padx=5, pady=5)
