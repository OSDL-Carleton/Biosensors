import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.interpolate import make_interp_spline

x_values = np.array([0, 0.35, 0.7, 1.05, 1.4, 1.75, 2.1, 2.45])
y_values = {
    0.0: [-0.006905754, -0.002003551, -0.000166431, -0.00032215, 0.000129555, -0.000229268, 0.001576656, 0.001356911],
    0.1: [-0.006305452, -0.001530227, 9.851e-05, 0.000742812, 0.00235071, 0.004476904, 0.00709309, 0.007658504],
    0.2: [-0.005732702, -0.000948747, 0.000636714, 0.001610762, 0.004399675, 0.00932644, 0.01352915, 0.015915393],
    0.3: [-0.00545782, -0.000370215, 0.000477217, 0.001964849, 0.006230394, 0.013757802, 0.019841455, 0.02628307],
    0.4: [-0.005261847, 1.4e-05, 0.00063198, 0.002098967, 0.00782745, 0.017532346, 0.02700744, 0.040083023],
    0.5: [-0.005668852, 0.000348737, 0.000306883, 0.00284624, 0.009147227, 0.021047187, 0.034273362, 0.055544064],
    0.6: [-0.005032556, 0.000617064, 0.000899632, 0.003024027, 0.01047497, 0.024651181, 0.04195199, 0.07219192],
    0.7: [-0.004835822, 0.00100834, 0.001141566, 0.003807245, 0.011744694, 0.027529346, 0.049857944, 0.08920753],
    0.8: [-0.003876331, 0.001330738, 0.00241475, 0.004459096, 0.013231857, 0.030551447, 0.057856401, 0.105775668],
    0.9: [-0.003513578, 0.001483482, 0.0033617, 0.005343514, 0.014788312, 0.033398451, 0.065595927, 0.121564277],
    1.0: [-0.00206237, 0.00171154, 0.00375511, 0.005881662, 0.016382992, 0.036751669, 0.072459003, 0.129845911]
}

def run_part2():
    threshold_vgs = 2.0

    plt.figure(figsize=(10, 6))
    gm_values = {}
    curve_labels = {}

    all_max_slopes = []
    for key, values in y_values.items():
        spline = make_interp_spline(x_values, values, k=3)
        x_smooth = np.linspace(x_values.min(), x_values.max(), 300)
        y_smooth = spline(x_smooth)

        slopes = np.diff(y_smooth) / np.diff(x_smooth)
        all_max_slopes.append(np.max(np.abs(slopes)))

    threshold_for_off = np.percentile(all_max_slopes, 50)

    for key, values in y_values.items():
        spline = make_interp_spline(x_values, values, k=3)
        x_smooth = np.linspace(x_values.min(), x_values.max(), 300)
        y_smooth = spline(x_smooth)

        slopes = np.diff(y_smooth) / np.diff(x_smooth)
        max_slope = np.max(np.abs(slopes))

        if max_slope < threshold_for_off:
            curve_labels[key] = "Off"
            plt.plot(x_smooth, y_smooth, label=f'{key} (Off)', linestyle='-.')
        else:
            curve_labels[key] = "On"
            slopes_right_to_left = np.diff(y_smooth[::-1]) / np.diff(x_smooth[::-1])
            on_region_start_index = len(slopes_right_to_left) - np.argmax(slopes_right_to_left > np.percentile(slopes_right_to_left, 75)) - 1

            if on_region_start_index < len(x_smooth):
                x_on_region = x_smooth[on_region_start_index:].reshape(-1, 1)
                y_on_region = y_smooth[on_region_start_index:].reshape(-1, 1)

                reg = LinearRegression().fit(x_on_region, y_on_region)
                gm = reg.coef_[0][0]
                gm_values[key] = gm

                plt.plot(x_smooth, y_smooth, label=f'{key} (On)')
                plt.plot(x_on_region, reg.predict(x_on_region), linestyle='--')

                extension_factor = 0.1
                extended_x = np.linspace(x_smooth[on_region_start_index] - extension_factor, x_smooth[-1] + extension_factor, 100).reshape(-1, 1)
                plt.plot(extended_x, reg.predict(extended_x), linestyle=':', linewidth=2, label=f'Slope {key} (gm={gm:.4f}, R^2={reg.score(x_on_region, y_on_region):.2f})')
            else:
                gm_values[key] = np.nan

    plt.xlabel('VGS (V)')
    plt.ylabel('Isd (A)')
    plt.legend(title='Vd values', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.3)
    plt.title('Isd vs VGS with gm slopes (On/Off Region)')
    plt.grid(True)
    plt.tight_layout() 
    plt.show()

    for key, gm in gm_values.items():
        label = curve_labels[key]
        if label == "On":
            print(f'gm for Vd = {key} (On): {gm:.4f}')
        else:
            print(f'Curve for Vd = {key} is Off, showing linear or inactive behavior.')

if __name__ == "__main__":
    run_part2()

