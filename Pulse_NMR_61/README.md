
# Pulsed NMR Data Analysis

This repository contains scripts for analysing measurements from a **Pulsed NMR** experiment. The main script processes an Excel file containing experimental data and generates various plots and calculations related to relaxation times and magnetic field characteristics.

### Abstract:
With an apparatus designed for undergraduate students, we measured the gyromagnetic ratio of the proton to $\gamma_p = 4.255 \pm 0.034 \text{ MHz/KGs}$, which is in agreement to the accepted value of $\gamma_p = 4.258 \text{ MHz/KGs}$.
We achieved this by measuring the Larmor frequency of pure water in a uniform magnetic field. In addition, we measured both the longitudinal and transverse spin relaxation times of nine liquid samples with varying viscosities and concentrations of paramagnetic ions. The results exhibited the expected trend of faster relaxation with increasing viscosity and paramagnetic ion concentration.
The measured relaxation times allowed us to estimate the small inhomogeneities of the magnetic field, yielding $\Delta B_0 = 1.50 \pm 0.20 \text{ Gs}$, two orders of magnitude finer than the resolution of the available gaussmeter.

### Main Functionality:
The main function of the repository runs a series of Python scripts that perform the following tasks:

1. **T1, T2, and T2* Relaxation Analysis**: The data from the Pulsed NMR experiment is processed to calculate the spin-lattice relaxation time (T1), spin-spin relaxation time (T2), and effective relaxation time (T2*) for all samples.

2. **Gyromagnetic Ratio Calculation**: The gyromagnetic ratios of the sample materials are calculated.

3. **Magnetic Field Inhomogeneity Estimation**: The analysis includes an estimation of the magnetic field inhomogeneity.

4. **Data Plotting**: The script generates fitted plots for extracting T1, T2, T2* relaxation times for all samples.

### Script Flow:

The main script in the repository runs a sequence of Python scripts in the following order:
1. **Database Creation**:
    - `create_T1_database.py`
    - `create_T2_database.py`
    - `create_T2_eff_database.py`
    - `create_all_T_csv.py`
2. **Data Analysis**:
    - `t1_analysis.py`: Analyses and plots the fitted data, extracting T1 relaxation times.
    - `t2_analysis_peaks.py`: Extractes the envelopes from the measured signals
    - `t2_analysis.py`: Analyses and plots the fitted data, extracting T2 relaxation times.
    - `t2_eff_analysis.py`: Analyses and plots the fitted data, extracting the effective T2 relaxation times.
    - `magnetic_field_analysis.py`: Analyses magnetic field inhomogeneity and computes the gyromagnetic ratios.

### How It Works:
- **Input**: The scripts read experimental data from an Excel file.
- **Processing**: Each script performs data analysis, creating databases and extracting important physical parameters.
- **Output**: The analysis results include plots and a summary of relaxation times (T1, T2, T2*) and estimated magnetic field inhomogeneity.

### Estimated Run Time:
The total time taken for the data analysis will be displayed after the scripts finish executing. For example:
```bash
Data analysis took 1 minute and 21 seconds.
```

### Requirements:
- `ROOT` must be installed and importable in the Python environment.
- Requirements and dependencies are listed in `pyproject.toml`

### Notes:
Ensure the Excel file is structured exactly like the example in the `\Measurements` directory, with each sample placed on a separate sheet.
