#!/usr/bin/env python3

#AUTHOR: Joe Cloud
#PURPOSE: Perform simple descriptive analysis for Probability & Statistics for Engineers, project
#UTA FALL 2017


import numpy as np
import sys
import matplotlib.pyplot as plt


DATA_FILE = "../set_one/resistor_vals_offset.csv"  # Set to default list
QUARTILES = [25, 50, 75]

if len(sys.argv) > 1:
    DATA_FILE = sys.argv[1]

OUTPUT_FILE = "results/" + DATA_FILE.split('/')[-1].split('vals')[0]


def main():
    
    sample_vals = np.genfromtxt(DATA_FILE, delimiter=',')
    print(sample_vals)
    
    print("Min value is: %f" % min(sample_vals))
    print("Max value is: %f" % max(sample_vals))
    
    sample_mean = np.mean(sample_vals)
    print("Mean value is: %f" % sample_mean)

    sample_std = np.std(sample_vals)
    print("STD value is: %f" % sample_std)
    
    # Calculate quartiles
    sample_quarts = []
    for quart in QUARTILES:
        sample_quarts.append(np.percentile(sample_vals, quart))

    print("Quartiles: ", *sample_quarts, sep=', ')
    
    # Construct box-and-whisker plot, a.k.a. boxplot
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.boxplot(sample_vals, 0, 'kp', 0)
    fig.savefig(OUTPUT_FILE + 'boxplot.png')
    fig.clf()
    
    num_bins = 10
    
    # Frequency table
    frequency_table = np.histogram(sample_vals, bins=num_bins)
    print(frequency_table)

    # Histogram data
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.hist(sample_vals, bins=num_bins)
    fig.savefig(OUTPUT_FILE + 'histogram.png')
    fig.clf()




if __name__ == "__main__":
    main()
