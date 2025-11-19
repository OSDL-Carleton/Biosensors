from tkinter import ttk

def apply_styles():
    style = ttk.Style()

    # General button style
    style.configure('TButton', 
                    background='#007BFF', 
                    foreground='white', 
                    borderwidth=1,
                    relief='solid',
                    bordercolor='#007BFF',
                    focuscolor=style.configure(".")["background"], 
                    font=('Arial', 10, 'bold'), 
                    padding=(10, 5))

    style.map('TButton', 
              background=[('pressed', 'white'), ('active', '#0056b3'), ('disabled', '#d1d1d1')], 
              foreground=[('pressed', '#007BFF'), ('active', 'white')])

    # Selected button style
    style.configure('Selected.TButton', 
                    background='white', 
                    foreground='#007BFF', 
                    borderwidth=1,
                    relief='solid',
                    bordercolor='#007BFF',
                    focuscolor=style.configure(".")["background"], 
                    font=('Arial', 10, 'bold'), 
                    padding=(10, 5))

    style.map('Selected.TButton', 
              background=[('pressed', '#007BFF'), ('active', 'white')], 
              foreground=[('pressed', 'white'), ('active', '#007BFF')])

    # Label style
    style.configure('TLabel', 
                    background='white', 
                    font=('Arial', 10))

    # Button layout
    style.layout("TButton", 
                 [('Button.border', {'children': [('Button.padding', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})], 'border': '10', 'sticky': 'nswe'})])
