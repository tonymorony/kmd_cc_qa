#!/usr/bin/env python3

import os
import readline
import subprocess
from test_modules import get_tokens_list, create_token, oracle_create,\
oracle_register, oracle_subscribe, get_oracles_list, oracle_utxogen,\
tokens_converter, tx_broadcaster, gateways_bind

header = "\
 _____       _                               _____  _____ \n\
|  __ \     | |                             /  __ \/  __ \\\n\
| |  \/ __ _| |_ _____      ____ _ _   _ ___| /  \/| /  \/\n\
| | __ / _` | __/ _ \ \ /\ / / _` | | | / __| |    | |    \n\
| |_\ \ (_| | ||  __/\ V  V / (_| | |_| \__ \ \__/\| \__/\\\n\
 \____/\__,_|\__\___| \_/\_/ \__,_|\__, |___/\____/ \____/\n\
                                    __/ |                 \n\
                                   |___/                  \n"


colors = {
        'blue': '\033[94m',
        'pink': '\033[95m',
        'green': '\033[92m',
        }

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'

# maybe have to output manual by some menu option
# ! have to save created tokens/oracles/gateways in separate files and show it to user on such data input
def token_create_gw():
    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    name = input("Set your token name: ")
    supply = input("Set your token supply: ")
    description = input("Set your token description: ")
    file = open("tokens_list", "a")

    token_txid = create_token(ac_name, name, supply, description)
    file.writelines(token_txid + "\n")
    file.close()
    print(colorize("Entry added to tokens_list file!\n", "green"))
    input("Press [Enter] to continue...")

def token_list_gw():
    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    tokens = get_tokens_list(ac_name)
    print("\n\t\t\tToken id" + "\t\t\t\t" + "| Token name")
    print("_________________________________________________________________________\n")

    for token in tokens:
        print(token, tokens[token])

    input("Press [Enter] to continue...")

def oracle_create_gw():
    print("Availiable data types:\n")
    datatypes = "Ihh -> height, blockhash, merkleroot\ns -> <256 char string\nS -> <65536 char string\nd -> <256 binary data\nD -> <65536 binary data\n\
c -> 1 byte signed little endian number, C unsigned\nt -> 2 byte signed little endian number, T unsigned\n\
i -> 4 byte signed little endian number, I unsigned\nl -> 8 byte signed little endian number, L unsigned\n\
h -> 32 byte hash\n"
    print(datatypes)
    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    name = input("Set your oracle name: ")
    description = input("Set your oracle description: ")
    type = input("Set your oracle type (e.g. Ihh): ")
    datafee_reg = input("Set registration datafee >= txfee (in satoshis): ")
    datafee_sub = input("Set subscribtion datafee >= txfee (in satoshis): ")
    file = open("oracles_list", "a")

    oracle_id = oracle_create(ac_name, name, description, type)
    publisher_id = oracle_register(ac_name, oracle_id, datafee_reg)
    oracle_subscribe(ac_name, oracle_id, publisher_id, datafee_sub)

    file.writelines(oracle_id + "\n")
    file.close()
    print(colorize("Entry added to oracles_list file!\n", "green"))
    input("Press [Enter] to continue...")
# have to add type!!!
def oracles_list_gw():
    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    oracles = get_oracles_list(ac_name)

    print("\n\t\tOracle id" + "\t\t\t\t" + "| Oracle name")
    print("_________________________________________________________________________\n")

    for oracle in oracles:
        print(oracle, oracles[oracle])

    input("Press [Enter] to continue...")

def oracles_utxogen_gw():
    # to give user helpful info
    file01 = open("oracles_list", "r")
    for line in file01:
        print(line)
    file01.close()

    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    oracle_id = input("Input txid of oracle: ")
    utxo_num = input("Input number of UTXOs you want to make: ")
    # have to get it automatically by oraclesinfo oracle_id !!!
    pubkey = input("Input your pubkey (aka publisher id): ")
    data_fee = input("Set subscribtion datafee >= txfee (in satoshis): ")

    oracle_utxogen(ac_name,oracle_id,utxo_num,pubkey,data_fee)

    print("\nUTXOs succesfully broadcasted")
    input("Press [Enter] to continue...")

