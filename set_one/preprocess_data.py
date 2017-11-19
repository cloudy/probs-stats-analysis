#!/usr/bin/env python3

# This simply offsets each value by 0.33

FILE_NAME="resistor_vals.csv"

def main():

    f = open(FILE_NAME, 'r')

    data = f.readlines()

    print(data)

    data_output = []
    for val in data:
        data_output.append(float(val) - 0.00033)

    outfile = open("resistor_vals_offset.csv", 'w')

    for val in data_output:
        outfile.write("%s\n" % val)




if __name__ == "__main__":
    main()
