import json
import pandas as pd

databases_dir: str = '/Users/liam/Documents/Lab_C/Pulse_NMR_61/create_databases/'
t1_path: str = databases_dir + 'T1_Data.json'
t2_path: str = databases_dir + 'T2_Data.json'
t2_eff_path: str = databases_dir + 'T2_Eff_Data.json'

with open(t1_path, "r") as f:
    T1_Data: dict = json.load(f)
with open(t2_path, "r") as f:
    T2_Data : dict = json.load(f)
with open(t2_eff_path, "r") as f:
    T2_Eff_Data: dict = json.load(f)

cols_results: list = ['material', 'T1', 'T2', 'T2_Eff']
rows_results: dict = []

for material, data in T1_Data.items():
    T1_list = data['params']['par1']

    data2 = T2_Data[material]
    T2_list = data2['params']['par1']

    data_eff = T2_Eff_Data[material]
    T2_eff_list= [data_eff['params']['1'][0], data_eff['params']['1'][1]*1e3]

    rows_results.append({
        'material': material,
        'T1': T1_list,
        'T2': T2_list,
        'T2_Eff': T2_eff_list
    })

df_res = pd.DataFrame(rows_results, columns=cols_results)
df_res.to_csv('/Users/liam/Documents/Lab_C/Pulse_NMR_61/create_databases/all_T.csv', index=False)