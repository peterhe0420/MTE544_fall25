# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here

import matplotlib.pyplot as plt
from utilities import FileReader

def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file() 
   
    x_list = [float(row[0]) for row in values[1:]]  # skip header row if needed
    y_list = [float(row[1]) for row in values[1:]]

    plt.plot(x_list, y_list)
    
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")

    #plt.plot([lin[0] for lin in values], [lin[1] for lin in values])
    plt.legend()
    plt.grid()
    plt.show()
    
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)
