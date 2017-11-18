#!/usr/bin/env python3

# This performs necessary pre-processing for raw data from 'last' command

FILE_NAME = "stripped_batch_three.log"


def main():
    
    f = open(FILE_NAME, 'r')
    data = f.readlines()

    
    data_conved = convToSeconds(data)
    

    print(data_conved)

    data_interval = calcInterval(data_conved)

    print(data_interval)

    outfile = open("logininterval_vals.txt", 'w')

    
    for val in data_interval:
        outfile.write("%s\n" % val)


def convToSeconds(data):

    in_seconds = []

    for login in data:
        # Takes value in format HH:MM:SS and tokenizes, adds up each delimited element
        # w/ respective multiplier.
        temp_tok = login.split(':')

        in_seconds.append(int(temp_tok[2])+int(temp_tok[1])*60+int(temp_tok[0])*3600)

    return in_seconds



def calcInterval(data):
    in_intervals = []
    # Go through and get the difference between T1 and TO to determine login intervals
    # Must abs values bc for ex, TO may be 23:34:46 and T1 00:12:49 where the difference would be negative
    for i in range(0, len(data) - 1):
        in_intervals.append(abs(data[i] - data[i+1]))

    return in_intervals








if __name__ == "__main__":
    main()
