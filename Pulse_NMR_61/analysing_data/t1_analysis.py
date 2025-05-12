import sys
import os
import json
from tqdm import tqdm

sys.path.append(os.path.abspath('../..'))
from utils import root_tools as rt



T1_path = 'Pulse_NMR_61/create_databases/T1_Data.json'
with open(T1_path, "r") as f:
    T1_Data = json.load(f)


plot_directory = 'Pulse_NMR_61/Plots/T1/'
for material, data in tqdm(T1_Data.items()):
    # if material in ('8 para', '4 para', '2 para', '1 para', '0.5 para', '0.125 para', 'water', 'glycerine'): continue
    print(material)
    # if material != '8 para': continue
    results = data['tau'], data['volt'], data['delta_tau'], data['delta_v']
    titles = {'title': f'Peak voltage as a function of time delay in {material}', 'x_title': '#tau [ms]', 'y_title': 'V [Volt]'}
    fit_str = 'abs([0] * (1 - 2 * exp(- x / [1])))'
    
    x_range = 0, 1.1 * max(data['tau'])
    print(data['param_lim'])
    file_name = plot_directory + f'T1_{material}'

    t1_c = rt.draw_canvas(results, titles, fit_str, x_range, data['param_lim'], file_name=file_name, file_type='.png')

    fit_func = t1_c['fit']
    T1_Data[material]['params'] = {
        f'par{i}': (fit_func.GetParameter(i), fit_func.GetParError(i))
        for i in range(fit_func.GetNpar())
    }
    T1_Data[material]['statistics'] = t1_c['statistics']
    
with open(T1_path, 'w') as f:
    json.dump(T1_Data, f, indent=4)
