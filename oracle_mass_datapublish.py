#!/usr/bin/env python3
import time
import json
from subprocess import check_output

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ac_name = input("Input AC name with which you want to work (exmp: ORCL): ")
file1 = open("oracles_list", "r")
for line1 in file1:
    file2 = open("data_sample", "r")
    file3 = open("data_batonids", "a")
    for line2 in file2:
        new_oraclesdata = json.loads(check_output(["komodo-cli","-ac_name="+ac_name,"oraclesdata",line1.rstrip(),line2.rstrip()]))
        byte_oraclesdata_id = check_output(["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_oraclesdata["hex"]])
        batontx_id = byte_oraclesdata_id.decode().rstrip()
    else:
        file3.write(batontx_id + "\n")

print(bcolors.OKGREEN + "Data publishing transactions sent! Latest baton tx ids saved to data_batonids file." + bcolors.ENDC)
