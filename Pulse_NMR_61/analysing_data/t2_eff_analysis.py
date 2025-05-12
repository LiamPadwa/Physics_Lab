import sys
import os
import json
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.stats import chi2

sys.path.append(os.path.abspath('../..'))
from utils import root_tools as rt

plot_directory = 'Pulse_NMR_61/Plots/T2_eff/eps/'
T2_eff_path = 'Pulse_NMR_61/create_databases/T2_Eff_Data.json'

with open(T2_eff_path, "r") as f:
    T2_Eff_Data = json.load(f)


def fit_function(x, A, T2, C, t0, T_RC):
    """Fit function: A * (1 - exp(-x / T_RC)) * exp(-(x-t0) / T2)"""
    return A * (1 - np.exp(- (x - t0) / T_RC)) * np.exp(-(x - t0) / T2) + C

save_plt: bool = False
for material, data in tqdm(T2_Eff_Data.items()):    
    time = np.array(data['time'])
    volt = np.array(data['volt'])
    sigma_time = np.array(data['delta_time'])
    sigma_volt = np.array(data['delta_v'])

    T_RC = data['T_RC']
    param_bounds = data['param_lim']
    
    # Convert bounds from dict form to tuples (A_min, A_max), (T2_min, T2_max)
    lower_bounds = [val[0] for val in param_bounds.values()]
    upper_bounds = [val[1] for val in param_bounds.values()]

    # Initial guess
    p0 = [np.max(volt), (lower_bounds[1] + upper_bounds[1]) / 2, 3, 0.01, 0.1]

    # Fit using curve_fit
    popt, pcov = curve_fit(
        fit_function,
        time,
        volt,
        sigma=sigma_volt,
        p0=p0,
        bounds=(lower_bounds, upper_bounds),
        absolute_sigma=True
    )

    # Residuals and fit statistics
    residuals = volt - fit_function(time, *popt)
    chi2_val = np.sum((residuals / sigma_volt) ** 2)
    dof = len(time) - len(popt)
    chi2_red = chi2_val / dof
    p_val = 1 - chi2.cdf(chi2_val, dof)

    # Parameter errors
    perr = np.sqrt(np.diag(pcov))
    param_names = [0, 1, 2, 3, 4]
    param_dict = {
        i: (
            rt.round_respect_to_error(val, err),
            rt.sig_digits_round(err)
            )
            for i, val, err in zip(param_names, popt, perr)
        }

    stat_dict = {
        'chi2_red': rt.sig_digits_round(chi2_red, n=3),
        'p_value':  rt.sig_digits_round(p_val, n=3)
        }

    T2_Eff_Data[material]['params'] = param_dict
    T2_Eff_Data[material]['statistics'] = stat_dict
    print(param_dict)
    print(stat_dict)

    root_data = (
        data['root_data']['time'],
        data['root_data']['volt'],
        data['root_data']['delta_time'],
        data['root_data']['delta_v']
        )
    root_params = {i: val for i, val in zip(param_names, popt)}
    fit_str = "[0] * (1 - exp(- (x - [3]) / [4])) * exp(- (x - [3]) / [1]) + [2]"
    titles = {'title': f'Voltage as a function of time in {material}', 'x_title': 'Time [ms]', 'y_title': 'V [Volt]'}
    x_range = 0, 1.1 * max(root_data[0])
    root_file_name = plot_directory + f'root_T2_Eff_{material}'

    t2_eff_canvas = rt.draw_canvas(
        root_data, titles,fit_str, 
        x_range, root_params,
        file_name=root_file_name, file_type='.eps')

    # Plot result
    if save_plt:
        plt.figure(figsize=(8, 5))
        # plt.errorbar(time, volt, xerr=sigma_time, yerr=sigma_volt, fmt='o', label='Data', alpha=0.6)
        plt.plot(time, volt, 'o', label='Data', alpha=0.6)

        x_fit = np.linspace(0, 1.1 * max(time), 500)
        y_fit = fit_function(x_fit, *popt)  
        label = f'Fit: A={popt[0]:.2f}, T2={popt[1]:.2f}, C={popt[2]:.2f}, t0={popt[3]:.2f}, T_RC={popt[4]:.2f}'
        plt.plot(x_fit, y_fit, 'r-', label=label)

        plt.title(titles['title'])
        plt.xlabel(titles['x_title'])
        plt.ylabel(titles['y_title'])
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(plot_directory + f'plt_T2_Eff_{material}.png')
        # plt.show()
        plt.close()



with open(T2_eff_path, 'w') as f:
    json.dump(T2_Eff_Data, f, indent=4)


    
