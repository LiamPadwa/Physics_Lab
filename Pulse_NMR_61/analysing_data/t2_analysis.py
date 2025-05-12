import sys
import os
import json
from tqdm import tqdm

sys.path.append(os.path.abspath('../..'))
from utils import root_tools as rt


T2_path = 'Pulse_NMR_61/create_databases/T2_Data.json'
plot_directory = 'Pulse_NMR_61/Plots/T2/'

with open(T2_path, "r") as f:
    T2_Data = json.load(f)


for material, data in tqdm(T2_Data.items()):
    print(material)
    results = data['x_peak'], data['y_peak'], data['delta_t'], data['delta_v']
    titles = {'title': f'Envelope of voltage as a function of time in {material}', 'x_title': 't [ms]', 'y_title': 'V [Volt]'}
    par_limits = {0: (10, 50), 1: (1, 800), 2: (1, 8)}
    x_range = 0, 1.1 * max(data['x_peak'])
    fit_str = '[0] * exp(- x / [1]) + [2]'
    file_name = plot_directory + f'T2_{material}'

    t2_c = rt.draw_canvas(
        results, titles,
        fit_str, x_range,
        par_limits=par_limits,
        file_name=file_name, file_type='.png')

    fit_func = t2_c['fit']
    T2_Data[material]['param_lim'] = par_limits
    T2_Data[material]['params'] = t2_c['fitted_params']
    T2_Data[material]['statistics'] = t2_c['statistics']

# with open(T2_path, 'w') as f:
#     json.dump(T2_Data, f, indent=4)