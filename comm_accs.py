import json
import os
import sys
import uos_rpc

filename = ''
if len(sys.argv) > 1:
    filename = sys.argv[1]

if not os.path.isfile(filename):
    print("file does not exist: " + filename)
    sys.exit()

def create_acc_command(name, key):
    begin = 'cleos system newaccount eosio '
    if (len(name) < 12):
        begin = 'cleos system newaccount eosio '
    end = ' --stake-net "1.0000 UOS" --stake-cpu "1.0000 UOS" --buy-ram-kbytes 8'
    command = begin + name + " " + key + end
    return command

def direct_transfer_command(name, sum):
    begin = 'cleos transfer uos.holder '
    command = begin + name + ' "' +  ('%.4f' % sum) + ' UOS"'
    return command


index = 0
interactions = {};
with open(filename) as fp:
    for line in fp:
#        print(line)
        values = line.split("\t")
        name = values[0]
        key = values[1]
        balance = float(values[2])
        cr_command = create_acc_command(name, key)
        tr_command = direct_transfer_command(name, balance)

        print(cr_command)
        print(tr_command)
        with open("community_acc_commands.txt", "a") as comfile:
            comfile.write(cr_command + "\n")
            comfile.write(tr_command + "\n")


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
