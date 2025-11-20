import os
import re
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# =============================
# Configuration
# =============================
CHIP_FILES = {
    "5WT1": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT2": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT3": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT4": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT5": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT6": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
    "5WT7": ["T3_VSD_ISID_v1.csv", "T4_VSD_ISID_v1.csv", "T5_VSD_ISID_v1.csv"],
}

DILUTION_MAP = {
    "5WT7": (7, "1:7"),
    "5WT6": (6, "1:6"),
    "5WT5": (5, "1:5"),
    "5WT4": (4, "1:4"),
    "5WT3": (3, "1:3"),
    "5WT2": (2, "1:2"),
    "5WT1": (1, "1:1"),
}

TARGET_VSG = 0.4
VERBOSE = False

APPLY_FILTER = True
FILTER_WINDOW = 5
FILTER_PASSES = 1
PAD_MODE = "reflect"
ZERO_PHASE = True
EDGE_PAD_FOR_FITS = (FILTER_WINDOW // 2) if APPLY_FILTER else 0

SHOW_CRITICAL = True
SHOW_SUMMARY = True
SHOW_NONCRITICAL = False
OHMIC_VCAP = 0.10
SAT_FRAC_START = 0.70

GM_WINDOW = 3
GM_POSITIVE_BY_CONVENTION = True

# Baseline noise data
baseline_ID = np.array(
    [
        -3.01e-10,
        8.16e-10,
        -1.84e-10,
        -6.07e-10,
        8.66e-10,
        -4.88e-10,
        -3.56e-10,
        7.92e-10,
        -9.10e-11,
        -9.08e-10,
        4.83e-10,
        3.14e-10,
        -7.53e-10,
        1.38e-10,
        6.38e-10,
        -8.96e-10,
        4.74e-10,
        4.71e-10,
        -8.10e-10,
        9.40e-11,
        8.86e-10,
        -5.16e-10,
        -3.30e-10,
        7.97e-10,
        -1.20e-10,
        -6.43e-10,
        8.83e-10,
        -4.56e-10,
        -3.78e-10,
        7.72e-10,
        -8.90e-11,
        -8.25e-10,
        4.94e-10,
        3.21e-10,
        -8.03e-10,
        9.20e-11,
        5.62e-10,
        -8.81e-10,
        4.54e-10,
        3.79e-10,
        -7.80e-10,
        7.00e-11,
        8.86e-10,
        -4.82e-10,
        -3.30e-10,
        7.95e-10,
        -1.28e-10,
        -6.69e-10,
        9.01e-10,
        -4.55e-10,
        -3.76e-10,
        7.78e-10,
        -6.50e-11,
        -8.64e-10,
        4.96e-10,
        3.19e-10,
        -7.90e-10,
        1.04e-10,
        6.43e-10,
        -8.83e-10,
        4.31e-10,
    ]
)

BASELINE_ID = baseline_ID
baseline_Id_detrended = BASELINE_ID - np.median(BASELINE_ID)
BASELINE_RMS = float(np.std(baseline_Id_detrended))

TWO_SLOPE_WINDOWS = {
    "5WT1": {"steeper": (2.8, 3.1), "flatter": (3.4, 3.5)},
    "5WT2": {"steeper": (2.8, 3.1), "flatter": (3.4, 3.5)},
    "5WT3": {"steeper": (2.8, 3.1), "flatter": (3.4, 3.5)},
    "5WT4": {"steeper": (2.8, 3.1), "flatter": (3.4, 3.5)},
    "5WT5": {"steeper": (2.8, 3.1), "flatter": (3.4, 3.5)},
    "5WT6": {"steeper": (2.8, 3.1), "flatter": (3.4, 3.5)},
    "5WT7": {"steeper": (2.8, 3.1), "flatter": (3.4, 3.5)},
}


# =============================
# Helper Functions
# =============================
def clean_vgs(val):
    try:
        m = re.search(r"[-+]?[0-9]*\.?[0-9]+", str(val))
        return float(m.group(0)) if m else None
    except Exception:
        return None


def extract_values(file_path):
    """Extract Vd, VGS, Is, Id, and ISD from CSV file."""
    try:
        df0 = pd.read_csv(file_path, header=None)
        vgs_vals = [clean_vgs(v) for v in df0.iloc[4, 1:].tolist()]
        mid = len(vgs_vals) // 2
        vgs_vals = vgs_vals[:mid]

        df = pd.read_csv(file_path, skiprows=4).apply(pd.to_numeric, errors="coerce")
        vd = df.iloc[:, 0].tolist()
        is_df = df.iloc[:, 1 : mid + 1]
        id_df = df.iloc[:, mid + 1 : 2 * mid + 1]
        isd_df = is_df.subtract(id_df.values)

        if VERBOSE:
            base = os.path.basename(file_path)
            print(f"[{base}] VGS (Is/Id blocks): {vgs_vals}")
        return vd, vgs_vals, is_df, id_df, isd_df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None, None, None, None


def average_isd_over_files(chip, files, folder):
    vd_vals = vgs_vals = None
    acc = None
    n_found = 0
    for fn in files:
        fp = os.path.join(folder, chip, fn)
        if not os.path.exists(fp):
            if VERBOSE:
                print(f"Missing: {fp}")
            continue
        vd, vgs, _, _, isd = extract_values(fp)
        if isd is None:
            continue
        if acc is None:
            acc = isd.copy()
            vd_vals = vd
            vgs_vals = vgs
        else:
            acc = acc.add(isd, fill_value=np.nan)
        n_found += 1
    if acc is None or n_found == 0:
        return None, None, None
    return vd_vals, vgs_vals, acc / n_found


def _ma_once(y, window=5, pad_mode="reflect"):
    window = int(max(1, window))
    if window == 1:
        return y.copy()
    half = window // 2
    k = np.ones(window, float) / float(window)
    ypad = np.pad(y, (half, window - 1 - half), mode=pad_mode)
    return np.convolve(ypad, k, mode="valid")


def nan_safe_moving_average(y, window=5, passes=1, pad_mode="reflect", zero_phase=True):
    """NaN-safe centered MA with edge padding."""
    y = np.asarray(y, float)
    if window <= 1 or passes <= 0:
        return y.copy()
    x = np.arange(len(y))
    m = np.isfinite(y)
    yf = y.copy()
    if not np.all(m):
        yf[~m] = np.interp(x[~m], x[m], y[m])
    z = yf
    passes = int(max(1, passes))
    for _ in range(passes):
        if zero_phase:
            z = _ma_once(z, window, pad_mode)
            z = _ma_once(z[::-1], window, pad_mode)[::-1]
        else:
            z = _ma_once(z, window, pad_mode)
    return z


def apply_filter(traces, window=5, passes=1, pad_mode="reflect", zero_phase=True):
    if not APPLY_FILTER:
        return {k: (v[0], v[1]) for k, v in traces.items()}
    out = {}
    for chip, (vsd, isd) in traces.items():
        out[chip] = (
            vsd,
            nan_safe_moving_average(
                isd,
                window=window,
                passes=passes,
                pad_mode=pad_mode,
                zero_phase=zero_phase,
            ),
        )
    return out


def build_traces_at_vsg(avg_by_chip, target_vsg, interpret_as_vsg=True):
    raw = float(clean_vgs(target_vsg))
    target_vgs = -abs(raw) if interpret_as_vsg else raw
    traces = {}
    for chip, (vd_vals, vgs_vals, avg_isd) in avg_by_chip.items():
        idx = next(
            (i for i, v in enumerate(vgs_vals) if np.isclose(v, target_vgs, atol=1e-6)),
            None,
        )
        if idx is None:
            if VERBOSE:
                print(f"{chip}: VGS={target_vgs} not found")
            continue
        vsd = -np.asarray(vd_vals, float)
        isd = np.asarray(avg_isd.iloc[:, idx].tolist(), float)
        mask = np.isfinite(vsd) & np.isfinite(isd)
        vsd, isd = vsd[mask], isd[mask]
        order = np.argsort(vsd)
        traces[chip] = (vsd[order], isd[order])
    return traces


def r_squared(y, yhat):
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot if ss_tot != 0 else 0.0


def fit_line(x, y):
    m, b = np.polyfit(x, y, 1)
    return float(m), float(b)


def robust_small_v_fit(Vsd, Isd, v_cap=0.10, max_iter=3, z_thresh=3.0):
    """Linear fit in the small-V (ohmic) region."""
    Vsd = np.asarray(Vsd, float)
    Isd = np.asarray(Isd, float)
    mask = (Vsd >= 0) & (Vsd <= v_cap)
    if mask.sum() < 3:
        k = max(3, int(0.2 * len(Vsd)))
        mask = np.zeros_like(Vsd, dtype=bool)
        mask[:k] = True

    used = mask.copy()
    for _ in range(max_iter):
        if used.sum() < 3:
            break
        m, b = fit_line(Vsd[used], Isd[used])
        yhat = m * Vsd[used] + b
        resid = Isd[used] - yhat
        s = np.std(resid) if np.std(resid) > 0 else 1e-18
        new_used = used.copy()
        idx_used = np.where(used)[0]
        new_used[idx_used[np.abs(resid) > z_thresh * s]] = False
        if np.array_equal(new_used, used):
            break
        used = new_used

    if used.sum() >= 2:
        m, b = fit_line(Vsd[used], Isd[used])
        yhat = m * Vsd[used] + b
        r2 = r_squared(Isd[used], yhat)
        Ron = np.inf if m == 0 else 1.0 / m
    else:
        m = b = 0.0
        r2 = 0.0
        Ron = np.inf

    return float(Ron), float(m), float(b), used, float(r2)


def sat_region_mask(
    Vsd,
    vth=None,
    gate_voltage=0.0,
    frac_start=0.7,
    edge_pad=0,
    chip=None,
    two_slope_windows=None,
):
    """Determine saturation region mask."""
    Vsd = np.asarray(Vsd, float)
    n = len(Vsd)
    mask = None

    if two_slope_windows is not None and chip in two_slope_windows:
        lo, hi = two_slope_windows[chip]["flatter"]
        mask = (Vsd >= lo) & (Vsd <= hi)
        if mask.sum() < 3:
            pad = 0.05
            mask = (Vsd >= (lo - pad)) & (Vsd <= (hi + pad))

    if mask is None or mask.sum() < 3:
        if vth is not None and np.isfinite(vth):
            VOV = abs(gate_voltage - vth)
            mask = Vsd >= VOV
        else:
            start = int(frac_start * n)
            mask = np.zeros(n, dtype=bool)
            mask[start:] = True

    if edge_pad > 0:
        idx = np.where(mask)[0]
        if len(idx) > 0:
            mask[idx[-edge_pad:]] = False
    return mask


def output_params(
    Vsd,
    Isd,
    vth=None,
    gate_voltage=0.0,
    frac_start=0.7,
    vds_ref=None,
    edge_pad=0,
    chip=None,
    two_slope_windows=None,
):
    mask = sat_region_mask(
        Vsd,
        vth=vth,
        gate_voltage=gate_voltage,
        frac_start=frac_start,
        edge_pad=edge_pad,
        chip=chip,
        two_slope_windows=two_slope_windows,
    )
    xs, ys = Vsd[mask], Isd[mask]
    if len(xs) > 2:
        a, b = fit_line(xs, ys)
        gsd = abs(a)
        ro = np.inf if gsd == 0 else 1.0 / gsd
        VA = np.inf if a == 0 else abs(-b / a)
    else:
        a = b = 0.0
        gsd = 0.0
        ro = np.inf
        VA = np.inf
    if vds_ref is None:
        vds_ref = (
            float(np.median(xs)) if len(xs) else (float(Vsd[-1]) if len(Vsd) else 0.0)
        )
    Id_sat_ref = a * vds_ref + b if len(xs) else (Isd[-1] if len(Isd) else 0.0)
    return {
        "gsd": gsd,
        "ro": ro,
        "VA": VA,
        "a": a,
        "b": b,
        "vds_ref": float(vds_ref),
        "Id_sat_ref": float(Id_sat_ref),
        "sat_mask": mask,
    }


def two_slope_intersection(Vsd, Isd, steeper, flatter):
    m1mask = (Vsd >= steeper[0]) & (Vsd <= steeper[1])
    m2mask = (Vsd >= flatter[0]) & (Vsd <= flatter[1])
    if m1mask.sum() < 2 or m2mask.sum() < 2:
        return np.nan, np.nan, (np.nan, np.nan, np.nan, np.nan)
    m1, b1 = fit_line(Vsd[m1mask], Isd[m1mask])
    m2, b2 = fit_line(Vsd[m2mask], Isd[m2mask])
    if np.isclose(m1, m2):
        return np.nan, np.nan, (m1, b1, m2, b2)
    vx = (b2 - b1) / (m1 - m2)
    iy = m1 * vx + b1
    return float(vx), float(iy), (m1, b1, m2, b2)


def compute_snr(signal_A, baseline_trace_A=None, baseline_rms_A=None):
    signal_A = np.asarray(signal_A)
    if baseline_trace_A is not None:
        noise_rms = float(np.std(np.asarray(baseline_trace_A)))
    elif baseline_rms_A is not None:
        noise_rms = float(baseline_rms_A)
    else:
        noise_rms = 1e-12
    signal_rms = float(np.sqrt(np.mean(signal_A**2)))
    snr_linear = signal_rms / max(noise_rms, 1e-18)
    snr_db = 20 * np.log10(max(snr_linear, 1e-18))
    I_det = 3 * noise_rms
    dyn_db = 20 * np.log10(max(np.max(np.abs(signal_A)) / max(I_det, 1e-18), 1e-18))
    return {
        "noise_rms_A": noise_rms,
        "I_det_A": I_det,
        "snr_db": snr_db,
        "dynamic_range_db": dyn_db,
        "signal_rms_A": signal_rms,
    }


def _idsat_for_chip_over_vgs(
    chip, avg_by_chip, two_slope_windows, filt_window, filt_passes, pad_mode, zero_phase
):
    """Compute Id_sat across VGS."""
    vd_vals, vgs_vals, avg_isd = avg_by_chip[chip]
    vgs_vals = list(vgs_vals)
    vsd_base = -np.asarray(vd_vals, float)
    idsat_list, vgs_list = [], []

    w = two_slope_windows.get(chip) if two_slope_windows is not None else None

    for j, vgs in enumerate(vgs_vals):
        isd_col = np.asarray(avg_isd.iloc[:, j].tolist(), float)
        m = np.isfinite(vsd_base) & np.isfinite(isd_col)
        if not np.any(m):
            continue

        vsd = vsd_base[m]
        isd = isd_col[m]
        order = np.argsort(vsd)
        vsd, isd = vsd[order], isd[order]

        isd_f = (
            nan_safe_moving_average(
                isd,
                window=filt_window,
                passes=filt_passes,
                pad_mode=pad_mode,
                zero_phase=zero_phase,
            )
            if APPLY_FILTER
            else isd
        )

        idsat = np.nan
        if w is not None:
            vx, iy, (m1, b1, m2, b2) = two_slope_intersection(
                vsd, isd_f, w["steeper"], w["flatter"]
            )
            if np.isfinite(iy):
                idsat = float(iy)

        if not np.isfinite(idsat):
            out_alt = output_params(
                vsd,
                isd_f,
                vth=None,
                gate_voltage=0.0,
                frac_start=SAT_FRAC_START,
                vds_ref=None,
                edge_pad=EDGE_PAD_FOR_FITS,
                chip=chip,
                two_slope_windows=two_slope_windows,
            )
            idsat = float(out_alt["Id_sat_ref"])

        idsat_list.append(idsat)
        vgs_list.append(float(vgs))

    return np.asarray(vgs_list, float), np.asarray(idsat_list, float)


def _compute_gm_at_target_vgs(chip, target_vsg_abs, avg_by_chip, two_slope_windows):
    """Compute gm = d(Id_sat)/d(VGS) at target VSG."""
    if chip not in avg_by_chip:
        return np.nan, np.nan

    vgs_all, idsat_all = _idsat_for_chip_over_vgs(
        chip,
        avg_by_chip,
        two_slope_windows,
        filt_window=FILTER_WINDOW,
        filt_passes=FILTER_PASSES,
        pad_mode=PAD_MODE,
        zero_phase=ZERO_PHASE,
    )
    if vgs_all.size < 2 or idsat_all.size < 2:
        return np.nan, np.nan

    tgt_vgs = -abs(float(clean_vgs(target_vsg_abs)))

    order = np.argsort(vgs_all)
    vgs_all = vgs_all[order]
    idsat_all = idsat_all[order]

    idx = None
    for i, v in enumerate(vgs_all):
        if np.isclose(v, tgt_vgs, atol=1e-6):
            idx = i
            break
    if idx is None:
        return np.nan, np.nan

    half = max(1, int(GM_WINDOW // 2))
    lo = max(0, idx - half)
    hi = min(len(vgs_all), idx + half + 1)
    if (hi - lo) < 2:
        if idx == 0 and len(vgs_all) >= 2:
            lo, hi = 0, 2
        elif idx == len(vgs_all) - 1 and len(vgs_all) >= 2:
            lo, hi = len(vgs_all) - 2, len(vgs_all)
        else:
            return np.nan, np.nan

    x = vgs_all[lo:hi]
    y = idsat_all[lo:hi]
    if np.any(~np.isfinite(x)) or np.any(~np.isfinite(y)) or (len(x) < 2):
        return np.nan, np.nan

    m, b = fit_line(x, y)
    r2 = r_squared(y, m * x + b)
    gm = abs(m) if GM_POSITIVE_BY_CONVENTION else m
    return float(gm), float(r2)


def analyze_tab(tab_analyze):
    """Main analyze tab interface."""
    folder_path = tk.StringVar()
    selected_folder_display = tk.StringVar(value="No folder selected")

    analysis_data = {
        "avg_by_chip": {},
        "focused_raw": {},
        "focused_filt": {},
        "results": {},
        "_cache": {},
        "current_plot": [1],
    }

    tab_analyze.grid_rowconfigure(0, weight=1)
    tab_analyze.grid_columnconfigure(0, weight=0, minsize=250)
    tab_analyze.grid_columnconfigure(1, weight=1)

    left_frame_analyze = tk.Frame(tab_analyze, bg="lightgrey")
    left_frame_analyze.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
    left_frame_analyze.pack_propagate(False)

    notebook_analyze = ttk.Notebook(left_frame_analyze)
    notebook_analyze.pack(fill="both", expand=True)

    create_data_setup_frame(notebook_analyze, folder_path, selected_folder_display)
    output_text = create_console_log_frame(notebook_analyze)

    plot_frame_analyze = tk.Frame(tab_analyze)
    plot_frame_analyze.grid(row=0, column=1, sticky="nswe")

    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame_analyze)
    canvas_widget = canvas.get_tk_widget()
    toolbar = NavigationToolbar2Tk(canvas, plot_frame_analyze)
    toolbar.update()

    toolbar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    canvas.draw()

    create_controls_frame(
        notebook_analyze, folder_path, output_text, ax, canvas, fig, analysis_data
    )

    button_frame = tk.Frame(plot_frame_analyze)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False, pady=5)

    prev_button = tk.Button(
        button_frame,
        text="◀",
        command=lambda: switch_plot(
            "previous", analysis_data, ax, canvas, fig, output_text
        ),
    )
    next_button = tk.Button(
        button_frame,
        text="▶",
        command=lambda: switch_plot(
            "next", analysis_data, ax, canvas, fig, output_text
        ),
    )
    prev_button.pack(side=tk.LEFT, padx=5)
    next_button.pack(side=tk.RIGHT, padx=5)


def create_data_setup_frame(parent, folder_path_var, selected_folder_display_var):
    frame_data_setup = tk.LabelFrame(
        parent, text="Data Setup", relief=tk.SUNKEN, borderwidth=2
    )
    frame_data_setup.pack(fill="x", padx=10, pady=10)

    def select_folder():
        selected_folder = filedialog.askdirectory(
            title="Select a Folder", initialdir="/home/pi/Desktop/Biosensor V2/data"
        )
        if selected_folder:
            folder_path_var.set(selected_folder)
            # Display only the base name of the folder, but use the full path for processing
            selected_folder_display_var.set(os.path.basename(selected_folder))
            output_text_analyze.insert(tk.END, f"Selected folder: {selected_folder}\n")
            output_text_analyze.see(tk.END)

    tk.Label(frame_data_setup, text="Select Folder:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    select_folder_button = tk.Button(
        frame_data_setup, text="Browse", width=8, height=1, command=select_folder
    )
    select_folder_button.grid(row=0, column=1, padx=5, pady=5)

    # Label to display the selected folder path
    folder_display_label = tk.Label(
        frame_data_setup,
        textvariable=selected_folder_display_var,  # Use the StringVar
        wraplength=200,
        anchor="w",
        justify="left",
        bg="lightgrey",
    )
    folder_display_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)


