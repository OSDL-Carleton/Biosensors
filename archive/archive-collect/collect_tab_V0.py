import time
import datetime
import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import ttk
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from . import ADS1256
from . import DAC8532
from collect.data_setup_frame import create_data_setup_frame
from collect.params_frame import create_params_frame
from collect.console_log_frame import create_console_log_frame
from collect.controls_frame import create_controls_frame
from collect.plot_frame import create_plot_frame

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

def collect_tab(tab_collect):
    # Frame for parameters and controls on the left side in Collect Tab
    left_frame_collect = tk.Frame(tab_collect, width=250, bg='lightgrey')
    left_frame_collect.pack(fill="both", expand=False, side=tk.LEFT, padx=10, pady=10)

    # Notebook for inner tabs in the Collect left frame
    notebook_collect = ttk.Notebook(left_frame_collect)
    notebook_collect.pack(fill="both", expand=True)

    # Add Data Setup frame and retrieve entries for Chip and Trial Name
    chip_name_entry, trial_name_entry = create_data_setup_frame(notebook_collect)
    
    # Add Parameters frame
    create_params_frame(notebook_collect)

    # Add Console Log frame
    create_console_log_frame(notebook_collect)

    # Add Controls frame and pass the Chip and Trial Name entries to it
    create_controls_frame(notebook_collect, chip_name_entry, trial_name_entry)

    # Plot Frame for Collect tab to the right
    plot_frame_collect = tk.Frame(tab_collect, width=750)
    plot_frame_collect.pack(fill="both", expand=True, side=tk.RIGHT)

    # Add the plot frame
    create_plot_frame(plot_frame_collect)
