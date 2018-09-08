#!/usr/bin/env python3.6

from test_modules import get_oracles_list
from test_modules import oracle_create
from test_modules import oracle_register
from test_modules import oracle_subscribe

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

# Choosing oracle to work with with

# Choose data to input (text)

# Converting data to HEX + add string length

# Put data to oracle line by line

# Parsing result to file

# Comparing results
