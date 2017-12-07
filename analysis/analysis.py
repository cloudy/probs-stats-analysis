#!/usr/bin/env python3

#AUTHOR: Joe Cloud
#PURPOSE: Perform  analysis for Probability for Engineers, project
#UTA FALL 2017


import numpy as np
from scipy.stats import norm, expon, chisquare
import sys
import matplotlib.pyplot as plt
import tabulate

DATA_FILE = "../set_one/resistor_vals_offset.csv"  # Set to default list
QUARTILES = [25, 50, 75]
EXPECT_NORMAL = True

if len(sys.argv) > 1:
    DATA_FILE = sys.argv[1]
    #EXPECT_NORMAL = False

OUTPUT_FILE = "results/" + DATA_FILE.split('/')[-1].split('vals')[0]

def main():


    sample_vals = np.genfromtxt(DATA_FILE, delimiter=',')
    print(sample_vals)

    n = len(sample_vals)
    print("There are %d samples" % n)

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

    #generateTable(sample_vals)
    plt.style.use('ggplot')
    plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
    #Options
    params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
          }
    plt.rcParams.update(params)  
    # Construct box-and-whisker plot, a.k.a. boxplot
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.boxplot(sample_vals, 0, 'kp', 0)
    fig.savefig(OUTPUT_FILE + 'boxplot.png', bbox_inches='tight')
    fig.clf()

    num_bins = 10

    # Frequency table
    counts, ranges = np.histogram(sample_vals, bins=num_bins)
    print("histogram:", counts, ranges)

    # Histogram data
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.hist(sample_vals, bins=num_bins)
    fig.savefig(OUTPUT_FILE + 'histogram.png', bbox_inches='tight')
    fig.clf()

    # Part 2

    new_counts, new_ranges, new_expp = expected_frequencies(counts, ranges, sample_mean, sample_std, n)

    print(counts, new_counts)
    print(new_expp)

    print(sum(new_expp))
    print(counts)

    print(ranges, new_ranges)

    print(counts, new_counts)
    cS = chisquare(new_counts, new_expp) 
    print(cS)

    print("\n\n\n\n")

    print(new_counts)
    print(new_counts.T)

    # class , observed freq, class prob, expected freq, chi sq
    chi_vals = []
    for i in range(len(new_counts)):
        chi_vals.append(chi_sqr(new_counts[i],new_expp[i]))

    print(chi_vals)
    
    chi_vals = np.array(chi_vals)
    classp = new_expp/n

    print(len(new_ranges))
    print(len(new_counts))
    
    # Stack vectors together by column, so must take transpose
    pt2table = np.stack((np.insert(new_ranges[1:], 0, 0.0)[:-1], 
        new_ranges[1:].T,new_counts.T, classp.T, new_expp.T, chi_vals.T), axis=1)
    print(pt2table)

    generateTable(pt2table)
    

    print(1 - expon.cdf(33500.2, sample_mean, sample_std))

def chi_sqr(o, e):
    return ((o - e)**2)/e


def expected_frequencies(counts, ranges, sample_mean, sample_std, n):
    
    counts = np.copy(counts)
    ranges = np.copy(ranges)

    STATFUNC = norm.cdf 
    if EXPECT_NORMAL == False:
        STATFUNC = expon.cdf

    expp = []
    expp_sum = 0



    for i in range(0, len(ranges)):

        upper = 1 
        if i < len(ranges) - 1:
            upper = STATFUNC(ranges[i+1], sample_mean, sample_std)

        lower = STATFUNC(ranges[i], sample_mean, sample_std)
        if i == 0:
            lower = 0

        expp.append(upper - lower)

        expp_sum += expp[i]
        #print(i, expp_sum, upper, lower)

    #print(expp)
    
    if EXPECT_NORMAL == True:
        expp[-2] += expp[-1]
        expp = expp[:-1]
    else:
        expp[1] += expp[0]
        expp = expp[1:]
    #print("Sum should equal 1, is %f" % sum(expp)) # CHECK
    i = 0
    clean_pass = False
    found_dirt = False
    while(not clean_pass):
        
        found_dirt = False

        if expp[i]*n < 5.0: # Generally we don't want valus to be below 5%
            #print("Found dirt")
            found_dirt = True
            #print(expp[i]) 

            if i <= len(expp)/2:

                if i == 0:
                    expp[1] += expp[0]
                    counts[1] += counts[0]
                    expp = expp[1:]
                    counts = counts[1:]
                    ranges = ranges[1:]
                else:
                    if expp[i - 1] < expp[i + 1]:
                        expp[i] += expp[i - 1]
                        counts[i] += counts[i - 1]
                        expp = np.delete(expp, i - 1)
                        counts = np.delete(counts, i - 1)
                        ranges = np.delete(ranges, i - 1)
                    else:
                        expp[i] += expp[i + 1]
                        counts[i] += counts[i + 1]
                        expp = np.delete(expp, i + 1)
                        counts = np.delete(counts, i + 1)
                        ranges = np.delete(ranges, i + 1)
            else:         
                maxv = len(expp) - 1
                maxc = len(counts) -1
                cdelta =0 # maxv - maxc

                #print("MAX", maxv, maxc)
                if i == maxv:
                    expp[maxv - 1] += expp[maxv]
                    counts[maxc - 1] += counts[maxc]
                    expp = expp[:-1]
                    counts = counts[:-1]
                    ranges = ranges[:-1]
                else:
                    if expp[i - 1] < expp[i + 1]:
                        expp[i] += expp[i - 1]
                        counts[i - cdelta] += counts[i - 1 - cdelta]
                        expp = np.delete(expp, i - 1)
                        counts = np.delete(counts, i - 1 - cdelta)
                        ranges = np.delete(ranges, i - 1)
                    else:
                        expp[i] += expp[i + 1]
                        counts[i - cdelta] += counts[i + 1 - cdelta]
                        expp = np.delete(expp, i + 1)
                        counts = np.delete(counts, i + 1 - cdelta)
                        ranges = np.delete(ranges, i + 1)

        if (i == len(expp) - 1) and found_dirt == False:
            clean_pass = True

        i = (i + 1) % (len(expp))

        #print("EXPP:", expp,"\nCOUNTS: ", counts,"\nRANGES:", ranges)

    return counts, ranges, expp*n



def generateTable(data, reshape = False):

    data_c = data
    if reshape == True:
        data_c = data.reshape(10, int(len(data)/10))
        print(data_c.shape)

    gen_table = tabulate.tabulate(data_c, tablefmt="latex")
    print(gen_table)

    outfile = open(OUTPUT_FILE + 'latex_gen.txt', 'w')
    outfile.write("\n\n\n")
    outfile.write("%s\n" % gen_table)   


if __name__ == "__main__":
    main()
