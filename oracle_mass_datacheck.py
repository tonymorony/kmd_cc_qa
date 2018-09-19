#!/usr/bin/env python3

import filecmp
from test_modules import bcolors

def int_to_hex(input_filename):
    with open(input_filename, 'r') as file:
        data = file.readlines()
    with open(input_filename, 'w') as file:
        for entry in data:
            file.writelines(hex(int(entry))[2:] + "\n")

def io_compare(input_filename, output_filename):
    compare = filecmp.cmp(input_filename, output_filename, shallow=True)
    return compare

#Have to convert int back to hex first
file1 = open("oracles_list", "r")
for line in file1:
    int_to_hex("data_"+line.rstrip())
file1.close()

#Then compare with input data
file2 = open("oracles_list", "r")
for line in file2:
    compare = io_compare("data_sample", "data_"+line.rstrip())
    if compare:
        print(bcolors.OKGREEN + line.rstrip() + " data match!" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + line.rstrip() + " data not match!!!" + bcolors.ENDC)