def tokens_converter_gw():
    # to give user helpful info
    file00 = open("tokens_list", "r")
    for line in file00:
        print(line)
    file00.close()

    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    token_id = input("Input id of token which you want to convert: ")
    pubkey = input("Input pubkey to which you want to convert (for initial convertion use\
 03ea9c062b9652d8eff34879b504eda0717895d27597aaeb60347d65eed96ccb40): ")
    supply = input("Input supply which you want to convert (for initial convertion set all token supply): ")

    convertion_hex = tokens_converter(ac_name,"241",token_id,pubkey,supply)
    try:
        convertion_txid = tx_broadcaster(ac_name,convertion_hex["hex"])
    except KeyError:
        print("Hex error! Result of tokencovert call:")
        print(convertion_hex)
        input("Press [Enter] to continue...")
    else:
        print("Convertion transaction succesfully broadcasted: " + str(convertion_txid))
        input("Press [Enter] to continue...")

def gateway_bind_gw():
    # to give user helpful info
    file00 = open("tokens_list", "r")
    for line in file00:
        print(line)
    file00.close()
    print("\n")
    file01 = open("oracles_list", "r")
    for line in file01:
        print(line)
    file01.close()

    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    token_id = input("Input id of converted token which you want to bind: ")
    oracle_id = input("Input id of Ihh data type oracle which you want to bind: ")
    coinname = input("Input external coinname (should match with token and oracle names): ")
    # have to add automaticall tokensupply grab to not give user to mistake here
    tokensupply = input("Input supply of token which you want to bind: ")
    # have to add possiblity to choose option for auto-grab user pubkey
    pubkey = input("Input trusted pubkey for associating with gateway (e.g. yours): ")
    file = open("gateways_list", "a")

    bind_hex = gateways_bind(ac_name,token_id,oracle_id,coinname,tokensupply,pubkey)
    try:
        bind_txid = tx_broadcaster(ac_name,bind_hex["hex"])
    except KeyError:
        print("Hex error! Result of gatewaysbind call:")
        print(bind_hex)
        input("Press [Enter] to continue...")
    else:
        print(colorize("Bind transaction succesfully broadcasted: " + bind_txid.decode().rstrip(), "green"))
        file.writelines(bind_txid + "\n")
        file.close()
        print(colorize("Entry added to gateways_list file!\n", "green"))
        input("Press [Enter] to continue...")

def oraclefeed_compile_gw():
    path_to_komodo = input("Provide me path to your komodo directory. E.g. /home/komodo/ : ")
    # have to add / if last not /
    subprocess.call(["gcc",path_to_komodo+"src/cc/dapps/oraclefeed.c","-lm","-o",path_to_komodo+"/src/oraclefeed"])
    subprocess.call(["sudo","ln","-sf",path_to_komodo+"/src/oraclefeed","/usr/local/bin/oraclefeed"])
    print("oraclefeed is compiled and ready to call as oraclefeed")
    input("Press [Enter] to continue...")

def oraclefeed_run_gw():
    print("You called bar()")
    input("Press [Enter] to continue...")

#def oraclefeed_status_monitor(): would be great for future create simple node monitoring tool/method
# working with multi-instances of oraclefeed
# checking consisntancy of Ihh oracles height data

def send_kmd_gw():
    print("You called bar()")
    input("Press [Enter] to continue...")
# Send z_sendmany transaction - ask wallets and amounts, get txid, wait for confirmation
# Automatically execute gatewaysdeposit?

def tokens_witdrawal_gw():
    print("You called bar()")
    input("Press [Enter] to continue...")

menuItems = [
    { "Create token": token_create_gw },
    { "Get list of availiable tokens": token_list_gw },
    { "Create oracle": oracle_create_gw },
    { "Oracle subscription UTXOs generator" : oracles_utxogen_gw },
    { "Get list of availiable oracles": oracles_list_gw },
    #maybe have just write method and call it with option on deposit/withdrawal execution
    { "Tokens converter": tokens_converter_gw },
    { "Bind gateway": gateway_bind_gw },
    { "Compile oraclefeed dAPP": oraclefeed_compile_gw },
    { "Run oraclefeed dAPP": oraclefeed_run_gw },
    { "Send KMD gateway deposit transaction": send_kmd_gw },
    { "Withdraw tokens": tokens_witdrawal_gw },
    { "Exit": exit },
]

def main():
    while True:
        os.system('clear')
        print(colorize(header, 'pink'))
        print(colorize('CLI version 0.1 by Anton Lysakov\n', 'green'))
        for item in menuItems:
            print(colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + list(item.keys())[0])
        choice = input(">> ")
        # Have to handle CTRL + C (back to main menu on it if user changed his mind inside of some menuitem)
        try:
            if int(choice) < 0 : raise ValueError
            # Call the matching function
            list(menuItems[int(choice)].values())[0]()
        except (ValueError, IndexError):
            pass

if __name__ == "__main__":
    main()
