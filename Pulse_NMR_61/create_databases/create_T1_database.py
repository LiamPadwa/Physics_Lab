import sys
import os
sys.path.append(os.path.abspath('../../..'))

import json
from tqdm import tqdm
import pandas as pd
import numpy as np

from utils import pandas_tools as pt

filename = "Pulse_NMR_61/Measurements/Measurements_day_3.xlsx"
xls = pd.ExcelFile(filename)

T1_Database = {}
time_col = 'T'
time_idx = pt.excel_col_to_index(time_col)
header_row = 5
end_row = 18

for sheet_name in tqdm(xls.sheet_names):
    if sheet_name in ('question'): continue
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # Extract full columns
    tau = df.iloc[header_row + 1: end_row, time_idx].dropna()
    volt = df.iloc[header_row + 1: end_row, time_idx + 2].dropna()

    delta_tau = df.iloc[header_row + 1: end_row, time_idx + 1].dropna()
    delta_v = df.iloc[header_row + 1: end_row, time_idx + 3].dropna()

    T1 = tau[volt.idxmin()] / np.log(2)

    param_lim = {0: (0.8*max(volt), 1.2*max(volt)), 1: (0.9*T1, 1.1*T1)}

    T1_Database[sheet_name] = {
        'tau': tau.tolist(),
        'volt': volt.tolist(),
        'delta_tau': delta_tau.tolist(),
        'delta_v': delta_v.tolist(),
        'param_lim': param_lim
    }

output_directory = "Pulse_NMR_61/create_databases/"
output_file_path = output_directory + f"T1_Data.json"
with open(output_file_path, "w") as f:
    json.dump(T1_Database, f, indent=4)