import matplotlib.pyplot as plt
from utilities import FileReader
import argparse

def plot_data(filename):
    headers, values = FileReader(filename).read_file()
    rows = values[1:]  # skip header if present

    # Fixed column order: x, y, theta, time (timestamps)
    x = [float(row[0]) for row in rows]
    y = [float(row[1]) for row in rows]
    th = [float(row[2]) for row in rows]
    t_raw = [float(row[3]) for row in rows]

    # Convert timestamps to seconds (assuming nanoseconds)
    # t = [(val - t_raw[0]) / 1e9 for val in t_raw]
    time_list=[]
    
    first_stamp=rows[0][-1]
    
    for val in rows:
        time_list.append(val[-1] - first_stamp)
    # --- Figure 1: x–y trajectory ---
    plt.figure(figsize=(6, 5))
    plt.plot(x, y, label='Trajectory')
    plt.title('x vs y')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.legend()
    plt.grid(True)

    # --- Figure 2: x–t, y–t, θ–t ---
    fig, axs = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    axs[0].plot(time_list, x, color='b', label='x(t)')
    axs[1].plot(time_list, y, color='g', label='y(t)')
    axs[2].plot(time_list, th, color='r', label='θ(t)')

    axs[0].set_ylabel('x [m]')
    axs[1].set_ylabel('y [m]')
    axs[2].set_ylabel('θ [rad]')
    axs[2].set_xlabel('t [ns]')

    for ax in axs:
        ax.grid(True)
        ax.legend()

    fig.suptitle(f'Position and Orientation vs Time')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot x–y and time-based states from log file.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to plot')
    args = parser.parse_args()

    for f in args.files:
        print(f"Plotting {f} ...")
        plot_data(f)
