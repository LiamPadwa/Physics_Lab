import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.append(os.path.abspath('../..'))
from utils import pandas_tools as pt

T2_path = 'Pulse_NMR_61/create_databases/T2_Data.json'
plot_directory = 'Pulse_NMR_61/Plots/T2/Peaks/'

with open(T2_path, "r") as f:
    T2_Data = json.load(f)

# Getting the envelopes for all T2 data. stds should be adjusted 
for material, data in tqdm(T2_Data.items()):
    print(material)
    x, y = np.array(data['time']), np.array(data['volt'])
    tau = data['tau']
    peak_diff = 1.8 * tau if tau == 0.1 else 1.7 * tau
    min_h = 4.4 if material == '2 para' else 5.
    x_peaks, y_peaks = pt.get_peaks(x, y, min_time_between_peaks=peak_diff, min_height=min_h)

    x, y_smooth = pt.smooth_xy_data(x, y, window_length=31, polyorder=2)
    x_speak, y_speak = pt.get_peaks(x, y_smooth, min_time_between_peaks=0.9*peak_diff, min_height = 5.)

    data['x_peak'], data['y_peak'] = list(x_peaks), list(y_peaks)
    data['delta_t'] = [0.2 * tau] * len(x_peaks)

    dv = 0.15
    if material in ('water', '2 para', '1 para'): dv = 0.5
    if material in ('4 para', '0.5 para', '0.25 para', '0.125 para'): dv = 0.3
    if material in ('glycerine'): data['delta_v']: dv = 0.2
    data['delta_v'] = [dv] * len(y_peaks)
    
    T2_Data[material] = data

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label='Signal', alpha=0.5)
    plt.plot(x_peaks, y_peaks, 'go', label='Envelope Peaks')
    # plt.plot(x, y_smooth, label='Smooth', color='purple', alpha=0.3)
    # plt.plot(x_speak, y_speak, 'co', label='Smooth Peaks')
    plt.xlabel('Time [ms]')
    plt.ylabel('Voltage [V]')
    plt.title(f'Envelope Detection from {material}')
    plt.legend()
    plt.grid(True)
    file_name = f'peaks_for_{material}.png'
    plt.savefig(plot_directory + file_name)

with open(T2_path, 'w') as f:
    json.dump(T2_Data, f, indent=4)