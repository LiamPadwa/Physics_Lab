import pandas as pd
import numpy as np
from uncertainties import ufloat
from scipy.signal import find_peaks, savgol_filter

print('PANDAS TOOLS LIBRARY')

def extract_xy_data_from_excel(
    filename: str,
    sheet_name: str,
    x_col: str,
    y_col: str,
    header_row: int
    ) -> tuple[np.ndarray, np.ndarray]:
    """
    Extracts X and Y numerical data from specific columns in an Excel sheet,
    starting from a given header row.

    Args:
        filename (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to read.
        x_col (str): Excel-style column letter for the X data (e.g., 'A').
        y_col (str): Excel-style column letter for the Y data (e.g., 'B').
        header_row (int): Index of the row where actual data starts (0-based).

    Returns:
        tuple[np.ndarray, np.ndarray]: Two NumPy arrays: X values and Y values,
        with rows filtered to only include those where X >= 0.
    """
    # Load the Excel sheet with no automatic header parsing
    df = pd.read_excel(filename, sheet_name=sheet_name, header=None)

    # Convert Excel column letters to zero-based indices
    x_idx = excel_col_to_index(x_col)
    y_idx = excel_col_to_index(y_col)

    # Extract X and Y columns starting from the header row
    x = df.iloc[header_row:, x_idx]
    y = df.iloc[header_row:, y_idx]

    # Filter out rows where X is negative or NaN
    valid_mask = x >= 0
    x = x[valid_mask].to_numpy()
    y = y[valid_mask].to_numpy()

    return x, y

def smooth_xy_data(x: np.ndarray, y: np.ndarray, window_length: int = 101, polyorder: int = 3):
    """
    Smooth y-data using Savitzky-Golay filter.

    Parameters:
        x (np.ndarray): Independent variable (e.g., time)
        y (np.ndarray): Dependent variable (e.g., voltage)
        window_length (int): Length of the filter window (must be odd and > polyorder)
        polyorder (int): Polynomial order to use in the filter

    Returns:
        x (np.ndarray): Original x data (unchanged)
        y_smooth (np.ndarray): Smoothed y data
    """
    if len(y) < window_length:
        raise ValueError(f"Window length ({window_length}) is larger than data size ({len(y)}).")

    if window_length % 2 == 0:
        window_length += 1  # ensure it's odd

    y_smooth = savgol_filter(y, window_length, polyorder)
    return x, y_smooth

def get_peaks(x: np.ndarray, y: np.ndarray, min_time_between_peaks: float, min_height: float, prominence: float = 0.5):
    # Estimate sample spacing and compute required peak distance in samples
    dt = np.mean(np.diff(x))
    min_distance_samples = int(min_time_between_peaks / dt)

    # Find peaks with constraints
    peak_indices, properties = find_peaks(y, height=min_height, distance=min_distance_samples, prominence=prominence)

    x_peaks = x[peak_indices]
    y_peaks = y[peak_indices]

    return x_peaks, y_peaks

def excel_col_to_index(col: str) -> int:
    """
    Convert an Excel-style column label (e.g., 'A', 'BP') to a 0-based index.

    Args:
        col (str): Column label using Excel notation (e.g., 'A', 'Z', 'AA', 'BP').

    Returns:
        int: Zero-based column index (e.g., 'A' -> 0, 'B' -> 1, ..., 'AA' -> 26).

    Examples:
        >>> excel_col_to_index('A')
        0
        >>> excel_col_to_index('Z')
        25
        >>> excel_col_to_index('AA')
        26
    """
    col = col.upper()
    index = 0
    for i, c in enumerate(reversed(col)):
        index += (ord(c) - ord('A') + 1) * (26 ** i)
    return index - 1  # Convert to 0-based index

def index_to_excel_col(index: int) -> str:
    """Convert 0-based column index to Excel-style column label (e.g., 0 → 'A', 27 → 'AB')."""
    if index < 0:
        raise ValueError("Index must be non-negative")
    col = ""
    index += 1  # Convert to 1-based index for Excel-style logic
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        col = chr(65 + remainder) + col
    return col


if __name__ == '__main__':
    pass