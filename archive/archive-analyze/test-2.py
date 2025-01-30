import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

folder_path = "/content/drive/My Drive/Masters/5MWT-Oligio"


chip_files = {
    "5WT1": [
        "T3_VSD_ISID_v1.csv",
        # 'T3_VSD_ISIG_v1.csv',
        "T4_VSD_ISID_v1.csv",
        # 'T4_VSD_ISIG_v1.csv',
        "T5_VSD_ISID_v1.csv",
        # 'T5_VSD_ISIG_v1.csv'
    ],
    "5WT2": [
        "T3_VSD_ISID_v1.csv",
        # 'T3_VSD_ISIG_v1.csv',
        "T4_VSD_ISID_v1.csv",
        # 'T4_VSD_ISIG_v1.csv',
        "T5_VSD_ISID_v1.csv",
        # 'T5_VSD_ISIG_v1.csv'
    ],
    "5WT3": [
        "T3_VSD_ISID_v1.csv",
        # 'T3_VSD_ISIG_v1.csv',
        "T4_VSD_ISID_v1.csv",
        # 'T4_VSD_ISIG_v1.csv',
        "T5_VSD_ISID_v1.csv",
        # 'T5_VSD_ISIG_v1.csv'
    ],
    "5WT4": [
        "T3_VSD_ISID_v1.csv",
        # 'T3_VSD_ISIG_v1.csv',
        "T4_VSD_ISID_v1.csv",
        # 'T4_VSD_ISIG_v1.csv',
        "T5_VSD_ISID_v1.csv",
        # 'T5_VSD_ISIG_v1.csv'
    ],
    "5WT5": [
        "T3_VSD_ISID_v1.csv",
        # 'T3_VSD_ISIG_v1.csv',
        "T4_VSD_ISID_v1.csv",
        # 'T4_VSD_ISIG_v1.csv',
        "T5_VSD_ISID_v1.csv",
        # 'T5_VSD_ISIG_v1.csv'
    ],
    "5WT6": [
        "T3_VSD_ISID_v1.csv",
        # 'T3_VSD_ISIG_v1.csv',
        "T4_VSD_ISID_v1.csv",
        # 'T4_VSD_ISIG_v1.csv',
        "T5_VSD_ISID_v1.csv",
        # 'T5_VSD_ISIG_v1.csv'
    ],
    "5WT7": [
        "T3_VSD_ISID_v1.csv",
        # 'T3_VSD_ISIG_v1.csv',
        "T4_VSD_ISID_v1.csv",
        # 'T4_VSD_ISIG_v1.csv',
        "T5_VSD_ISID_v1.csv",
        # 'T5_VSD_ISIG_v1.csv'
    ],
}


def extract_values(file_path):
    try:

        df = pd.read_csv(file_path, header=None)

        vgs_values = df.iloc[4, 1:9].tolist()
        print(f"VGS values from {file_path} (row 5, columns B to I): {vgs_values}")

        df = pd.read_csv(file_path, skiprows=4)

        vd_values = df.iloc[:, 0].tolist()
        print(f"Vd values from {file_path}: {vd_values}")

        is_values = df.iloc[:, 1:9]
        id_values = df.iloc[:, 9:17]

        isd_values = id_values.subtract(is_values.values)

        for idx, vgs in enumerate(vgs_values):
            is_vals = is_values.iloc[:, idx].tolist()
            id_vals = id_values.iloc[:, idx].tolist()
            isd_vals = isd_values.iloc[:, idx].tolist()
            print(f"For Vgs = {vgs} from {file_path}:")
            print(f"  Is values: {is_vals}")
            print(f"  Id values: {id_vals}")
            print(f"  Isd values: {isd_vals}")

        return vd_values, vgs_values, is_values, id_values, isd_values
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None, None, None, None


def compute_average_isd(tool, files):
    combined_isd = None
    vgs_values = None
    vd_values = None

    for file_name in files:
        file_path = os.path.join(folder_path, tool, file_name)
        if os.path.exists(file_path):
            vd_vals, vgs_vals, _, _, isd_values = extract_values(file_path)
            if isd_values is not None:
                if combined_isd is None:
                    combined_isd = isd_values
                    vgs_values = vgs_vals
                    vd_values = vd_vals
                else:
                    combined_isd = combined_isd.add(isd_values, fill_value=0)
        else:
            print(f"File not found: {file_path}")

    if combined_isd is not None and len(files) > 0:

        average_isd = combined_isd / len(files)
        return vd_values, vgs_values, average_isd
    else:
        return None, None, None


average_isd_values = {}

for tool, files in chip_files.items():
    vd_values, vgs_values, average_isd = compute_average_isd(tool, files)
    if vgs_values is not None and average_isd is not None:
        average_isd_values[tool] = (vd_values, vgs_values, average_isd)