# Global variable for analyze tab's output text for logging
output_text_analyze = None


def create_console_log_frame(parent):
    global output_text_analyze  # Use the global variable for analyze tab

    frame_output = tk.LabelFrame(
        parent, text="Console Log", relief=tk.SUNKEN, borderwidth=2
    )
    frame_output.pack(fill="both", padx=10, pady=5, expand=True)

    output_text_analyze = tk.Text(
        frame_output, height=10, width=40, wrap="none", bg="white"
    )
    scrollbar = tk.Scrollbar(
        frame_output, orient=tk.VERTICAL, command=output_text_analyze.yview, width=20
    )
    output_text_analyze.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text_analyze.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    return output_text_analyze


def create_controls_frame(
    parent, folder_path, log_widget, ax, canvas, fig, analysis_data
):
    frame_controls = tk.LabelFrame(
        parent, text="Controls", relief=tk.SUNKEN, borderwidth=2
    )
    frame_controls.pack(fill="x", padx=10, pady=5)

    run_button = tk.Button(
        frame_controls,
        text="Run Analysis",
        width=15,
        height=2,
        command=lambda: run_analysis(
            folder_path.get(), log_widget, ax, canvas, fig, analysis_data
        ),
    )
    run_button.pack(padx=5, pady=10)


def run_analysis(folder, log_widget, ax, canvas, fig, analysis_data):
    """Run comprehensive analysis on selected folder."""
    if not folder:
        log_widget.insert(tk.END, "Please select a folder first!\n")
        log_widget.see(tk.END)
        return

    log_widget.insert(tk.END, "Starting analysis...\n")
    log_widget.see(tk.END)

    # Build average per chip
    avg_by_chip = {}
    for chip, files in CHIP_FILES.items():
        vd, vgs, avg_isd = average_isd_over_files(chip, files, folder)
        if vgs is not None and avg_isd is not None:
            avg_by_chip[chip] = (vd, vgs, avg_isd)
            log_widget.insert(tk.END, f"Processed {chip} with {len(files)} files.\n")
        else:
            log_widget.insert(tk.END, f"Error processing {chip}.\n")
    log_widget.see(tk.END)

    if not avg_by_chip:
        log_widget.insert(tk.END, "No data found. Check folder structure.\n")
        log_widget.see(tk.END)
        return

    # Focus traces at target VSG and filter
    focused_raw = build_traces_at_vsg(avg_by_chip, TARGET_VSG, interpret_as_vsg=True)
    focused_filt = apply_filter(
        focused_raw,
        window=FILTER_WINDOW,
        passes=FILTER_PASSES,
        pad_mode=PAD_MODE,
        zero_phase=ZERO_PHASE,
    )

    # Color palette for chips
    _palette = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    chip_colors = {
        chip: _palette[i % len(_palette)]
        for i, chip in enumerate(sorted(focused_filt.keys()))
    }

    # Analysis per chip
    results = {}
    _cache = {}

    for chip, (Vsd_arr, Isd_f) in focused_filt.items():
        color = chip_colors[chip]
        est_rms = None
        if BASELINE_RMS is None:
            k = max(5, int(0.15 * len(Isd_f)))
            local = Isd_f[:k] - np.median(Isd_f[:k])
            est_rms = float(np.std(local))

        Ron, m_lin, b_lin, lin_mask, r2_lin = robust_small_v_fit(
            Vsd_arr, Isd_f, v_cap=OHMIC_VCAP
        )

        out = output_params(
            Vsd_arr,
            Isd_f,
            vth=None,
            gate_voltage=0.0,
            frac_start=SAT_FRAC_START,
            vds_ref=None,
            edge_pad=EDGE_PAD_FOR_FITS,
            chip=chip,
            two_slope_windows=TWO_SLOPE_WINDOWS,
        )
        xs_sat = Vsd_arr[out["sat_mask"]]
        ys_sat = Isd_f[out["sat_mask"]]

        if chip in TWO_SLOPE_WINDOWS:
            w = TWO_SLOPE_WINDOWS[chip]
            vx, iy, (m1, b1, m2, b2) = two_slope_intersection(
                Vsd_arr, Isd_f, w["steeper"], w["flatter"]
            )
        else:
            vx = iy = m1 = b1 = m2 = b2 = np.nan

        r2_steep = np.nan
        r2_flat = np.nan
        if chip in TWO_SLOPE_WINDOWS and np.isfinite(m1) and np.isfinite(m2):
            w = TWO_SLOPE_WINDOWS[chip]
            m1mask = (Vsd_arr >= w["steeper"][0]) & (Vsd_arr <= w["steeper"][1])
            m2mask = (Vsd_arr >= w["flatter"][0]) & (Vsd_arr <= w["flatter"][1])

            if m1mask.sum() >= 2:
                yhat1 = m1 * Vsd_arr[m1mask] + b1
                r2_steep = r_squared(Isd_f[m1mask], yhat1)
            if m2mask.sum() >= 2:
                yhat2 = m2 * Vsd_arr[m2mask] + b2
                r2_flat = r_squared(Isd_f[m2mask], yhat2)

        SNR = compute_snr(
            Isd_f,
            baseline_trace_A=baseline_Id_detrended,
            baseline_rms_A=(BASELINE_RMS or est_rms),
        )

        results[chip] = {
            "Ron_ohm": Ron,
            "R2_lin": r2_lin,
            "gsd_S": out["gsd"],
            "ro_ohm": out["ro"],
            "VA_V": out["VA"],
            "Id_sat_ref_A": out["Id_sat_ref"],
            "Vds_ref_V": out["vds_ref"],
            "Vx_two_slope_V": vx,
            "Isd_sat_two_slope_A": iy,
            "R2_steep": r2_steep,
            "R2_flat": r2_flat,
            "noise_rms_A": SNR["noise_rms_A"],
            "I_det_A": SNR["I_det_A"],
            "SNR_dB": SNR["snr_db"],
            "DynRange_dB": SNR["dynamic_range_db"],
        }
        _cache[chip] = {
            "color": color,
            "lin_mask": lin_mask,
            "m_lin": m_lin,
            "b_lin": b_lin,
            "xs_sat": xs_sat,
            "ys_sat": ys_sat,
            "a_sat": out["a"],
            "b_sat": out["b"],
            "two": {"vx": vx, "iy": iy, "m1": m1, "b1": b1, "m2": m2, "b2": b2},
            "raw": focused_raw.get(chip, (Vsd_arr, Isd_f)),
        }

    # Compute gm at TARGET_VSG
    for chip in sorted(avg_by_chip.keys()):
        gm_S, gm_R2 = _compute_gm_at_target_vgs(
            chip, TARGET_VSG, avg_by_chip, TWO_SLOPE_WINDOWS
        )
        if chip in results:
            results[chip]["gm_S"] = gm_S
            results[chip]["gm_R2"] = gm_R2

    # Store in analysis_data
    analysis_data["avg_by_chip"] = avg_by_chip
    analysis_data["focused_raw"] = focused_raw
    analysis_data["focused_filt"] = focused_filt
    analysis_data["results"] = results
    analysis_data["_cache"] = _cache
    analysis_data["current_plot"] = [1]

    log_widget.insert(
        tk.END, "Analysis complete! Use navigation buttons to view plots.\n"
    )
    log_widget.see(tk.END)

    # Display first plot
    switch_plot("current", analysis_data, ax, canvas, fig, log_widget)


