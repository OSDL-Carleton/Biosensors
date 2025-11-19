import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from gui_styles import apply_styles
import subprocess

def collect_action():
    try:
        print("Collect button pressed")
        collect_button.state(['!pressed'])
        subprocess.Popen(["python", "/home/pi/Desktop/Biosensor V1/Collect/main.py"])
    except Exception as e:
        print(f"Error launching collect script: {e}")

def analyze_action():
    try:
        print("Analyze button pressed")
        analyze_button.state(['!pressed'])
        subprocess.Popen(["python", "/home/pi/Desktop/Biosensor V1/Analyze/main.py"])
    except Exception as e:
        print(f"Error launching analyze script: {e}")

def collect_analyze_action():
    try:
        print("Collect & Analyze button pressed")
        subprocess.Popen(["python", "/home/pi/Desktop/Biosensor V1/Collect/main.py"])
        subprocess.Popen(["python", "/home/pi/Desktop/Biosensor V1/Analyze/main.py"])
    except Exception as e:
        print(f"Error launching collect & analyze scripts: {e}")

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def escape_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root = tk.Tk()
root.title("Biosensor V1")

root.attributes("-fullscreen", True)

root.bind("<Escape>", escape_fullscreen)

root.configure(bg='white')
apply_styles()

style = ttk.Style()
large_font = ('Helvetica', 20, 'bold') 
style.configure('Large.TButton', font=large_font, padding=10) 
logo_path = '/home/pi/Desktop/Biosensor V1/OSDL-Logo.jpg'
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((180, 180), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

main_frame = tk.Frame(root, bg='white')
main_frame.pack(expand=True, fill='both')

content_frame = tk.Frame(main_frame, bg='white')
content_frame.pack(expand=True)

logo_label = ttk.Label(content_frame, image=logo_photo, background='white')
logo_label.pack(pady=10)

button_frame = tk.Frame(content_frame, bg='white')
button_frame.pack(pady=10)

collect_button = ttk.Button(button_frame, text="Collect", command=collect_action, style='Large.TButton')
analyze_button = ttk.Button(button_frame, text="Analyze", command=analyze_action, style='Large.TButton')
collect_analyze_button = ttk.Button(button_frame, text="Collect & Analyze", command=collect_analyze_action, style='Large.TButton')

collect_button.pack(side='left', padx=15, pady=10, ipadx=10, ipady=10)
analyze_button.pack(side='left', padx=15, pady=10, ipadx=10, ipady=10)
collect_analyze_button.pack(side='left', padx=15, pady=10, ipadx=10, ipady=10)

root.mainloop()
