import json
import os
import sys
import uos_rpc

filename = 'transactions_cache.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

if not os.path.isfile(filename):
    print("file does not exist: " + filename)
    sys.exit()

def command_histactndt(tran):
    data_json = json.dumps(tran["data"])
    if "'" in data_json:
        data_json = data_json.replace("'", "'" + '"' + "'" + '"' + "'")
    return "cleos push action uos.activity histactndt '" + data_json + "' -p uoshistorian"

def command_socialactndt(tran):
    block = uos_rpc.get_block(tran["block_num"])
    timestamp = block["timestamp"]
    timestamp = timestamp[0:19] + "Z"
    new_data = dict(tran["data"])
    new_data["timestamp"] = timestamp
    new_data["acc"] = "uoshistorian"
    if "action_data" not in new_data.keys():
        new_data["action_data"] = ""
    data_json = json.dumps(new_data)
    if "'" in data_json:
        data_json = data_json.replace("'", "'" + '"' + "'" + '"' + "'")
    return "cleos push action uos.activity histactndt '" + data_json + "' -p uoshistorian"


index = 0
interactions = {};
with open(filename) as fp:
    for line in fp:
        tran = json.loads(line)
#        if tran["action"] in ["transfer","makecontent","usertouser","usertocont","makecontorg","socialaction","socialactndt","histactndt"]:
#            continue
#        if tran["action"] != "histactndt": continue
        if tran["action"] != "socialactndt": continue
#        if tran["action"] != "socialaction": continue
#        print(line)
#        command = command_histactndt(tran)
        command = command_socialactndt(tran)

#        print(command)
#        with open("histactndt.txt", "a") as comfile:
        with open("socialactndt.txt", "a") as comfile:
#        with open("socialaction.txt", "a") as comfile:
            comfile.write(command + "\n")

#        timestamp = tran["data"]["timestamp"]
#        action_json = json.loads(tran["data"]["action_json"])
#        interaction = action_json["interaction"]
#        if interaction not in interactions.keys():
#            interactions[interaction] = 0;
#        interactions[interaction] += 1
#        print(tran["block_num"] + " " + action_json["interaction"])
        index += 1
        print(index)
#        if index >= 1: break
#        if error and 'Error' in error.decode("utf-8"):
#            print(error.decode("utf-8"))
#            sys.exit()

#print(interactions)
print(index)