def switch_plot(direction, analysis_data, ax, canvas, fig, log_widget):
    """Switch between plots."""
    if direction == "previous":
        analysis_data["current_plot"][0] = max(1, analysis_data["current_plot"][0] - 1)
    elif direction == "next":
        analysis_data["current_plot"][0] = min(4, analysis_data["current_plot"][0] + 1)

    plot_num = analysis_data["current_plot"][0]

    if plot_num == 1:
        plot_output_characteristics(analysis_data, ax, canvas, fig, log_widget)
    elif plot_num == 2:
        plot_raw_vs_filtered(analysis_data, ax, canvas, fig, log_widget)
    elif plot_num == 3:
        plot_concentration_vs_id_sat(analysis_data, ax, canvas, fig, log_widget)
    elif plot_num == 4:
        plot_summary_table(analysis_data, ax, canvas, fig, log_widget)


def plot_output_characteristics(analysis_data, ax, canvas, fig, log_widget):
    """Plot 1: Output characteristics (filtered; faint raw overlay)."""
    focused_filt = analysis_data.get("focused_filt", {})
    _cache = analysis_data.get("_cache", {})

    if not focused_filt:
        ax.clear()
        ax.set_title("No Data for Output Characteristics Plot")
        canvas.draw_idle()
        return

    ax.clear()
    for chip, (Vsd_arr, Isd_f) in focused_filt.items():
        c = _cache[chip]["color"]
        Vsd_raw, Isd_raw = _cache[chip]["raw"]
        ax.plot(Vsd_raw, Isd_raw, "-", color=c, alpha=0.25)
        ax.plot(Vsd_arr, Isd_f, "o-", color=c, label=chip)

    ax.set_xlim(
        0, max(np.max(v[0]) for v in focused_filt.values()) if focused_filt else 3.5
    )
    ax.set_xlabel("VSD (V)", fontsize=11)
    ax.set_ylabel("ISD (A)", fontsize=11)
    VSG_LABEL = f"{abs(float(TARGET_VSG)):.2f}"
    ax.set_title(f"ISD–VSD (filtered) at VSG = {VSG_LABEL} V", fontsize=12)
    ax.grid(True, ls=":")
    ax.legend()
    fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
    canvas.draw_idle()
    log_widget.insert(tk.END, "Displayed: Output Characteristics\n")
    log_widget.see(tk.END)


