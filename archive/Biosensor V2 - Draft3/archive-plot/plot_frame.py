import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

def create_plot_frame(parent, total_plots=5):
    current_plot = [1]  # Track the current plot index

    # Container for plot navigation and display
    plot_container = tk.Frame(parent)
    plot_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Navigation function to switch plots
    def switch_plot(direction):
        if direction == "previous" and current_plot[0] > 1:
            current_plot[0] -= 1
        elif direction == "next" and current_plot[0] < total_plots:
            current_plot[0] += 1

        # Update plot with dummy data for demonstration
        ax.cla()
        ax.plot([0, 1, 2, 3], [i * current_plot[0] for i in [0, 1, 4, 9]], label=f"Plot {current_plot[0]}")
        ax.set_xlabel("X-axis Label")
        ax.set_ylabel("Y-axis Label")
        ax.legend()
        canvas.draw()

        # Update the image label to show the current plot number
        image_label.config(text=f"Image {current_plot[0]} of {total_plots}")

    # Previous and Next buttons for plot navigation
    prev_button = tk.Button(plot_container, text="◀", command=lambda: switch_plot("previous"))
    prev_button.pack(side=tk.LEFT, padx=5, pady=5)

    next_button = tk.Button(plot_container, text="▶", command=lambda: switch_plot("next"))
    next_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Plot area setup
    plot_area = tk.Frame(plot_container)
    plot_area.pack(fill="both", expand=True, side=tk.LEFT)

    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3], [0, 1, 4, 9], label="Sample Plot")
    ax.set_xlabel("X-axis Label")
    ax.set_ylabel("Y-axis Label")
    ax.legend()

    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_area)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Interactive toolbar for plot
    toolbar = NavigationToolbar2Tk(canvas, parent)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Footer label to show the current image number
    image_label = tk.Label(parent, text=f"Image {current_plot[0]} of {total_plots}", font=("Arial", 12))
    image_label.pack(side=tk.BOTTOM, pady=5)
