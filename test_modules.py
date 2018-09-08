import json
import os
import subprocess
import time
from subprocess import check_output

def get_tokens_list(ac_name):
    """Getting information about tokens availiable on AC

    Args:
      ac_name (string): name of Komodo AC, filling -ac_name=
          parameter in all komodod calls, e.g. CHIPS

     Returns:
       tokens_list (dict): list of availiable tokens
       in form of dictionary ("name":"tokenid"), e.g. ("TOKEN1",
       af789fa9a7601cd42ef79b5e12432e6ef51efe8a85ac94af05cc25b27c301098)
    """
    tokens_ids = json.loads(check_output(
    ["komodo-cli","-ac_name="+ac_name,"tokenlist"]))
    tokens_list = {}

    for token_id in tokens_ids:
        tokens_info = json.loads(check_output(
        ["komodo-cli","-ac_name="+ac_name,"tokeninfo",token_id]))
        tokens_list[tokens_info["name"]] = tokens_info["tokenid"]
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
       is_created (bool): returns is token with pre-set params
       was found on the blockchain in period, within 5 minutes.
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
        if token_id in tokens_list.values():
            print("Token succesfully created!")
            is_created = True
            break
        elif waiting_time > 359:
            print("Something seems to have gone wrong: 5 minutes timeout passed.")
            is_created = False
            break
        else:
            print("Token is not created yet. I will check it again in 60 seconds.\n"
                  "You already waiting {} seconds. "
                  "Max. waiting time is 300 seconds.".format(waiting_time))
            waiting_time += 60
            time.sleep(60)
    return is_created

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
        oracles_list[oracle_info["name"]] = oracle_info["txid"]
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
        if oracle_id in oracles_list.values():
            print("Oracle succesfully created!")
            is_created = True
            break
        elif waiting_time > 359:
            print("Something seems to have gone wrong: 5 minutes timeout passed.")
            is_created = False
            break
        else:
            print("Oracle is not created yet. I will check it again in 60 seconds.\n"
                  "You already waiting {} seconds. "
                  "Max. waiting time is 300 seconds.".format(waiting_time))
            waiting_time += 60
            time.sleep(60)
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
            print("Oracle succesfully registered!")
            is_registered = True
            break
        elif waiting_time > 359:
            print("Something seems to have gone wrong: 5 minutes timeout passed.")
            is_created = False
            break
        else:
            print("Oracle is not registered yet. I will check it again in 60 seconds.\n"
                  "You already waiting {} seconds. "
                  "Max. waiting time is 300 seconds.".format(waiting_time))
            waiting_time += 60
            time.sleep(60)
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
            print("Succesfully subscribed on oracle!")
            is_registered = True
            break
        elif waiting_time > 359:
            print("Something seems to have gone wrong: 5 minutes timeout passed.")
            is_created = False
            break
        else:
            print("You not subscribed on Oracle yet. I will check it again in 60 seconds.\n"
                  "You already waiting {} seconds. "
                  "Max. waiting time is 300 seconds.".format(waiting_time))
            waiting_time += 60
            time.sleep(60)
    return is_subscribed
