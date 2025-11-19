import sys
print("Python executable being used:", sys.executable)
from sklearn.linear_model import LinearRegression


# Set the directory where your data files are located
data_directory = '/home/pi/Desktop/Biosensor V1/Data Collect/Data/Set1'

# List all CSV files in the directory
file_paths = [os.path.join(data_directory, f) for f in os.listdir(data_directory) if f.endswith('.csv')]

# Process each file
for file_path in file_paths:
    # Load the data, assuming the format is similar to the one you've used before
    df = pd.read_csv(file_path, skiprows=4)

    # Extract data
    Vsd = df['X-Axis (V) - Vd']
    fig, ax = plt.subplots(figsize=(12, 8))

    Isd_columns = df.columns[2:10]
    Id_columns = df.columns[11:19]

    # Plot data
    for col in Isd_columns:
        Vsg_label = col.split(' ')[0]
        ax.plot(Vsd, df[col], label=f'Is, Vsg = {Vsg_label}V', linestyle='-')

    for col in Id_columns:
        Vsg_label = col.split(' ')[0]
        ax.plot(Vsd, df[col], label=f'Id, Vsg = {Vsg_label}V', linestyle='--')

    ax.set_xlabel('Vsd (V)')
    ax.set_ylabel('Current (A)')
    ax.set_title('Is and Id vs Vsd for different Vsg values')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.show()