def plot_raw_vs_filtered(analysis_data, ax, canvas, fig, log_widget):
    """Plot 2: Raw vs Filtered overlay with two-slope lines."""
    focused_filt = analysis_data.get("focused_filt", {})
    _cache = analysis_data.get("_cache", {})
    results = analysis_data.get("results", {})

    if not focused_filt:
        ax.clear()
        ax.set_title("No Data for Raw vs Filtered Plot")
        canvas.draw_idle()
        return

    ax.clear()
    xmax = max(np.max(v[0]) for v in focused_filt.values())

    VSG_LABEL = f"{abs(float(TARGET_VSG)):.2f}"

    for chip, (Vsd_arr, Isd_f) in focused_filt.items():
        color = _cache[chip]["color"]
        Vsd_r, Isd_r = _cache[chip]["raw"]

        w = TWO_SLOPE_WINDOWS.get(chip)
        if w is not None:
            vx_r, iy_r, (m1r, b1r, m2r, b2r) = two_slope_intersection(
                Vsd_r, Isd_r, w["steeper"], w["flatter"]
            )
            vx_f, iy_f, (m1f, b1f, m2f, b2f) = two_slope_intersection(
                Vsd_arr, Isd_f, w["steeper"], w["flatter"]
            )
        else:
            vx_r = iy_r = m1r = b1r = m2r = b2r = np.nan
            vx_f = iy_f = m1f = b1f = m2f = b2f = np.nan

        gm_val = results[chip].get("gm_S", np.nan)
        lab_raw = f"{chip} — raw"
        if np.isfinite(iy_f) and np.isfinite(vx_f):
            if np.isfinite(gm_val):
                lab_filt = (
                    f"{chip} — filtered (ID sat={iy_f*1e6:.2f} µA @ {vx_f:.2f} V; "
                    f"gm={gm_val*1e6:.2f} µS)"
                )
            else:
                lab_filt = (
                    f"{chip} — filtered (ID sat={iy_f*1e6:.2f} µA @ {vx_f:.2f} V)"
                )
        else:
            lab_filt = f"{chip} — filtered"

        ax.plot(Vsd_r, Isd_r, "o-", alpha=0.25, color=color, label=lab_raw)
        ax.plot(Vsd_arr, Isd_f, "o-", alpha=0.95, color=color, label=lab_filt)

        pad = 0.15
        if np.isfinite(m1f) and np.isfinite(m2f):
            x1 = np.linspace(
                max(0.0, w["steeper"][0] - pad),
                min(xmax, (vx_f + pad) if np.isfinite(vx_f) else w["steeper"][1] + pad),
                200,
            )
            x2 = np.linspace(
                max(0.0, (vx_f - pad) if np.isfinite(vx_f) else w["flatter"][0] - pad),
                min(xmax, w["flatter"][1] + pad),
                200,
            )
            ax.plot(
                x1, m1f * x1 + b1f, "--", color=color, alpha=0.95, label="_nolegend_"
            )
            ax.plot(
                x2, m2f * x2 + b2f, "--", color=color, alpha=0.95, label="_nolegend_"
            )

        if np.isfinite(vx_f) and 0.0 <= vx_f <= xmax:
            ax.scatter([vx_f], [iy_f], marker="x", s=80, color=color)

    ax.set_xlim(0, xmax)
    ax.set_xlabel("VSD (V)", fontsize=11)
    ax.set_ylabel("ISD (A)", fontsize=11)
    ax.set_title(
        "Output Characteristics — Filtered vs Raw with Two-Slope ID sat", fontsize=12
    )
    ax.grid(True, ls=":")

    handles, labels = ax.get_legend_handles_labels()
    uniq_h, uniq_l, seen = [], [], set()
    for h, l in zip(handles, labels):
        if l == "_nolegend_":
            continue
        if l not in seen:
            uniq_h.append(h)
            uniq_l.append(l)
            seen.add(l)
    ax.legend(uniq_h, uniq_l, loc="best", frameon=True, fontsize=8)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
    canvas.draw_idle()
    log_widget.insert(tk.END, "Displayed: Raw vs Filtered with Two-Slope Lines\n")
    log_widget.see(tk.END)


