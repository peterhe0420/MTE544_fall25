import matplotlib.pyplot as plt
from utilities import FileReader
import argparse

def plot_data(filename):
    headers, values = FileReader(filename).read_file()
    rows = values
    
    # Extract odometry data: odom_x, odom_y, odom_th (columns 0, 1, 2)
    odom_x = [float(row[0]) for row in rows]
    odom_y = [float(row[1]) for row in rows]
    odom_th = [float(row[2]) for row in rows]
    
    # Extract particle filter data: pf_x, pf_y, pf_th (columns 5, 6, 7)
    pf_x = [float(row[5]) for row in rows]
    pf_y = [float(row[6]) for row in rows]
    pf_th = [float(row[7]) for row in rows]
    
    # Extract timestamps (column 8)
    stamps = [float(row[8]) for row in rows]
    
    # Convert timestamps to seconds relative to first timestamp
    first_stamp = stamps[0]
    time_list = [(stamp - first_stamp) / 1e9 for stamp in stamps]  # Convert nanoseconds to seconds
    
    # --- ODOMETRY PLOTS ---
    # Figure 1: Odometry x-y trajectory
    plt.figure(figsize=(8, 6))
    plt.plot(odom_x, odom_y, 'b-', label='Odometry Trajectory', linewidth=2)
    plt.title('Odometry: x vs y')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    
    # Figure 2: Odometry x-t, y-t, θ-t
    fig_odom, axs_odom = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    axs_odom[0].plot(time_list, odom_x, color='b', label='odom_x(t)', linewidth=2)
    axs_odom[1].plot(time_list, odom_y, color='g', label='odom_y(t)', linewidth=2)
    axs_odom[2].plot(time_list, odom_th, color='r', label='odom_θ(t)', linewidth=2)
    
    axs_odom[0].set_ylabel('x [m]')
    axs_odom[1].set_ylabel('y [m]')
    axs_odom[2].set_ylabel('θ [rad]')
    axs_odom[2].set_xlabel('t [s]')
    
    for ax in axs_odom:
        ax.grid(True)
        ax.legend()
    
    fig_odom.suptitle('Odometry: Position and Orientation vs Time')
    plt.tight_layout()
    plt.show()
    
    # --- PARTICLE FILTER PLOTS ---
    # Figure 3: Particle Filter x-y trajectory
    plt.figure(figsize=(8, 6))
    plt.plot(pf_x, pf_y, 'r-', label='Particle Filter Trajectory', linewidth=2)
    plt.title('Particle Filter: x vs y')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    
    # Figure 4: Particle Filter x-t, y-t, θ-t
    fig_pf, axs_pf = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    axs_pf[0].plot(time_list, pf_x, color='b', label='pf_x(t)', linewidth=2)
    axs_pf[1].plot(time_list, pf_y, color='g', label='pf_y(t)', linewidth=2)
    axs_pf[2].plot(time_list, pf_th, color='r', label='pf_θ(t)', linewidth=2)
    
    axs_pf[0].set_ylabel('x [m]')
    axs_pf[1].set_ylabel('y [m]')
    axs_pf[2].set_ylabel('θ [rad]')
    axs_pf[2].set_xlabel('t [s]')
    
    for ax in axs_pf:
        ax.grid(True)
        ax.legend()
    
    fig_pf.suptitle('Particle Filter: Position and Orientation vs Time')
    plt.tight_layout()
    plt.show()
    
    # --- COMPARISON PLOTS ---
    # Comparison 1: x-y trajectories overlay
    plt.figure(figsize=(8, 8))
    plt.plot(odom_x, odom_y, 'b-', label='Odometry', linewidth=2, alpha=0.7)
    plt.plot(pf_x, pf_y, 'r-', label='Particle Filter', linewidth=2, alpha=0.7)
    plt.title('Comparison: Odometry vs Particle Filter Trajectories')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    
    # Comparison 2: theta vs time
    plt.figure(figsize=(10, 6))
    plt.plot(time_list, odom_th, 'b-', label='Odometry θ', linewidth=2, alpha=0.7)
    plt.plot(time_list, pf_th, 'r-', label='Particle Filter θ', linewidth=2, alpha=0.7)
    plt.title('Comparison: Orientation (θ) vs Time')
    plt.xlabel('t [s]')
    plt.ylabel('θ [rad]')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot odometry and particle filter data from robotPose.csv file.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to plot')
    args = parser.parse_args()
    
    for f in args.files:
        print(f"Plotting {f} ...")
        plot_data(f)
