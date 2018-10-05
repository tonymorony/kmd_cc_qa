import json
import os
import subprocess
import time
import filecmp
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

def tx_broadcaster(ac_name, hex):
    try:
        tx_id = check_output(["komodo-cli","-ac_name="+ac_name,"sendrawtransaction", hex]).decode().rstrip()
    except subprocess.CalledProcessError:
        tx_id = "Error"
    return tx_id

def get_tokens_list(ac_name):
    """Getting information about tokens availiable on AC

    Args:
      ac_name (string): name of Komodo AC, filling -ac_name=
          parameter in all komodod calls, e.g. CHIPS

     Returns:
       tokens_list (dict): list of availiable tokens
       in form of dictionary ("tokenid":"name"), e.g. (
       af789fa9a7601cd42ef79b5e12432e6ef51efe8a85ac94af05cc25b27c301098: "TOKEN1")
    """
    tokens_ids = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"tokenlist"]))
    tokens_list = {}

    for token_id in tokens_ids:
        tokens_info = json.loads(check_output(
        ["komodo-cli","-ac_name="+ac_name,"tokeninfo",token_id]))
        tokens_list[tokens_info["tokenid"]] = tokens_info["name"]
    return tokens_list

def create_token(ac_name, name, supply, description):
    """Creating new token and testing is it on blockchain

    Args:
      ac_name (string): name of Komodo AC, filling -ac_name=
          parameter in all komodod calls, e.g. CHIPS
      name (string): name of the new token
      supply (int): total tokens supply, e.g. 0.1
      description (string): token description, e.g. best coin

    Returns:
       tokenid (string): returns id of created token
     """
    is_created = False
    waiting_time = 0
    new_token = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"tokencreate",name,supply,description]))
    byte_token_id = check_output(
    ["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_token["hex"]])
    token_id = byte_token_id.decode().rstrip()

    print("Token creation transaction sent to blockchain.\n"
          "Transaction ID: " + token_id)
    while True:
        tokens_list = get_tokens_list(ac_name)
        if token_id in tokens_list.keys():
            print(bcolors.OKGREEN + "Token succesfully created!" + bcolors.ENDC)
            is_created = True
            break
        elif waiting_time > 359:
            print("Something seems to have gone wrong: 5 minutes timeout passed.")
            is_created = False
            break
        else:
            print("Token is not created yet. I will check it again in 30 seconds.\n"
                  "You already waiting {} seconds. "
                  "Max. waiting time is 300 seconds.".format(waiting_time))
            waiting_time += 30
            time.sleep(30)
    return token_id

def tokens_converter(ac_name, evalcode, token_id, pubkey, supply):
    #catch {'result': 'error', 'error': 'couldnt convert tokens'}
    try:
        convertation_id = json.loads(check_output(
        ["komodo-cli","-ac_name="+ac_name,"tokenconvert",evalcode,token_id,pubkey,supply]))
    except subprocess.CalledProcessError as e:
        print('Something is broken\ncommand: %s\noutput: %s\nreturncode:%i' % (e.cmd, e.output, e.returncode))

    return convertation_id

#def show_orders(ac_name):

#def make_trade(ac_name, ticker):

#def place_trade(ac_name, ticker):

def get_oracles_list(ac_name):
    oracles_ids = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"oracleslist"]))
    oracles_list = {}

    for oracle_id in oracles_ids:
        oracle_info = json.loads(check_output(
        ["komodo-cli","-ac_name="+ac_name,"oraclesinfo",oracle_id]))
        oracles_list[oracle_info["txid"]] = oracle_info["name"]
    return oracles_list

