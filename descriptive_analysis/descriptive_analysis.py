#!/usr/bin/env python3

#AUTHOR: Joe Cloud
#PURPOSE: Perform simple descriptive analysis for Probability & Statistics for Engineers, project
#UTA FALL 2017


import numpy as np
import sys
import matplotlib.pyplot as plt


DATA_FILE = "../set_one/resistor_vals.csv"  # Set to default list

QUARTILES = [25, 50, 75]

if len(sys.argv) > 1:
    DATA_FILE = sys.argv[1]


def main():
    sample_vals = np.genfromtxt(DATA_FILE, delimiter=',')
    
    print(min(sample_vals))
    print(max(sample_vals))
    
    print(sample_vals)
    
    sample_mean = np.mean(sample_vals)
    
    print(sample_mean)

    sample_std = np.std(sample_vals)

    print(sample_std)
    
    # Calculate quartiles
    sample_quarts = []
    for quart in QUARTILES:
        sample_quarts.append(np.percentile(sample_vals, quart))

    
    print(sample_quarts)
    
    # Construct box-and-whisker plot, a.k.a. boxplot
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.boxplot(sample_vals, 0, 'kp', 0)
    fig.savefig('boxplot.png')
    fig.clf()
    

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.hist(sample_vals)
    fig.savefig('histogram.png')




if __name__ == "__main__":
    main()
