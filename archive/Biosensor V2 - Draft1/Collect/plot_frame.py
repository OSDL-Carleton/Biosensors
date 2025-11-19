import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def create_plot_frame(parent):
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3], [0, 1, 4, 9], label="Sample Line")
    ax.set_xlabel("X-axis Label")
    ax.set_ylabel("Y-axis Label")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    toolbar = NavigationToolbar2Tk(canvas, parent)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
