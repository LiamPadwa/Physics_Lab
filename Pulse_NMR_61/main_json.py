import subprocess
import os
from time import time

start_time = time()
# List your Python scripts in the desired order
scripts = [
    "Pulse_NMR_61/create_databases/create_T1_database.py",
    "Pulse_NMR_61/create_databases/create_T2_database.py",
    "Pulse_NMR_61/create_databases/create_T2_eff_database.py",
    "Pulse_NMR_61/analysing_data/t1_analysis.py",
    "Pulse_NMR_61/analysing_data/t2_analysis_peaks.py",
    "Pulse_NMR_61/analysing_data/t2_analysis.py",
    "Pulse_NMR_61/analysing_data/t2_eff_analysis.py",
    "Pulse_NMR_61/create_databases/create_all_T_csv.py",
    "Pulse_NMR_61/analysing_data/magnetic_field_analysis.py"
]

# Loop through and run each script
for path in scripts:
    script = os.path.basename(path)
    print(f"Running {script}...")
    result = subprocess.run(["python", path])
    if result.returncode != 0:
        print(f"Error running {path}, stopped.")
        break
    print(f"Finished {script}.\n")

run_time = time() - start_time

if run_time >= 60:
    minutes = int(run_time // 60)
    seconds = run_time % 60
    print(f"Data analysis took {minutes} minutes and {seconds:.2f} seconds.")
else:
    print(f"Data analysis took {run_time:.2f} seconds.")