import sys
import os
# Add the parent directory to Python's path
sys.path.append(os.path.abspath('../../..'))

import json
from tqdm import tqdm
import pandas as pd

from utils import pandas_tools as pt

filename = "Pulse_NMR_61/Measurements/Measurements_day_3.xlsx"
xls = pd.ExcelFile(filename)

T2_Database = {}
time_col = 'AA'
time_idx = pt.excel_col_to_index(time_col)
header_row = 7

for sheet_name in tqdm(xls.sheet_names):
    if sheet_name in ('question'): continue
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # Extract full columns AA and AB
    time = df.iloc[header_row + 1:, time_idx].dropna() * 1e3  # Convert to milliseconds
    volt = df.iloc[header_row + 1:, time_idx + 1].dropna()

    mask = time >= 0
    time = time[mask]
    volt = volt[mask]

    tau = df.iloc[3, time_idx]       # Cell AA5
    repetition_time = df.iloc[3, time_idx + 3]  # Cell AD5 → index 29

    T2_Database[sheet_name] = {
        'time': time.tolist(),
        'volt': volt.tolist(),
        'repetition_time': repetition_time,
        'tau': tau
    }

output_directory = "Pulse_NMR_61/create_databases/"
output_file_path = output_directory + "T2_Data.json"
with open(output_file_path, "w") as f:
    json.dump(T2_Database, f, indent=4)