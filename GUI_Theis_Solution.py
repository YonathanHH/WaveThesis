import numpy as np
from scipy.special import expi
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog
import tkinter as tk

# Function to calculate and plot the results
def plot_results():
    # Get user input values
    p0 = float(p0_entry.get())
    h = float(h_entry.get())
    k = float(k_entry.get())
    r = float(r_entry.get())
    porosity = float(porosity_entry.get())
    px = float(px_entry.get())

    # Calculate other parameters
    v = 1.326e-6  # Fluid Viscosity
    density = 1000
    Crock = 1.e-10
    Cfluid = 4.52e-10
    compressability = Crock + Cfluid
    D = (k/v)/(porosity*density*compressability)  # Diffusivity in m2/s

    # Load flow rate data
    data_file = filedialog.askopenfilename(title="Select Flowrate CSV File")
    data = pd.read_csv(data_file)
    t = data['time'].values
    qm = data['flowrate'].values

    # Calculate pressure
    z = (r**2 / (4 * D * t))
    p = p0 + (qm / (4 * np.pi * h * k / v)) * expi(z)
    pbar = (p/1e5) - px

    # Load numerical simulation result
    press1_file = filedialog.askopenfilename(title="Select Numerical Simulation CSV File")
    press1 = np.loadtxt(press1_file, delimiter=',')
    press1_time = np.array(list(press1[:,0]))
    press1_P = np.array(list(press1[:,1]))

    # Plot the results
    plt.figure(figsize=(10, 5))
    plt.xlabel('Time[bar]')
    plt.ylabel('Pressure[bar]')
    plt.ylim(0,85)
    plt.title('Pressure vs Time')
    plt.semilogx(press1_time, press1_P, color='red', label='Numerical')
    plt.semilogx(t, pbar, color='blue', label='Analytical')
    plt.grid(True)
    plt.legend(loc='lower right')
    plt.show()

# Create the GUI
root = tk.Tk()
root.title("Modern Theis Solution")

# Create input fields
p0_label = tk.Label(root, text="p0:")
p0_label.grid(row=0, column=0, padx=5, pady=5)
p0_entry = tk.Entry(root)
p0_entry.grid(row=0, column=1, padx=5, pady=5)

h_label = tk.Label(root, text="h:")
h_label.grid(row=1, column=0, padx=5, pady=5)
h_entry = tk.Entry(root)
h_entry.grid(row=1, column=1, padx=5, pady=5)

k_label = tk.Label(root, text="k:")
k_label.grid(row=2, column=0, padx=5, pady=5)
k_entry = tk.Entry(root)
k_entry.grid(row=2, column=1, padx=5, pady=5)

r_label = tk.Label(root, text="r:")
r_label.grid(row=3, column=0, padx=5, pady=5)
r_entry = tk.Entry(root)
r_entry.grid(row=3, column=1, padx=5, pady=5)

porosity_label = tk.Label(root, text="Porosity:")
porosity_label.grid(row=4, column=0, padx=5, pady=5)
porosity_entry = tk.Entry(root)
porosity_entry.grid(row=4, column=1, padx=5, pady=5)

px_label = tk.Label(root, text="px:")
px_label.grid(row=5, column=0, padx=5, pady=5)
px_entry = tk.Entry(root)
px_entry.grid(row=5, column=1, padx=5, pady=5)

# Create the plot button
plot_button = tk.Button(root, text="Plot", command=plot_results)
plot_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