def oracle_create(ac_name, name, description, type):
    is_created = False
    waiting_time = 0

    new_oracle = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"oraclescreate",name,description,type]))
    byte_oracle_id = check_output(
    ["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_oracle["hex"]])
    oracle_id = byte_oracle_id.decode().rstrip()

    print("Oracle creation transaction sent to blockchain.\n"
          "Transaction ID: " + oracle_id)
    while True:
        oracles_list = get_oracles_list(ac_name)
        if oracle_id in oracles_list.keys():
            print(bcolors.OKGREEN + "Oracle succesfully created!" + bcolors.ENDC)
            is_created = True
            break
        elif waiting_time > 359:
            print("Something seems to have gone wrong: 5 minutes timeout passed.")
            is_created = False
            break
        else:
            print("Oracle is not created yet. I will check it again in 30 seconds.\n"
                  "You already waiting {} seconds. "
                  "Max. waiting time is 300 seconds.".format(waiting_time))
            waiting_time += 30
            time.sleep(30)
    return oracle_id

def oracle_register(ac_name, oracle_id, datafee):
    is_registered = False
    waiting_time = 0
    baton_returned = ""
    publisher_id = ""

    new_registration = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"oraclesregister",oracle_id,datafee]))
    byte_registration_id = check_output(
    ["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_registration["hex"]])
    batontx_id = byte_registration_id.decode().rstrip()
    print("Oracle registration transaction sent to blockchain.\n"
          "Transaction ID: " + batontx_id)
    while True:
        oracles_info = json.loads(check_output(
        ["komodo-cli","-ac_name="+ac_name,"oraclesinfo",oracle_id]))
        for entry in oracles_info["registered"]:
            baton_returned = entry["batontxid"]
        if baton_returned == batontx_id:
            print(bcolors.OKGREEN + "Oracle succesfully registered!" + bcolors.ENDC)
            is_registered = True
            break
        elif waiting_time > 359:
            print("Something seems to have gone wrong: 5 minutes timeout passed.")
            is_created = False
            break
        else:
            print("Oracle is not registered yet. I will check it again in 30 seconds.\n"
                  "You already waiting {} seconds. "
                  "Max. waiting time is 300 seconds.".format(waiting_time))
            waiting_time += 30
            time.sleep(30)
    for entry in oracles_info["registered"]:
        publisher_id = entry["publisher"]
    return publisher_id

def oracle_subscribe(ac_name, oracle_id, publisher_id, datafee):
    is_subscribed = False
    waiting_time = 0
    lifetime = 0

    new_subscription = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"oraclessubscribe",oracle_id,publisher_id,datafee]))
    byte_subscription_id = check_output(
    ["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_subscription["hex"]])
    subscription_txid = byte_subscription_id.decode().rstrip()
    print("Oracle subscription transaction sent to blockchain.\n"
          "Transaction ID: " + subscription_txid)
    while True:
        oracles_info = json.loads(check_output(
        ["komodo-cli","-ac_name="+ac_name,"oraclesinfo",oracle_id]))
        for entry in oracles_info["registered"]:
            lifetime = float(entry["lifetime"])
        if lifetime > 0 :
            print(bcolors.OKGREEN + "Succesfully subscribed on oracle!" + bcolors.ENDC)
            is_subscribed = True
            break
        elif waiting_time > 359:
            print("Something seems to have gone wrong: 5 minutes timeout passed.")
            is_created = False
            break
        else:
            print("You not subscribed on Oracle yet. I will check it again in 30 seconds.\n"
                  "You already waiting {} seconds. "
                  "Max. waiting time is 300 seconds.".format(waiting_time))
            waiting_time += 30
            time.sleep(30)
    return is_subscribed

def oracle_utxogen(ac_name, oracle_id, utxo_num, pubkey, data_fee):
    for i in range(int(utxo_num)):
        new_subscription = oracle_subscribe(ac_name, oracle_id, pubkey, data_fee)

def file_oraclize(ac_name, oracle_id, filename):
    baton_returned = ""
    waiting_time = 0
    is_oraclized = False
    lines_oraclized = 0
    lines_count = len(open(filename).readlines(  ))
    file = open(filename, "r")

    for line in file:
        new_oraclesdata = json.loads(check_output(["komodo-cli","-ac_name="+ac_name,"oraclesdata",oracle_id,line]))
        byte_oraclesdata_id = check_output(["komodo-cli","-ac_name="+ac_name,"sendrawtransaction",new_oraclesdata["hex"]])
        batontx_id = byte_oraclesdata_id.decode().rstrip()
        print("Line oraclizing transaction sent to blockchain.\n"
              "Transaction ID: " + batontx_id)
        while True:
            oracles_info = json.loads(check_output(["komodo-cli","-ac_name="+ac_name,"oraclesinfo",oracle_id]))
            for entry in oracles_info["registered"]:
                baton_returned = entry["batontxid"]
            if baton_returned == batontx_id:
                print(bcolors.OKGREEN + "Line succesfully oraclized!" + bcolors.ENDC)
                lines_oraclized = lines_oraclized + 1
                print("Oraclized {} lines from {}".format(lines_oraclized, lines_count))
                waiting_time = 0
                break
            elif waiting_time > 359:
                print("Something seems to have gone wrong: 5 minutes timeout passed.")
                is_created = False
                break
            else:
                print("Line is not oraclized yet. I will check it again in 30 seconds.\n"
                      "You already waiting {} seconds. "
                      "Max. waiting time is 300 seconds.".format(waiting_time))
                waiting_time += 30
                time.sleep(30)
    is_oraclized = True
    return is_oraclized

def oracle_read(ac_name, oracle_id, filename, depth):
    is_readed = False
    baton_returned = ""
    file = open(filename, "w")
    oracles_data = []

    oracles_info = json.loads(check_output(["komodo-cli","-ac_name="+ac_name,"oraclesinfo",oracle_id]))
    for entry in oracles_info["registered"]:
        baton_returned = entry["batontxid"]

    oracles_jsondata = json.loads(check_output(["komodo-cli","-ac_name="+ac_name,"oraclessamples",oracle_id,baton_returned,depth]))
    for sample in oracles_jsondata["samples"]:
        file.write(sample[0] + "\n")
    is_readed = True
    return is_readed

def gateways_bind(ac_name,token_id,oracle_id,coinname,tokensupply,pubkey):
    try:
        tx_id =  json.loads(check_output(["komodo-cli","-ac_name="+ac_name,"gatewaysbind",token_id,oracle_id,coinname,tokensupply,"1","1",pubkey]))
    except subprocess.CalledProcessError:
        tx_id = "Error"
    return tx_id

def gateways_deposit(acname, bindtxid, coin, cointxid, destpub, amount):
    #bindtxid height coin cointxid claimvout deposithex proof destpub amount
    raw_transaction = json.loads(check_output(["komodo-cli","getrawtransaction",cointxid,"1"]))
    height = raw_transaction["height"]
    claimvout = "0" #have to recheck it
    deposithex = raw_transaction["hex"]
    proof = (check_output(["komodo-cli","gettxoutproof","[\"{}\"]".format(cointxid)])).decode().rstrip()
    print(["komodo-cli","-ac_name="+acname,"gatewaysdeposit",bindtxid,str(height),coin,cointxid,claimvout,deposithex,proof, destpub, amount])
    gateways_deposit_txid = json.loads(check_output(["komodo-cli","-ac_name="+acname,"gatewaysdeposit",bindtxid,str(height),coin,cointxid,claimvout,deposithex,proof, destpub, amount]).decode().rstrip())
    return gateways_deposit_txid

def gateways_claim(acname, bindtxid, coin, deposittxid, destpub, amount):
    #gatewaysclaim bindtxid coin deposittxid destpub amount
    gateways_claim_txid = json.loads(check_output(["komodo-cli","-ac_name="+acname,"gatewaysclaim", bindtxid, coin, deposittxid, destpub, amount]).decode().rstrip())
    return gateways_claim_txid

def int_to_hex(input_filename):
    with open(input_filename, 'r') as file:
        data = file.readlines()
    with open(input_filename, 'w') as file:
        for entry in data:
            file.writelines(hex(int(entry))[2:] + "\n")

def io_compare(input_filename, output_filename):
    compare = filecmp.cmp(input_filename, output_filename, shallow=True)
    return compare

def z_sendmany_twoaddresses(sendaddress, recepient1, amount1, recepient2, amount2):
    json_sendaddress = "\"{}\"".format(sendaddress)
    sending_block = "[{{\"address\":\"{}\",\"amount\":{}}},{{\"address\":\"{}\",\"amount\":{}}}]".format(recepient1, amount1, recepient2, amount2)
    print(sending_block)
    operation_id = (check_output(["komodo-cli","z_sendmany",sendaddress,sending_block])).decode().rstrip()
    return operation_id

def operationstatus_to_txid(zstatus):
    sending_block = "[\"{}\"]".format(zstatus)
    operation_json = json.loads(check_output(["komodo-cli","z_getoperationstatus",sending_block]))[0]
    txid = dict(operation_json["result"].items())["txid"]
    return txid

def list_address_groupings():
    address_list = json.loads(check_output(["komodo-cli","listaddressgroupings"]))
    print(address_list)
