#!/usr/bin/env python3

import json
from subprocess import check_output
from test_modules import bcolors

depth = 0
file0 = open("data_sample", "r")

for line in file0:
    depth = depth + 1

ac_name = str(input("Input AC name with which you want to work (exmp: ORCL): "))

file2 = open("data_batonids", "r")
file3 = open("oracles_list", "r")

file2_list = file2.read().split("\n")
file3_list = file3.read().split("\n")

file2.close()
file3.close()

for line1, line2 in zip(file2_list,file3_list):
    file1 = open("data_"+line2, "a")
    oracles_jsondata = json.loads(check_output(["komodo-cli","-ac_name="+ac_name,"oraclessamples",str(line2.rstrip()),str(line1.rstrip()),str(depth)]))
    for sample in oracles_jsondata["samples"]:
        file1.write(str(sample[0]) + "\n")
    else:
        file1.close()
print(bcolors.OKGREEN + "Data succesfully grabbed from blockchain to data_blockchain file" + bcolors.ENDC)
