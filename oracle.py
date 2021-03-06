#!/usr/bin/env python3
import readline
from test_modules import get_oracles_list
from test_modules import oracle_create
from test_modules import oracle_register
from test_modules import oracle_subscribe
from test_modules import file_oraclize
from test_modules import oracle_read
from test_modules import int_to_hex
from test_modules import io_compare

# Choosing AC to work
ac_name = str(input("Input AC name with which you want to work (exmp: ORCL): "))
# Creating new oracle if needed (initial registration and subscribtion is included)
while True:
    oracle_create_choice = input("Do you want to create a new oracle? (y/n): ")
    if oracle_create_choice == 'y':
        name = input("Set your oracle name: ")
        description = input("Set your oracle description: ")
        type = input("Set your oracle type (e.g. d): ")
        datafee_reg = input("Set registration datafee >= txfee (in satoshis): ")
        datafee_sub = input("Set subscribtion datafee >= txfee (in satoshis): ")
        oracle_id = oracle_create(ac_name, name, description, type)
        publisher_id = oracle_register(ac_name, oracle_id, datafee_reg)
        oracle_subscribe(ac_name, oracle_id, publisher_id, datafee_sub)
        break
    elif oracle_create_choice == 'n':
        break
    else:
        print("Input y or n")

# Displaying oracles list
while True:
    oracles_show_choice = input("Do you want to display oracles "
                               "availiable on this AC? (y/n): ")
    if oracles_show_choice == 'y':
        oracles = get_oracles_list(ac_name)
        for oracle in oracles:
            print(oracle, oracles[oracle])
        break
    elif oracles_show_choice == 'n':
        break
    else:
        print("Input y or n")

while True:
    file_oraclize_choice = input("Do you want to transfer file to oracle? (y/n): ")
    if file_oraclize_choice == 'y':
        oracle_id = input("Input ID of Oracle to which you want to put the data: ")
        filename = input("Input the filename which you want to transfer: ")
        file_oraclize(ac_name, oracle_id, filename)
        break
    elif file_oraclize_choice == 'n':
        break
    else:
        print("Input y or n")

while True:
    oracle_read_choice = input("Do you want to read data from oracle? (y/n): ")
    if oracle_read_choice == 'y':
        oracle_id = input("Input ID of Oracle from which you want to read the data: ")
        filename = input("Input the filename to which you want to write the data: ")
        depth = input("Set amount of entries needed to get from oracle: ")
        oracle_read(ac_name, oracle_id, filename, depth)
        break
    elif oracle_read_choice == 'n':
        break
    else:
        print("Input y or n")

while True:
    converter_choice = input("Do you want to convert hex output file? (y/n): ")
    if converter_choice == 'y':
        filename = input("Input filename which you want to convert: ")
        int_to_hex(filename)
        break
    elif converter_choice == 'n':
        break
    else:
        print("Input y or n")

while True:
    comparison_choice = input("Do you want to compare input and outputs? (y/n): ")
    if comparison_choice == 'y':
        input_filename = input("Input original data filename: ")
        output_filename = input("Input blockchain data filename: ")
        comparison = io_compare(input_filename, output_filename)
        if comparison:
            print("Data match!")
        else:
            print("Data not match!!!")
        break
    elif comparison_choice == 'n':
        break
    else:
        print("Input y or n")