for tool, (vd_values, vgs_values, avg_isd) in average_isd_values.items():
    print(f"\nSummary for {tool}:")
    print(f"  Vd values: {vd_values}")
    print(f"  Vgs values: {vgs_values}")
    for idx, vgs in enumerate(vgs_values):
        avg_isd_vals = avg_isd.iloc[:, idx].tolist()
        print(f"  Average Isd values for Vgs = {vgs}: {avg_isd_vals}")


target_vgs = "-2.800000 (none)"
for tool, (vd_values, vgs_values, avg_isd) in average_isd_values.items():
    if target_vgs in vgs_values:
        idx = vgs_values.index(target_vgs)
        avg_isd_vals = avg_isd.iloc[:, idx].tolist()
        print(f"\nFocused Summary for {tool}:")
        print(f"  Vd values: {vd_values}")
        print(f"  Vgs values: {vgs_values}")
        print(f"  Average Isd values for Vgs = {target_vgs}: {avg_isd_vals}")


def get_average_isd_df(average_isd_values):
    avg_isd_df = pd.DataFrame()
    for tool, (vd_values, vgs_values, avg_isd) in average_isd_values.items():
        avg_isd_df[tool] = avg_isd.mean(axis=1)
    return avg_isd_df


# Define the Part 0 plot function
def plot_part_0(file_path):
    df = pd.read_csv(file_path, skiprows=4)
    Vsd = df["X-Axis (V) - Vd"]

    fig, ax0 = plt.subplots(figsize=(12, 8))

    Isd_columns = df.columns[2:10]
    Id_columns = df.columns[11:19]

    # Plot Is and Id vs Vsd for different Vsg values
    for col in Isd_columns:
        Vsg_label = col.split(" ")[0]
        ax0.plot(Vsd, df[col], label=f"Is, Vsg = {Vsg_label}V", linestyle="-")

    for col in Id_columns:
        Vsg_label = col.split(" ")[0]
        ax0.plot(Vsd, df[col], label=f"Id, Vsg = {Vsg_label}V", linestyle="--")

    ax0.set_xlabel("Vsd (V)")
    ax0.set_ylabel("Current (A)")
    ax0.set_title("Part 0: Is and Id vs Vsd for different Vsg values")
    ax0.legend(loc="upper left", bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.show()


part_0_file_path = "/content/drive/My Drive/T3_VSD_ISID_v3_v1.csv"
plot_part_0(part_0_file_path)  # First, plot Part 0


# Part 1 plot
# Define a function to plot the comparison of Isd values
def plot_comparison(vd_tool, y_tools, average_isd_values):
    # Debugging step to check available keys
    print(f"Available tools: {list(average_isd_values.keys())}")

    # Extract Vd values from the specified tool
    if vd_tool not in average_isd_values:
        raise KeyError(f"Tool {vd_tool} not found in average_isd_values!")

    vd_values = average_isd_values[vd_tool][0]  # Vd values from the vd_tool
    plt.figure(figsize=(10, 6))

    # Iterate through the selected y_tools and plot their corresponding Isd values
    for y_tool in y_tools:
        if y_tool not in average_isd_values:
            print(f"Warning: {y_tool} not found in average_isd_values! Skipping.")
            continue
        avg_isd = average_isd_values[y_tool][2]  # Get the Isd values for the y_tool
        mean_isd_vals = avg_isd.mean(
            axis=1
        ).tolist()  # Get the mean Isd values across Vgs
        plt.plot(vd_values, mean_isd_vals, label=f"Average Isd for {y_tool}")

    plt.title(f"Part 1: Isd vs Vd Comparison (X-axis: Vd from {vd_tool})")
    plt.xlabel("Vd (V)")
    plt.ylabel("Average Isd (A)")
    plt.legend()
    plt.grid(True)
    plt.show()


# Function to get a dataframe with average Isd values
def get_average_isd_df(average_isd_values):
    avg_isd_df = pd.DataFrame()
    for tool, (vd_values, vgs_values, avg_isd) in average_isd_values.items():
        avg_isd_df[tool] = avg_isd.mean(axis=1)
    return avg_isd_df


# Specify the tool to use for Vd values (X-axis)
vd_tool = "5WT1"

# Specify the tools you want to plot the Isd values for (Y-axis)
y_tools = ["5WT1", "5WT2", "5WT3", "5WT4", "5WT5", "5WT5", "5WT6", "5WT7"]

# Generate average Isd DataFrame from computed values
average_isd_df = get_average_isd_df(average_isd_values)

# Plot Part 1
plot_comparison(vd_tool, y_tools, average_isd_values)