def plot_concentration_vs_id_sat(analysis_data, ax, canvas, fig, log_widget):
    """Plot 3: Concentration (Dilution) vs Id_sat."""
    results = analysis_data.get("results", {})
    _cache = analysis_data.get("_cache", {})

    if not results:
        ax.clear()
        ax.set_title("No Data for Concentration Plot")
        canvas.draw_idle()
        return

    ax.clear()
    VSG_LABEL = f"{abs(float(TARGET_VSG)):.2f}"

    chip_order = ["5WT7", "5WT6", "5WT5", "5WT4", "5WT3", "5WT2", "5WT1"]

    dilution_values = []
    dilution_labels = []
    id_sats = []
    chip_names = []
    colors_plot = []

    for chip in chip_order:
        if chip in results and chip in DILUTION_MAP:
            dil_num, dil_label = DILUTION_MAP[chip]
            id_sat = results[chip]["Isd_sat_two_slope_A"]
            if np.isfinite(id_sat):
                dilution_values.append(dil_num)
                dilution_labels.append(dil_label)
                id_sats.append(id_sat * 1e6)
                chip_names.append(chip)
                colors_plot.append(_cache[chip]["color"])

    if dilution_values:
        ax.plot(
            dilution_values, id_sats, "o-", linewidth=2, markersize=8, color="#1f77b4"
        )

        for dil_val, idsat, chip, color in zip(
            dilution_values, id_sats, chip_names, colors_plot
        ):
            ax.scatter(
                [dil_val],
                [idsat],
                s=100,
                color=color,
                edgecolors="black",
                linewidths=1.5,
                zorder=5,
            )
            ax.annotate(
                chip,
                (dil_val, idsat),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                fontsize=9,
                color=color,
                weight="bold",
            )

        ax.set_xticks(dilution_values)
        ax.set_xticklabels(dilution_labels)

        ax.set_xlabel("[C]", fontsize=13, weight="bold")
        ax.set_ylabel("ID sat (µA)", fontsize=12)
        ax.set_title(
            f"Concentration vs Saturation Current @ VSG = {VSG_LABEL} V", fontsize=13
        )
        ax.grid(True, ls=":", alpha=0.6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.invert_xaxis()
    else:
        ax.set_title("No valid concentration data")

    fig.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)
    canvas.draw_idle()
    log_widget.insert(tk.END, "Displayed: Concentration vs ID_sat\n")
    log_widget.see(tk.END)


