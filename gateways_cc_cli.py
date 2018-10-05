#!/usr/bin/env python3

import os
import readline
import subprocess
import signal
import sys
from subprocess import check_output
from test_modules import get_tokens_list, create_token, oracle_create,\
oracle_register, oracle_subscribe, get_oracles_list, oracle_utxogen,\
tokens_converter, tx_broadcaster, gateways_bind, z_sendmany_twoaddresses,\
list_address_groupings, operationstatus_to_txid, gateways_deposit, gateways_claim\

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
        print(colorize("Bind transaction succesfully broadcasted: " + bind_txid, "green"))
        file.writelines(bind_txid + "\n")
        file.close()
        print(colorize("Entry added to gateways_list file!\n", "green"))
        input("Press [Enter] to continue...")

def oraclefeed_compile_gw():
    while True:
        path_to_komodo = input("Provide me path to your komodo directory. E.g. /home/user/komodo/ : ")
        try:
            compile = check_output(["gcc",path_to_komodo+"src/cc/dapps/oraclefeed.c","-lm","-o",path_to_komodo+"/src/oraclefeed"])
        except subprocess.CalledProcessError as e:
            print(colorize("You've input wrong path. Please try again!", "pink"))
        else:
            #subprocess.call(["sudo","ln","-sf",path_to_komodo+"/src/oraclefeed","/usr/local/bin/oraclefeed"])
            # oraclefeed working only if executing from same directory with komodod :(
            print(colorize("oraclefeed dAPP is compiled and ready to execute as oraclefeed", "green"))
            break

    input("Press [Enter] to continue...")

def oraclefeed_run_gw():
    while True:
        path_to_komodo = input("Provide me path to your komodo executables directory. E.g. /home/user/komodo/src : ")
        try:
            subprocess.check_output("./oraclefeed", cwd=path_to_komodo,shell=True,stderr=subprocess.STDOUT)
        except FileNotFoundError as e:
            print(colorize("oraclefeed not found. Please try again!", "pink"))
        else:
            print(colorize("oraclefeed found and ready to server", "green"))
            break
    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    oracle_id = input("Input oracle id (oracle have to be Ihh data type): ")
    #oracleinfo if oracle wrong type -> again input
    pubkey = input("Input yours pubkey: ")
    format = "Ihh"
    bindtxid = input("Input your gateway bind txid: ")
    print(colorize("Please use gateways_cc_cli.py tool in other terminal window in next calls since in this oraclefeed is working"), "blue")
    subprocess.call(["oraclefeed",ac_name,oracle_id,pubkey,format,bindtxid])
    input("Press [Enter] to continue...")

#def oraclefeed_status_monitor(): would be great for future create simple node monitoring tool/method
# working with multi-instances of oraclefeed
# checking consisntancy of Ihh oracles height data

def send_kmd_gw():
    print(colorize("Please be carefull when input wallet addresses and amounts since all transactions doing in real KMD!", "pink"))
    print("Your addresses with balances: ")
    list_address_groupings()
    sendaddress = input("Input address from which you transfer KMD: ")
    recepient1 = input("Input address which belongs to pubkey which will receive tokens: ")
    amount1 = 0.0001
    recepient2 = input("Input gateway deposit address: ")
    file = open("deposits_list", "a")
    #have to show here deposit addresses for gateways created by user
    amount2 = input("Input how many KMD you want to deposit on this gateway: ")
    operation = z_sendmany_twoaddresses(sendaddress, recepient1, amount1, recepient2, amount2)
    file.writelines(operationstatus_to_txid(operation) + "\n")
    file.close()
    print("Operation proceed! " + str(operation))
    print(colorize("KMD Transaction ID: " + str(operationstatus_to_txid(operation)) + " Entry added to deposits_list file", "green"))
    input("Press [Enter] to continue...")
    # maybe have to save it in file

def gateways_claim_gw():
    ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
    gateway = input("Input gateway bindtxid you want to work with: ")
    coin = input("Input coin ticker you working with: ")
    gatewayspending = check_output(["komodo-cli","-ac_name="+ac_name,"gatewayspending",gateway,coin])
    print("Pending deposits availiable for selected gateway: ")
    print(gatewayspending)
    print("Input the details for transaction claiming now")
    bindtxid = input("Input your gateway bind txid: ")
    coin = input("Input your external coin ticker (e.g. KMD): ")
    deposittxid = input("Input yours gatewaysdeposit txid: ")
    destpub = input("Input pubkey you want to tokens appear to: ")
    amount = input("Input amount of yours claiming: ")
    claim_tx_hex = gateways_claim(ac_name, bindtxid, coin, deposittxid, destpub, amount)
    claim_tx_txid = tx_broadcaster(ac_name,claim_tx_hex["hex"])
    print("Transaction succesfully claimed: " + claim_tx_id)
    input("Press [Enter] to continue...")

def gateways_deposit_gw():
    autodeposit_choice = input("Do you want to proceed to gateway deposit of yours transaction? (y/n): ")
    if autodeposit_choice == 'y':
        ac_name = str(input("Input AC name with which you want to work (exmp: ORCL1): "))
        bindtxid = input("Input your gateway bind txid: ")
        coin = input("Input your external coin ticker (e.g. KMD): ")
        # have to hold till it have at least one confirmation
        cointxid = input("Input your deposit txid: ")
        destpub = input("Input pubkey which claim deposit: ")
        amount = input("Input amount of your deposit: ")
        deposit_raw = gateways_deposit(ac_name, bindtxid, coin, cointxid, destpub, amount)
        deposit_txid = tx_broadcaster(ac_name,deposit_raw["hex"])
        print(colorize("Deposit is successful! Deposit request txid: " + deposit_txid \
         + " After gatewaysclaim node confirmation you will get the tokens", "green"))
         #have to save it to file
    elif autodeposit_choice == 'n':
        pass
    else:
        print("Input y or n")
    input("Press [Enter] to continue...")


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
    { "Run oraclefeed dAPP - NOT WORK CORRECT NOW PLEASE RUN DAPP MANUALLY": oraclefeed_run_gw },
    { "Send KMD gateway deposit transaction": send_kmd_gw },
    { "Execute gateways deposit": gateways_deposit_gw },
    # { "Claim gateways deposit": gateways_claim },
    { "Execute gateways claim": gateways_claim_gw },
    { "Execute gateways withdrawal": tokens_witdrawal_gw },
    { "Exit": exit },
]

def signal_handler(signal, frame):
     os.execv(__file__, sys.argv)

def main():
    while True:
        os.system('clear')
        signal.signal(signal.SIGINT, signal_handler)
        print(colorize(header, 'pink'))
        print(colorize('CLI version 0.1 by Anton Lysakov\n', 'green'))
        for item in menuItems:
            print(colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + list(item.keys())[0])
        choice = input(">> ")
        try:
            if int(choice) < 0 : raise ValueError
            # Call the matching function
            list(menuItems[int(choice)].values())[0]()
        except (ValueError, IndexError):
            pass

if __name__ == "__main__":
    main()
