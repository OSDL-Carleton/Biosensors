import pandas as pd
import os

folder_path = '/home/pi/Desktop/Biosensor V1/Collect/Data/Set1'

chip_files = {
    'MWT1': ['T3_VSD_ISID_v1.csv', 'T5_VSD_ISID_v1.csv'],
    'MWT2': ['T4_VSD_ISID_v1.csv', 'T5_VSD_ISID_v1.csv'],
    'MWT3': ['T4_VSD_ISID_v1.csv', 'T5_VSD_ISID_v1.csv'],
    'MWT4': ['T4_VSD_ISID_v1.csv', 'T5_VSD_ISID_v1.csv'],
    'MWT5': ['T4_VSD_ISID_v1.csv', 'T5_VSD_ISID_v1.csv'],
}

def extract_values(file_path):
    try:
        df = pd.read_csv(file_path, header=None)
        vgs_values = df.iloc[4, 1:9].tolist()
        print(f'VGS values from {file_path} (row 5, columns B to I): {vgs_values}')
        df = pd.read_csv(file_path, skiprows=4)
        vd_values = df.iloc[:, 0].tolist()
        print(f'Vd values from {file_path}: {vd_values}')
        is_values = df.iloc[:, 1:9]
        id_values = df.iloc[:, 9:17]
        isd_values = id_values.subtract(is_values.values)
        for idx, vgs in enumerate(vgs_values):
            is_vals = is_values.iloc[:, idx].tolist()
            id_vals = id_values.iloc[:, idx].tolist()
            isd_vals = isd_values.iloc[:, idx].tolist()
            print(f'For Vgs = {vgs} from {file_path}:')
            print(f'  Is values: {is_vals}')
            print(f'  Id values: {id_vals}')
            print(f'  Isd values: {isd_vals}')
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

def run_part0():
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
            print(f'  Average Isd values for Vgs = {vgs}: {avg_isd_vals}')

    target_vgs = '-2.800000 (none)'
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

    average_isd_df = get_average_isd_df(average_isd_values)
    print(average_isd_df)

if __name__ == "__main__":
    run_part0()