def plot_summary_table(analysis_data, ax, canvas, fig, log_widget):
    """Plot 4: Summary table."""
    results = analysis_data.get("results", {})
    focused_filt = analysis_data.get("focused_filt", {})
    _cache = analysis_data.get("_cache", {})

    if not results:
        ax.clear()
        ax.set_title("No Data for Summary Table")
        canvas.draw_idle()
        return

    VSG_LABEL = f"{abs(float(TARGET_VSG)):.2f}"

    headers = [
        "Chip",
        "Ron (Ω)",
        "R² (ohmic)",
        "gsd (µS)",
        "ro (kΩ)",
        "V_A (V)",
        "Id@Vref (µA)",
        "Vref (V)",
        "Vx knee (V)",
        "Id@knee (µA)",
        "gm (µS)",
        "gm R²",
        "slope_steep (µS)",
        "R²_steep",
        "slope_flat (µS)",
        "R²_flat",
        "noise_rms (pA)",
        "I_det=3σ (pA)",
        "signal_rms (µA)",
        "SNR (dB)",
        "DynRange (dB)",
    ]
    rows = []
    for chip in sorted(results.keys()):
        r = results[chip]
        vx = r["Vx_two_slope_V"]
        iy = r["Isd_sat_two_slope_A"]
        vx_s = f"{vx:.3f}" if np.isfinite(vx) else "—"
        iy_s = f"{iy*1e6:.2f}" if np.isfinite(iy) else "—"

        two = _cache[chip]["two"]
        m1_uS = two["m1"] * 1e6 if np.isfinite(two["m1"]) else np.nan
        m2_uS = two["m2"] * 1e6 if np.isfinite(two["m2"]) else np.nan
        m1_s = f"{m1_uS:.2f}" if np.isfinite(m1_uS) else "—"
        m2_s = f"{m2_uS:.2f}" if np.isfinite(m2_uS) else "—"

        r2s = f"{r['R2_steep']:.3f}" if np.isfinite(r.get("R2_steep", np.nan)) else "—"
        r2f = f"{r['R2_flat']:.3f}" if np.isfinite(r.get("R2_flat", np.nan)) else "—"

        sig_rms_uA = (
            float(np.sqrt(np.mean(focused_filt[chip][1] ** 2)) * 1e6)
            if chip in focused_filt
            else 0.0
        )

        gm_S = r.get("gm_S", np.nan)
        gm_R2 = r.get("gm_R2", np.nan)

        rows.append(
            [
                chip,
                f"{r['Ron_ohm']:.2f}",
                f"{r['R2_lin']:.3f}",
                f"{r['gsd_S']*1e6:.2f}",
                f"{r['ro_ohm']/1e3:.2f}",
                f"{r['VA_V']:.2f}",
                f"{r['Id_sat_ref_A']*1e6:.2f}",
                f"{r['Vds_ref_V']:.2f}",
                vx_s,
                iy_s,
                f"{gm_S*1e6:.2f}" if np.isfinite(gm_S) else "—",
                f"{gm_R2:.3f}" if np.isfinite(gm_R2) else "—",
                m1_s,
                r2s,
                m2_s,
                r2f,
                f"{r['noise_rms_A']*1e12:.2f}",
                f"{r['I_det_A']*1e12:.2f}",
                f"{sig_rms_uA:.2f}",
                f"{r['SNR_dB']:.1f}",
                f"{r['DynRange_dB']:.1f}",
            ]
        )

    ax.clear()
    ax.axis("off")

    ncols = len(headers)
    fig_w = max(24, 1.4 * ncols)
    fig_h = 0.62 * (len(rows) + 2)

    table = ax.table(cellText=rows, colLabels=headers, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(2.0, 1.25)

    for (rr, cc), cell in table.get_celld().items():
        if rr == 0:
            cell.set_text_props(weight="bold", color="black", fontsize=8)
            cell.set_height(cell.get_height() * 1.25)
        else:
            if rr % 2 == 0:
                cell.set_facecolor("#f6f7f9")

    title_suffix = (
        f"@ VSG = {VSG_LABEL} V — Id@Vref from sat-fit; Id@knee from two-slope"
    )
    fig.suptitle(f"Summary of Metrics {title_suffix}", fontsize=12, weight="bold")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.08)
    canvas.draw_idle()
    log_widget.insert(tk.END, "Displayed: Summary Table\n")
    log_widget.see(tk.END)
