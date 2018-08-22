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
