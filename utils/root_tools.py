import os
import time
from math import floor, log10
from colorama import Fore, Style
from uncertainties import ufloat
import ROOT
from ROOT import TGraphErrors, TF1

print("ROOT TOOLS LIBRARY")

def generate_data_points(x_data, y_data, delta_x, delta_y):
    # Generate the data points with error bars
    graph = ROOT.TGraphErrors(len(x_data))
    for i, (x, y, dx, dy) in enumerate(zip(x_data, y_data, delta_x, delta_y)):
        graph.SetPoint(i, x, y)
        graph.SetPointError(i, dx, dy)
    
    graph.GetYaxis().CenterTitle()
    return graph

def create_tf1(fit_str, fit_name: str, x_min: float, x_max: float, params: dict[int | str, float], colour=2):
    fit_func: TF1 = ROOT.TF1(fit_name, fit_str, x_min, x_max)
    for i, param_val in params.items():
            if f'[{i}]' not in fit_str:
                raise ValueError(f"Parameter [{i}] not found in fit string: {fit_str}")
            if isinstance(i, str):
                try:
                    i = int(i)
                except ValueError:
                    raise ValueError(f"Cannot convert string '{i}' to integer.")
            fit_func.SetParameter(i, param_val)
    
    fit_func.SetNpx(2000)
    fit_func.SetLineColor(colour)
    return fit_func

def fit_custom(graph: TGraphErrors, fit_str: str, fit_name: str,
               x_min: float = 0, x_max: float = 10, colour=2,
               par_limits: dict[int | str, tuple[float, float]] | None = None) -> TF1:
    """
    Fits a TGraphErrors object using a custom function defined by a fit string.

    Parameters:
        graph (TGraphErrors): The graph to be fitted.
        fit_str (str): The fitting function string in ROOT format (e.g., "[0]*x + [1]").
        fit_name (str): Name assigned to the TF1 fitting object.
        x_min (float, optional): Minimum x-range for the fit. Defaults to 0.
        x_max (float, optional): Maximum x-range for the fit. Defaults to 10.
        colour (int, optional): Line colour for the fit function. Defaults to red.
        par_limits (dict[int, tuple[float, float]], optional): 
            Optional dictionary of parameter limits in the form 
            {param_index: (min, max)}.

    Returns:
        TF1: The fitted TF1 object.

    Raises:
        ValueError: If a parameter index in `par_limits` is not found in `fit_str`.
    """
    fit_func: TF1 = ROOT.TF1(fit_name, fit_str, x_min, x_max)

    if par_limits:
        for i, (par_min, par_max) in par_limits.items():
            if f'[{i}]' not in fit_str:
                raise ValueError(f"Parameter [{i}] not found in fit string: {fit_str}")
            if isinstance(i, str):
                try:
                    i = int(i)
                except ValueError:
                    raise ValueError(f"Cannot convert string '{i}' to integer.")
            fit_func.SetParLimits(i, par_min, par_max)

    graph.Fit(fit_name)
    fit_func.SetLineColor(colour)
    fit_func.SetNpx(2000)
    return fit_func

def fit_linear(graph, name: str, colour=0):
    # Fit the function to the main graph
    funct = ROOT.TF1(name, "[0] * x + [1]", 15, 135)
    #funct.SetParLimits(0, 160., 180.)
    #funct.SetParLimits(1, -5., 5.)
    if colour: funct.SetLineColor(colour)
    graph.Fit(name)
    return funct

def generate_residuals(fitline, x_data, y_data, delta_x, delta_y):
    label_size = 0.035
    res_pad_height = 0.35

    residuals_graph = ROOT.TGraphErrors(len(x_data))
    for i, (x, y, dx, dy) in enumerate(zip(x_data, y_data, delta_x, delta_y)):
        residual = y - fitline.Eval(x)
        residuals_graph.SetPoint(i, x, residual)
        residuals_graph.SetPointError(i, dx, dy)

    residuals_graph.GetXaxis().SetTitleSize(label_size / res_pad_height)

    residuals_graph.GetYaxis().SetTitle('Residuals')
    residuals_graph.GetYaxis().SetTitleSize(0.08)
    residuals_graph.GetYaxis().SetTitleOffset(+0.5)
    residuals_graph.GetYaxis().CenterTitle()
    residuals_graph.SetTitle('')

    # Draw a horizontal line at y=0 in blue
    line = ROOT.TLine(min(x_data), 0, max(x_data), 0)
    line.SetLineColor(4)  # Blue colour

    return residuals_graph, line

def create_residuals_canvas(logy: bool = False):
    # Generate a unique canvas name using a counter
    canvas_name = f"canvas_{hash(time.time())}"
    canvas = ROOT.TCanvas(canvas_name, "", 800, 800)
    
    # Create the main graph's pad
    main_pad = ROOT.TPad("main_pad", "main_pad", 0, 0.3, 1.0, 1.0)
    main_pad.SetTopMargin(0.09)
    main_pad.SetBottomMargin(0.06)
    main_pad.SetGrid()

    if logy: main_pad.SetLogy()

    main_pad.Draw()

    canvas.cd()
    # Create the residuals pad
    residuals_pad = ROOT.TPad("res_pad", "res_pad", 0, 0, 1, 0.3)
    residuals_pad.SetTopMargin(0.06)
    residuals_pad.SetBottomMargin(0.40)
    residuals_pad.SetGrid()
    residuals_pad.Draw()

    return canvas, main_pad, residuals_pad

