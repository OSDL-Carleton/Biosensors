# gui_styles.py
from tkinter import ttk

def apply_styles():
    style = ttk.Style()

    # General button style
    style.configure('TButton', 
                    background='#007BFF', 
                    foreground='white', 
                    borderwidth=1,
                    relief='solid',
                    font=('Arial', 10, 'bold'), 
                    padding=(10, 5))

    style.map('TButton', 
              background=[('pressed', 'white'), ('active', '#0056b3'), ('disabled', '#d1d1d1')], 
              foreground=[('pressed', '#007BFF'), ('active', 'white')])

    # Selected button style for highlighting active buttons
    style.configure('Selected.TButton', 
                    background='white', 
                    foreground='#007BFF', 
                    borderwidth=1,
                    relief='solid',
                    font=('Arial', 10, 'bold'), 
                    padding=(10, 5))

    style.map('Selected.TButton', 
              background=[('pressed', '#007BFF'), ('active', 'white')], 
              foreground=[('pressed', 'white'), ('active', '#007BFF')])

    # Label style for all labels
    style.configure('TLabel', 
                    background='white', 
                    font=('Arial', 10))

    # Entry style (e.g., for input fields like Sweep Step Voltage, Y-axis limits, etc.)
    style.configure('TEntry', 
                    padding=(5, 5),
                    font=('Arial', 10))

    # Combobox style (for dropdowns like X-axis and Y-axis selection)
    style.configure('TCombobox', 
                    padding=(5, 5),
                    font=('Arial', 10))

    # Button layout
    style.layout("TButton", 
                 [('Button.border', {'children': [('Button.padding', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})], 'border': '10', 'sticky': 'nswe'})])
