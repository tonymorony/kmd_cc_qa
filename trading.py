#!/usr/bin/env python3.6
from test_modules import get_tokens_list
from test_modules import create_token

ac_name = str(input("Input AC name with which you want to work (exmp: BRK): "))

while True:
    token_add_choice = input("Do you want to create a new token? (y/n): ")
    if token_add_choice == 'y':
        name = input("Set your token name: ")
        supply = input("Set your token supply: ")
        description = input("Set your token description: ")
        create_token(ac_name, name, supply, description)
        break
    elif token_add_choice == 'n':
        break
    else:
        print("Input y or n")

while True:
    tokens_show_choice = input("Do you want to display tokens "
                               "availiable in this AC? (y/n): ")
    if tokens_show_choice == 'y':
        tokens = get_tokens_list(ac_name)
        for token in tokens:
            print(token, tokens[token])
        break
    elif tokens_show_choice == 'n':
        break
    else:
        print("Input y or n")
