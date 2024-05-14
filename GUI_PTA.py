import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from math import log10, log

#the code used some calculation from (McLean, 2020)
diff_int = 0.2
def calculate_superposition_time(array_time, array_flowtimes, array_flowrate):
    if not len(array_flowrate)==len(array_flowtimes):
        sys.exit("arrays not same length")
    sup_t = np.empty(len(array_time),dtype=float)
    N = len(array_flowrate)
    q = array_flowrate
    t = array_flowtimes

    for x in range(0,len(array_time)):
        sup_t[x] = log10(array_time[x])

        for i in range(0,N-1):
            if i==0:
                temp = (q[i]/(q[N-1]-q[N-2]))*log10(t[N-1]-t[i]+array_time[x])
                sup_t[x] = sup_t[x] + temp
            else:
                temp = ((q[i]-q[i -1]) /(q[N -1] - q[N -2]) )* log10 (t[N -1] -t[i]+array_time[x])
                sup_t[x] = sup_t[x] + temp
    return sup_t

def calculate_delta ( array_data ):
    delta = np.empty(len(array_data) - 1, dtype=float)

    for i in range (0, len( delta )):
        temp = array_data[i + 1] - array_data[0]
        delta[i] = abs(temp)
    return delta

def find_ln_sep_points(array, i, interval):
    j = 1
    k = 1
    while i + j <= len(array) - 1:
        if i == 0:
            break
        if log(array[i + j]) - log(array[i]) >= interval:
            break
        if log( array [i+j]) - log( array [i]) < interval and i+j == len( array ) -1:
            j = 0
            break
        j = j + 1
    if i == len(array) - 1:
        j = 0

    while i-k > 0:
        if log(array[i]) - log(array[i - k]) >= interval:
            break
        if log(array[i]) - log(array[i - k]) < interval and i - k == 0:
            k = 0
            break
        k = k + 1

    if i == 0 or i == 1:
        k = 0

    return j, k

#Function to calculate smooth derivative
def calculate_smooth_derivative ( array_time ,ar_dP ,ar_Sn , diff_interval ):
    deriv_smooth = np.empty(len(array_time), dtype=float)
    j_indices = np.empty(len(array_time), dtype=int)
    k_indices = np.empty(len(array_time), dtype=int)

    for i in range(0, len(array_time)):
        j, k = find_ln_sep_points(array_time, i, diff_interval)
        j_indices[i] = j
        k_indices[i] = k

    for i in range (0, len( array_time )):
        if i==0:
            deriv_smooth[i] = 0.0
        else:
            j = j_indices[i]
            k = k_indices[i]
            if j == 0 or k == 0:
                deriv_smooth[i] = 0.0
                continue
            if i-k<0 or i+j>len( deriv_smooth ):
                deriv_smooth[i] = -9999.0
                continue

            temp = ar_dP[i + j] * ((ar_Sn[i] - ar_Sn[i - k]) / ((ar_Sn[i + j] - ar_Sn[i]) * (ar_Sn[i+j] - ar_Sn[i-k]))) + \
                   ar_dP[i]*((ar_Sn[i+j] + ar_Sn[i-k]-2 * ar_Sn[i]) / ((ar_Sn[i+j] - ar_Sn[i]) * (ar_Sn[i+j] - ar_Sn[i-k]))) \
                   - ar_dP[i-k]*((ar_Sn[i+j]-ar_Sn[i])/(( ar_Sn [i]- ar_Sn [i-k]) * ( ar_Sn [i+j] - ar_Sn [i-k])))
            deriv_smooth[i] = temp / 2.303
    return deriv_smooth

