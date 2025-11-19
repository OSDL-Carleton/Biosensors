import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_path = '/home/pi/Desktop/Biosensor V1/Collect/Data/Set1/Test-Data-OEGFET.csv'

data = pd.read_csv(file_path, usecols=['X-Axis (V)', 'MWT1', 'MWT2', 'MWT3', 'MWT4', 'MWT5'])
data.set_index('X-Axis (V)', inplace=True)
transformed_data = data.applymap(lambda x: np.abs(np.sqrt(x)))

def find_flat_region(x, y, threshold_factor=0.1):
    dy = np.gradient(y, x)
    threshold = np.mean(np.abs(dy)) * threshold_factor
    flat_indices = np.where(np.abs(dy) < threshold)[0]
    if flat_indices.size > 0:
        return flat_indices[0], flat_indices[-1]
    return None, None

def find_sloped_region(x, y, flat_start, threshold_factor=0.5):
    if flat_start is None or flat_start == 0:
        return None
    dy = np.gradient(y[:flat_start], x[:flat_start])
    threshold = np.mean(np.abs(dy)) * threshold_factor
    sloped_indices = np.where(np.abs(dy) > threshold)[0]
    if sloped_indices.size > 0:
        return sloped_indices[0], sloped_indices[-1]
    return None, None

def plot_slope(x, y, x_full, color, label):
    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope * x_full + intercept
    plt.plot(x_full, y_fit, color + '--', label=label + f' slope: {slope:.2e}, R^2: {calc_r_squared(x, y, slope, intercept):.2f}')
    return slope, intercept

def calc_r_squared(x, y, slope, intercept):
    y_fit = slope * x + intercept
    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

def analyze_column(data, column_name, x_full):
    x = data.index.to_numpy()
    y = data[column_name].to_numpy()
    plt.plot(x, y, label=f'{column_name} Data', alpha=0.3)
    flat_start, flat_end = find_flat_region(x, y, threshold_factor=0.2)
    if flat_start is not None and flat_end is not None:
        slope_flat, intercept_flat = plot_slope(x[flat_start:flat_end+1], y[flat_start:flat_end+1], x_full, 'g', f'{column_name} Flat Region')
    else:
        slope_flat, intercept_flat = None, None

    if flat_start is None and flat_end is None:
        print(f"{column_name} does not have a flat region, identifying two sloped regions instead.")
        slope_start, slope_end = 0, len(y) - 1
        slope1, intercept1 = plot_slope(x[slope_start:(slope_end//2)+1], y[slope_start:(slope_end//2)+1], x_full, 'b', f'{column_name} Sloped Region 1')
        slope2, intercept2 = plot_slope(x[(slope_end//2)+1:slope_end+1], y[(slope_end//2)+1:slope_end+1], x_full, 'm', f'{column_name} Sloped Region 2')

        if np.isclose(slope1, slope2, atol=1e-2):
            print(f"Error: The slopes for {column_name} are too similar, indicating no distinct regions.")
        else:
            x_intersect = (intercept2 - intercept1) / (slope1 - slope2)
            y_intersect = slope1 * x_intersect + intercept1
            plt.plot(x_intersect, y_intersect, 'ko', markersize=10, label=f'Intersection {column_name} ({x_intersect:.2f}, {y_intersect:.2e})')
            print(f'Intersection for {column_name}: x = {x_intersect:.2f}, y = {y_intersect:.2e}')
    else:
        if flat_start is not None:
            slope_start, slope_end = find_sloped_region(x, y, flat_start, threshold_factor=1.0)
            if slope_start is not None and slope_end is not None:
                slope_increasing, intercept_increasing = plot_slope(x[slope_start:slope_end+1], y[slope_start:slope_end+1], x_full, 'r', f'{column_name} Sloped Region')

                if slope_flat != slope_increasing:
                    x_intersect = (intercept_increasing - intercept_flat) / (slope_flat - slope_increasing)
                    y_intersect = slope_increasing * x_intersect + intercept_increasing
                    plt.plot(x_intersect, y_intersect, 'ko', markersize=10, label=f'Intersection {column_name} ({x_intersect:.2f}, {y_intersect:.2e})')
                    print(f'Intersection for {column_name}: x = {x_intersect:.2f}, y = {y_intersect:.2e}')

def run_part1():
    plt.figure(figsize=(15, 10))
    x_full = np.linspace(transformed_data.index.min(), transformed_data.index.max(), 500)
    for column in transformed_data.columns:
        analyze_column(transformed_data, column, x_full)

    plt.title('Transformed Current vs Voltage Characteristics for MWT1, MWT2, MWT3, MWT4, and MWT5')
    plt.xlabel('Voltage (V)')
    plt.ylabel('Transformed Current (sqrt(A))')
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.5, fontsize='small')  # Adjusted the legend position with a margin
    plt.grid(True)
    plt.tight_layout()  # Automatically adjusts subplot params to give specified padding
    plt.show()

if __name__ == "__main__":
    run_part1()

