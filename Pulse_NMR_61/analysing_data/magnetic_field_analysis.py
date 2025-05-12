import sys
import os
import ast  # for safely parsing list strings
import json
import pandas as pd
from uncertainties import ufloat

sys.path.append(os.path.abspath('../..'))
from utils import root_tools as rt

df = pd.read_csv("Pulse_NMR_61/create_databases/all_T.csv") 

# Parse the list strings into actual Python lists
df['T2'] = df['T2'].apply(ast.literal_eval)
df['T2_Eff'] = df['T2_Eff'].apply(ast.literal_eval)

# Extract values and errors
t2_vals = [entry[0] for entry in df['T2']]
t2_errs = [entry[1] for entry in df['T2']]

t2_eff_vals = [entry[0] for entry in df['T2_Eff']]
t2_eff_errs = [entry[1] for entry in df['T2_Eff']]

experiment = t2_vals, t2_eff_vals, t2_errs, t2_eff_errs


plot_directory = 'Pulse_NMR_61/Plots/T2_eff/T2_eff_against_T2/'
file_name = plot_directory + 'Magnetic_field_variance'
titles = {'title': 'T_{2}^{*} as a function of T_{2}', 'x_title': 'T_{2} [ms]', 'y_title': 'T_{2}^{*} [ms]'}
x_range = (0, 1.1 * max(t2_vals))
fit_str = 'x / ([0] * x + 1)'
par_limits = {0: (0, 20)}

canvas = rt.draw_canvas(experiment, titles, fit_str, x_range, par_limits, file_name=file_name, file_type='.eps')
Param_list = canvas['fitted_params']['par0']
chi2_red = canvas['statistics']['chi2_red']
p_val = canvas['statistics']['p_value']

gamma = ufloat(4.255, 0.034)
p0 = ufloat(*Param_list)
Delta_B = p0 / gamma


# Convert to dict format
data = {
    "gamma": [gamma.n, gamma.s],
    "Delta_B": [Delta_B.n, Delta_B.s],
    "p0": [p0.n, p0.s],
    "statistics": {
            "chi2_red": chi2_red,
            "p_value": p_val
            }
}

# Save to JSON
with open("Pulse_NMR_61/create_databases/magnetic_field_std.json", "w") as f:
    json.dump(data, f, indent=4)
