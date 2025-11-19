import tkinter as tk
from tkinter import ttk
from collect import collect_tab
from analyze import analyze_tab
from plot_settings import plot_settings_tab

def main():
    # Create main window
    root = tk.Tk()
    root.title("OSDL OEGFET")
    root.geometry("1000x600")
    root.configure(bg='lightgrey')

    # Create Notebook for tabs in the main window
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Main Tab
    tab_main = ttk.Frame(notebook)
    notebook.add(tab_main, text="Main")

    # Welcome message in Main Tab
    main_label = tk.Label(tab_main, text="Welcome Home", font=("Arial", 24))
    main_label.pack(pady=20)

    # Frame for buttons below the welcome message
    button_frame = tk.Frame(tab_main)
    button_frame.pack(pady=20)

    # Button to switch to both Collect and Analyze (You can customize this function)
    def switch_to_collect_and_analyze():
        notebook.select(tab_collect)
        # Add any additional actions for "Collect & Analyze" here

    collect_analyze_button = tk.Button(button_frame, text="Collect & Analyze", command=switch_to_collect_and_analyze, width=15)
    collect_analyze_button.grid(row=0, column=2, padx=10, pady=5)

    # Collect Tab
    tab_collect = ttk.Frame(notebook)
    notebook.add(tab_collect, text="Collect")
    collect_tab(tab_collect)

    # Analyze Tab
    tab_analyze = ttk.Frame(notebook)
    notebook.add(tab_analyze, text="Analyze")
    analyze_tab(tab_analyze)

    # Plot Settings Tab
    tab_plot_settings = ttk.Frame(notebook)
    notebook.add(tab_plot_settings, text="Plot Settings")
    plot_settings_tab(tab_plot_settings)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
