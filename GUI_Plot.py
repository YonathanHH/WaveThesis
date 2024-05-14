import tkinter as tk
from tkinter import filedialog
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from t2listing import *
import numpy as np

def plot_data():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Pressure (bar)')
    ax.grid(True)
    colors = ['#f50505','#1105f5', '#29f505','#e905f5','#f5f105','#05f5ad']  # List of colors for plots
    labels = []  # List to store labels for legend

    for idx, file_path in enumerate(file_paths):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            time = []
            pressure = []
            for row in reader:
                time.append(float(row[0]))
                pressure.append(float(row[1]))
            label = plot_labels[idx].get()  # Get the label from the entry field
            labels.append(label)
            color = colors[idx % len(colors)]  # Cycle through colors for each plot
            ax.semilogx(time, pressure, label=label, color=color)  # Use semilogy for semilog plot

    ax.legend(labels)
    ax.set_title('pressure overtime at injection block')  # Set the graph title
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("SVG", "*.svg"), ("PDF", "*.pdf")])
    if file_path:
        plt.savefig(file_path)
def add_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        file_paths.append(file_path)
        file_list.insert(tk.END, file_path)
        plot_label_entry = tk.Entry(plot_label_frame)
        plot_label_entry.pack(pady=5)
        plot_labels.append(plot_label_entry)


root = tk.Tk()
root.title("Multifunction TOUGH2 GUI")

file_paths = []
plot_labels = []  # List to store label entry fields

file_title = tk.Label(root, text="Files:")
file_list = tk.Listbox(root, width=50)
file_list.pack(pady=10)

add_button = tk.Button(root, text="Add File", command=add_file)
add_button.pack(pady=5)

save_button = tk.Button(root, text="Save Plot", command=save_plot)
save_button.pack(pady=5)

#graph_title = tk.StringVar()
#title_entry = tk.Entry(root, textvariable=graph_title)
#title_entry.pack(pady=5)

plot_label_frame = tk.Frame(root)
plot_label_frame.pack(pady=10)

plot_button = tk.Button(root, text="Plot Data", command=plot_data)
plot_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

root.mainloop()