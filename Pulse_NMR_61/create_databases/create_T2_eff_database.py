import sys
import os
# Add the parent directory to Python's path
sys.path.append(os.path.abspath('../../..'))


import json
from tqdm import tqdm
import pandas as pd
import numpy as np

from utils import pandas_tools as pt

filename = "Pulse_NMR_61/Measurements/Measurements_day_3.xlsx"
xls = pd.ExcelFile(filename)

T2_Database = {}
time_col = 'K'
time_idx = pt.excel_col_to_index(time_col)
header_row = 5

for sheet_name in tqdm(xls.sheet_names):
    if sheet_name in ('question'): continue
    df = pd.read_excel(xls, sheet_name=sheet_name)

    time = df.iloc[header_row + 1:, time_idx].dropna() * 1e3
    volt = df.iloc[header_row + 1:, time_idx + 1].dropna()

    # Find first index where volt > 5
    v_min: float = 5. if sheet_name == '0.5 para' else 4.
    first_valid_idx = volt[volt > v_min].index.min()

    # Apply mask: keep data only after (and including) first_valid_idx
    mask_v_min = time.index >= first_valid_idx
    time = time[mask_v_min]
    volt = volt[mask_v_min]

    mask_t0 = time >= 0
    time = time[mask_t0]
    volt = volt[mask_t0]

    time = time.reset_index(drop=True)
    volt = volt.reset_index(drop=True) 
    
    dt, dv = 0.01 / np.sqrt(12), 0.2 / np.sqrt(12)
    delta_time = [dt] * len(time)
    delta_v    = [dv] * len(volt)

    # Assume time and volt are already defined Series with aligned indices
    max_idx = volt.idxmax()

    # Split at global max index
    before_max = time.index <= max_idx
    after_max = time.index > max_idx

    # Select parts
    time_before = time[before_max].iloc[::50]
    volt_before = volt[before_max].iloc[::50]

    time_after = time[after_max].iloc[::300]
    volt_after = volt[after_max].iloc[::300]

    # Combine
    time_root = pd.concat([time_before, time_after])
    volt_root = pd.concat([volt_before, volt_after])
    delta_t_root = [dt] * len(time_root)
    delta_v_root = [dv] * len(volt_root)
    root_dic = {
        "time": time_root.tolist(),
        "volt": volt_root.tolist(),
        "delta_time": delta_t_root,
        "delta_v": delta_v_root
    }

    T_RC = df.iloc[3, time_idx - 1]

    param_lim = {0: (15, 70), 1: (0.01, 1), 2: (1, 8), 3: (-0.3, 0.3), 4: (0.05, 0.5)}
    # 0: V0, 1: T2*, 2: C, 3: t0, 4: T_RC
    T2_Database[sheet_name] = {
        'time': time.tolist(),
        'volt': volt.tolist(),
        'delta_time': delta_time,
        'delta_v': delta_v,
        'root_data': root_dic,
        'T_RC': T_RC,
        'param_lim': param_lim
    }

output_directory = "Pulse_NMR_61/create_databases/"
output_file_path = output_directory + "T2_Eff_Data.json"
with open(output_file_path, "w") as f:
    json.dump(T2_Database, f, indent=4)