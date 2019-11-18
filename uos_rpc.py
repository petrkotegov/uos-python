import requests
import json
import os

STAGING_URL = "https://staging-api-node-2.u.community:7888"
PROD_URL = "http://127.0.0.1:8888"

def get_accounts_batch(code = "", table = "", limit = 10, lower_bound = ""):
    get_scope_url = PROD_URL + "/v1/chain/get_table_by_scope"
    params = {}
    params["code"] = code
    params["table"] = table
    params["limit"] = limit
    params["lower_bound"] = lower_bound
    response = requests.put(get_scope_url, data=json.dumps(params))
    json_res = json.loads(response.text)
    rows = json_res["rows"]
    names_map = map(lambda x : x["scope"], rows)
    names_list = list(names_map)
    more = json_res["more"]
    return {'names':names_list,'more':more}

def get_table_rows(code, scope, table):
    get_table_url = PROD_URL + "/v1/chain/get_table_rows"
    params = {}
    params["code"] = code
    params["scope"] = scope
    params["table"] = table
    response = requests.put(get_table_url, data = json.dumps(params))
    json_res = json.loads(response.text)
    return json_res

def get_block(block_num):
    get_block_url = STAGING_URL + "/v1/chain/get_block"
    params = {}
    params["block_num_or_id"] = block_num
    response = requests.put(get_block_url, data = json.dumps(params))
    return json.loads(response.text)

def get_accinfo(name):
    get_acc_url = PROD_URL + "/v1/chain/get_account"
    params = {}
    params["account_name"] = name
    response = requests.put(get_acc_url, data=json.dumps(params))
    json_res = json.loads(response.text)
    return json_res


def get_all_accounts(code = "eosio", table = "userres", first_batch = 5, other_batches = 100):
    res = get_accounts_batch(code,table,first_batch)
    #print(res)
    names = res["names"]
    more = res["more"]
    while more != "":
        res = get_accounts_batch(code,table,other_batches,more)
        #print(res)
        names.extend(res["names"])
        more = res["more"]
        #print(more)
    return names

def create_acc_command(name):
    begin = 'cleos system newaccount accregistrar '
    end = ' EOS6jydCjcB3MpJmXUHtrzwVEF4ndVcsc8y4qdEV2E6HtVk4QummQ --stake-net "1.0000 UOS" --stake-cpu "1.0000 UOS" --buy-ram-kbytes 8'
    command = begin + name + end
    return command

def update_perm_command(name, perm):
    begin = 'cleos set account permission '
    command = begin + name + " " + perm["perm_name"] + " '" + json.dumps(perm["required_auth"]) + "' " + perm["parent"]
    if perm["perm_name"] == 'owner':
        command = command + " " + "-p " + name + "@owner"
    return command

def get_permissions(names):
    command_list = []
    for name in names:
        unusual = False
        line = [name]
        accinfo = get_accinfo(name)
        for perm in accinfo["permissions"]:
            line.append(perm["perm_name"])
            auth = perm["required_auth"];
            line.append(auth["threshold"])
            if auth["keys"]:
                line.append("keys")
                line.append(len(auth["keys"]))
            if auth["accounts"]:
                line.append("accounts")
                line.append(len(auth["accounts"]))
            if auth["waits"]:
                line.append("waits")
                line.append(len(auth["waits"]))
            if perm["perm_name"] not in ["active","owner","social"]:
                unusual = True
            if auth["threshold"] != 1:
                unusual = True
            if len(auth["keys"]) != 1:
                unusual = True
            if auth["accounts"] or auth["waits"]:
                unusual = True
        if unusual:
            continue
        perms = {perm["perm_name"] : perm for perm in accinfo["permissions"]}
        with open("commands.txt", "a") as comfile:
            comfile.write(create_acc_command(name) + "\n")
            if 'social' in perms.keys(): comfile.write(update_perm_command(name, perms['social']) + "\n")
            comfile.write(update_perm_command(name, perms['active']) + "\n")
            comfile.write(update_perm_command(name, perms['owner']) + "\n")

def get_all_emission(names):
    for name in names:
        res = get_table_rows("eosio",name,"userres")
        print(res)

def linux_command():
    os.system('/home/peter/Cleos/cleos.sh')