def draw_canvas(data: tuple, titles: dict[str, str], fit_str, x_range, par_limits, file_name=None, file_type: str = '.png'):
    title, x_title, y_title = titles['title'], titles['x_title'], titles['y_title']
    canvas, main_pad, res_pad = create_residuals_canvas()

    main_pad.cd()
    graph = generate_data_points(*data)
    
    if all(isinstance(v, (tuple, list)) and len(v) == 2 for v in par_limits.values()):
        # Case: all values are tuples of length 2 → (min, max)
        fit_function = fit_custom(graph, fit_str, fit_str,
                                x_min=x_range[0], x_max=x_range[1], par_limits=par_limits)
        
    elif all(isinstance(v, (int, float)) for v in par_limits.values()):
        # Case: all values are single values
        fit_function = create_tf1(fit_str, fit_str, x_range[0], x_range[1], par_limits)
    
    else:
        raise ValueError("par_limits must be either all (min, max) tuples or all single values")

    graph.Draw('AP')
    fit_function.Draw('same')
    graph.GetYaxis().SetTitle(y_title)
    graph.SetTitle(title)

    res_pad.cd()
    res, line = generate_residuals(fit_function, *data)
    res.Draw('AP')
    line.Draw('same')
    res.GetXaxis().SetTitle(x_title)

    try:
        chi2_red: float = sig_digits_round(fit_function.GetChisquare() / fit_function.GetNDF(), n=3)
    except ZeroDivisionError:
        chi2_red = 0

    p_value: float = sig_digits_round(fit_function.GetProb(), n=3)
    fitted_params: dict = {
        f'par{i}': (
            round_respect_to_error(fit_function.GetParameter(i), fit_function.GetParError(i)),
            sig_digits_round(fit_function.GetParError(i))
            )
        for i in range(fit_function.GetNpar())
    }

    print(f'Fitting function(x): {fit_str}')
    print(f"Chi2_Red = {chi2_red}")
    print(f"P_value = {p_value}")

    canvas.Update()
    if file_name:
        save_canvas(canvas, file_name, recreate=True, filetype=file_type)
    canvas.Draw()
    return {
        'canvas': canvas,
        'graph': graph,
        'fit': fit_function,
        'residuals': res,
        'res_line': line,
        'fitted_params': fitted_params,
        'statistics': {
            'chi2_red': chi2_red,
            'p_value':  p_value
        }
    }

def sig_digits_round(a: float, n: int = 2) -> float | int:
    if a == 0:
        return 0
    rounded_num = round(a, -int(floor(log10(abs(a)))) + (n - 1))
    return int(rounded_num) if int(rounded_num) == rounded_num else rounded_num

def round_respect_to_error(a: float, err: float, n: int = 2) -> float | int:
    rounded_err = sig_digits_round(err, n)
    err_str = str(rounded_err)
    m = len(err_str)
    if '.' in err_str: m -= 1
    return sig_digits_round(a, m)

def ufloat_to_str(measured: ufloat, n: int = 2) -> str:
    std:  float | int = sig_digits_round(measured.s, n)
    norm: float | int = round_respect_to_error(measured.n, err=std, n=n)
    return f'{norm} \pm {std}'

def print_fitting_params():
    pass

def print_title_graphics_specs(title):
    # get the title font (an integer code) and title size (a float fraction of pad height)
    font_code = title.GetTitleFont()
    title_size = title.GetTitleSize()

    # you can also check the label font/size
    label_font  = title.GetLabelFont()
    label_size  = title.GetLabelSize()

    print(f"Title font code: {font_code}")
    print(f"Title size:      {title_size:.3f}")
    print(f"Label font code: {label_font}")
    print(f"Label size:      {label_size:.3f}")

def save_canvas(canvas, file_name, recreate=False, filetype: str='.png'):
    # Adjusting filetype
    filetype = filetype.lower()
    if '.' not in filetype: filetype = '.' + filetype

    fig_path = file_name + filetype
    if not recreate and os.path.exists(fig_path):
        print(f"{Fore.RED}The {filetype[1:].upper()} file '{file_name}' already exists. Skipping the save.{Style.RESET_ALL}")
    else:
        canvas.SaveAs(fig_path)
        print(f"{Fore.GREEN}The {filetype[1:].upper()} file '{file_name}' has been saved.{Style.RESET_ALL}")

if __name__ == '__main__':
    check_list = [(3.48387438, 0.00236), (3.48387, 0.23), (5673, 348)]
    for num, std in check_list:
        print(round_respect_to_error(num, std), sig_digits_round(std))