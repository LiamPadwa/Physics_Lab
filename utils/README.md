# Utils Package

A collection of utility functions for data analysis and visualisation, particularly focused on handling experimental data and ROOT-based analysis.

## Overview

This package provides two modules:

1. `pandas_tools.py`: Utilities for data manipulation and analysis using pandas
2. `root_tools.py`: Tools for ROOT-based data analysis and visualisation

## pandas_tools

### Functions

- `extract_xy_data_from_excel(filename, sheet_name, x_col, y_col, header_row)`: Extracts X and Y numerical data from Excel files
- `smooth_xy_data(x, y, window_length=101, polyorder=3)`: Smooths data using Savitzky-Golay filter
- `get_peaks(x, y, min_time_between_peaks, min_height, prominence=0.5)`: Identifies peaks in data with specified constraints
- `excel_col_to_index(col)`: Converts Excel-style column labels to zero-based indices
- `index_to_excel_col(index)`: Converts zero-based indices to Excel-style column labels

## root_tools

### Functions

#### Data Generation and Fitting
- `generate_data_points(x_data, y_data, delta_x, delta_y)`: Creates TGraphErrors objects with error bars
- `create_tf1(fit_str, fit_name, x_min, x_max, params, colour=2)`: Creates ROOT TF1 objects
- `fit_custom(graph, fit_str, fit_name, x_min=0, x_max=10, colour=2, par_limits=None)`: Fits custom functions to data
- `fit_linear(graph, name, colour=0)`: Performs linear fits

#### Visualization
- `generate_residuals(fitline, x_data, y_data, delta_x, delta_y)`: Generates residual plots
- `create_residuals_canvas(logy=False)`: Creates canvas with main plot and residuals
- `draw_canvas(data, titles, fit_str, x_range, par_limits, file_name=None, file_type='.png')`: Creates complete plots with fits and residuals

#### Utility Functions
- `sig_digits_round(a, n=2)`: Rounds numbers to significant digits
- `round_respect_to_error(a, err, n=2)`: Rounds numbers respecting error bars
- `ufloat_to_str(measured, n=2)`: Formats uncertainty values as strings
- `save_canvas(canvas, file_name, recreate=False, filetype='.png')`: Saves ROOT canvases to files

## Dependencies

- pandas
- numpy
- ROOT
- uncertainties
- scipy
- colorama
