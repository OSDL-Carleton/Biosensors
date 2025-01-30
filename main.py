import tkinter as tk
from tkinter import ttk
from collect.collect_tab import collect_tab
from analyze.analyze_tab import analyze_tab
from plot.plot_tab import plot_tab
from settings.settings_tab import settings_tab


def main():
    root = tk.Tk()
    root.title("OSDL OEGFET")
    root.geometry("1000x600")
    root.configure(bg="lightgrey")

    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=[10, 5])
    style.configure("TNotebook", tabposition="n")
    style.configure("Centered.TNotebook", tabmargins=[200, 2, 200, 0])

    notebook = ttk.Notebook(root, style="Centered.TNotebook")
    notebook.pack(fill="both", expand=True)

    tab_main = ttk.Frame(notebook)
    notebook.add(tab_main, text="Main")

    main_label = tk.Label(tab_main, text="Welcome Home", font=("Arial", 24))
    main_label.pack(pady=20)

    button_frame = tk.Frame(tab_main)
    button_frame.pack(pady=20)

    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    def switch_to_collect_and_analyze():
        notebook.select(tab_collect)

    collect_analyze_button = tk.Button(
        button_frame,
        text="Collect & Analyze",
        command=switch_to_collect_and_analyze,
        width=15,
    )
    collect_analyze_button.grid(row=0, column=2, padx=10, pady=5)

    tab_collect = ttk.Frame(notebook)
    notebook.add(tab_collect, text="Collect")
    collect_tab(tab_collect, root)

    tab_analyze = ttk.Frame(notebook)
    notebook.add(tab_analyze, text="Analyze")
    analyze_tab(tab_analyze)

    tab_plot = ttk.Frame(notebook)
    notebook.add(tab_plot, text="Plot")
    plot_tab(tab_plot)

    tab_settings = ttk.Frame(notebook)
    notebook.add(tab_settings, text="Settings")
    settings_tab(tab_settings)

    root.mainloop()


if __name__ == "__main__":
    main()