def calculate_smooth_derivative_noSn (ar_t ,ar_dP , diff_interval ):
    deriv_smooth_bad = np.empty(len(ar_t), dtype=float)
    j_indices = np.empty(len(ar_t), dtype=int)
    k_indices = np.empty(len(ar_t), dtype=int)

    ln_t_2 = calculate_ln_time(ar_t)

    for i in range(0, len(ar_t)):
        j, k = find_ln_sep_points(ar_t, i, diff_interval)
        j_indices[i] = j
        k_indices[i] = k

    for i in range(0, len(ar_t)):
        if i == 0:
            deriv_smooth_bad[i] = 0.0
        else:
            j = j_indices[i]
            k = k_indices[i]
            if j == 0 or k == 0:
                deriv_smooth_bad[i] = 0.0
                continue
            if i - k < 0 or i + j > len(deriv_smooth_bad):
                deriv_smooth_bad[i] = -9999.0
                continue

            temp = ar_dP[i + j] * ((ln_t_2[i] - ln_t_2[i - k]) / ((ln_t_2[i + j] - ln_t_2[i]) *( ln_t_2 [i+j]- ln_t_2 [i-k]))) +\
                   ar_dP[i] * ((ln_t_2[i + j] + ln_t_2 [i-k] -2* ln_t_2 [i]) /(( ln_t_2 [i+j]- ln_t_2 [i]) *( ln_t_2 [i]- ln_t_2 [i-k]))) \
                   - ar_dP [i-k ]*(( ln_t_2 [i+j]- ln_t_2 [i]) /(( ln_t_2 [i] -ln_t_2 [i-k]) *( ln_t_2 [i+j]- ln_t_2 [i-k])))
            deriv_smooth_bad[i] = temp
    return deriv_smooth_bad

def calculate_ln_time(array_time):
    array_ln_time = np.empty(len(array_time), dtype=float)

    for i in range(0, len(array_time)):
        temp = np.log(array_time[i])
        array_ln_time[i] = temp

    return array_ln_time

def plot_pressure_transient():
    press1 = np.loadtxt(press1_file, delimiter=',')
    press1_time = np.array(list(press1[:,0]))
    press1_P = np.array(list(press1[:,1]))

    FLOW = np.loadtxt(FLOW_file, delimiter=',')
    FLOW_time = np.array(list(FLOW[:,0]))
    FLOW_rate = np.array(list(FLOW[:,1]))

    delta_time_1 = calculate_delta(press1_time)
    delta_P_1 = calculate_delta(press1_P)

    temp_FLOW_time = FLOW_time[: 0]
    temp_FLOW_rate = FLOW_rate[: 0]

    Sn_1 = calculate_superposition_time(delta_time_1, temp_FLOW_time, temp_FLOW_rate)
    ln_time_1 = calculate_ln_time(delta_time_1)

    smooth_deriv_1 = calculate_smooth_derivative(delta_time_1, delta_P_1, Sn_1, diff_int)
    smooth_deriv_no_superposition_1 = calculate_smooth_derivative_noSn(delta_time_1, delta_P_1, diff_int)

    delta_time_1_crop = delta_time_1[: -1]
    delta_P_1_crop = delta_P_1[: -1]
    smooth_deriv_1_crop = smooth_deriv_1[: -1]
    smooth_deriv_no_superposition_1_crop = smooth_deriv_no_superposition_1[: -1]

    fig = plt.figure()
    plt.plot(delta_time_1_crop, delta_P_1_crop, 'r-', linewidth=3.0, label='model P 1')
    plt.plot(delta_time_1_crop, smooth_deriv_no_superposition_1_crop, 'r--', linewidth=2.0, label='model dP no superposition 1')
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel('Time [ seconds ]')
    plt.ylabel('Pressure and derivative [bar]')
    plt.grid(True)
    plt.legend(loc='upper left', fontsize=10)
    plt.title('Log-log pressure derivative plot')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

def select_press1_file():
    global press1_file
    press1_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    press1_label.config(text=f"Press1 file: {press1_file}")

def select_FLOW_file():
    global FLOW_file
    FLOW_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    FLOW_label.config(text=f"FLOW file: {FLOW_file}")

root = tk.Tk()
root.title("Pressure Transient Analysis")

press1_label = tk.Label(root, text="Press1 file: None")
press1_label.pack()

FLOW_label = tk.Label(root, text="FLOW file: None")
FLOW_label.pack()

press1_button = tk.Button(root, text="Select Pressure File", command=select_press1_file)
press1_button.pack()

FLOW_button = tk.Button(root, text="Select Flow File", command=select_FLOW_file)
FLOW_button.pack()

plot_button = tk.Button(root, text="Plot Pressure Transient", command=plot_pressure_transient)
plot_button.pack()

root.mainloop()
