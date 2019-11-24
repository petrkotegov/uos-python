import json
import os
import sys
import uos_rpc

filename = 'snapshot.csv'
if len(sys.argv) > 1:
    filename = sys.argv[1]
if not os.path.isfile(filename):
    print("file does not exist: " + filename)
    sys.exit()

res_filename = ''
if len(sys.argv) > 2:
    res_filename = sys.argv[2]
if not res_filename:
    print("no output file")
    sys.exit()

mode = ''
if len(sys.argv) > 3:
    mode = sys.argv[3]
if mode not in ['direct', 'time', 'activity']:
    print("unknown mode: " + mode)
    sys.exit()

def create_acc_command(name, key):
    begin = 'cleos system newaccount accregistrar '
    if (len(name) < 12):
        begin = 'cleos system newaccount eosio '
    end = ' --stake-net "1.0000 UOS" --stake-cpu "1.0000 UOS" --buy-ram-kbytes 8'
    command = begin + name + " " + key + end
    return command

def direct_transfer_command(name, sum):
    begin = 'cleos transfer uos.holder '
    command = begin + name + ' "' +  ('%.4f' % sum) + ' UOS"'
    return command

def time_transfer_command(name, sum):
    begin = 'cleos transfer uos.holder uostimelock1 "'
    command = begin + ('%.4f' % sum) + ' UOS" "' + name + '"'
    return command

def active_transfer_command(name, sum):
    begin = 'cleos transfer uos.holder uosactvlock1 "'
    command = begin + ('%.4f' % sum) + ' UOS" "' + name + '"'
    return command

if os.path.exists(res_filename):
    os.remove(res_filename)

index = 0
sum = 0
full_list = []
input_str = {}
with open(filename, 'r') as fp:
    input_str = fp.read()
    input_data = json.loads(input_str)
#    print(input_data)
    for entry in input_data:
#        print(line)
#        print(entry)

        sum += float(entry["balance"])

#        print(sum)
#        print(values)
#        print(eos_value)
#        print('%.4f' % uos_value)
        name = entry["eos_account"]
        key = entry["eos_pk"]
        balance = float(entry["balance"])

        cr_command = create_acc_command(name, key)
        tr_command = ''
        if mode == "direct": tr_command = direct_transfer_command(name, balance)
        if mode == "time": tr_command = time_transfer_command(name, balance)
        if mode == "activity": tr_command = active_transfer_command(name, balance)

        print(cr_command)
        print(tr_command)

        with open(res_filename, "a") as comfile:
            comfile.write(cr_command + "\n")
            comfile.write(tr_command + "\n")

        index += 1
        print(index)
#        if index >= 10: break

#print(interactions)
print(index)
print(sum)
#sorted_list = sorted(full_list, key=lambda x: x["sum"], reverse=True)
#print(*(sorted_list[0:10]), sep = "\n")
