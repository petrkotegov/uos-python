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
head = []
result = []
with open(filename, 'r') as fp:
#    print(input_data)
    for line in fp:
#        print(line)
#        print(entry)

        if index == 0:
           head = line.split(";")
           index += 1
           continue

        values = line.split(";")
        entry = dict(zip(head, values))

#        print(sum)
#        print(values)
#        print(eos_value)
#        print('%.4f' % uos_value)

        name = entry["name"]
        type = entry["type"]
        importance = float(entry["importance"])
#        balance = importance / 0.1095735606 * 30000000
        balance = 2700

        if type != "ACCOUNT" or len(name) != 12: continue
        if "." in name or "-" in name or "initbp" in name or "initcalc" in name: continue

        result.append({"name":name, "balance":balance})

        sum += importance

        print(name + " " + ('%.10f' % importance) + " " + ('%.10f' % sum) + " " + ('%.4f' % balance) )


#        cr_command = create_acc_command(name, key)
#        tr_command = ''
#        if mode == "direct": tr_command = direct_transfer_command(name, balance)
#        if mode == "time": tr_command = time_transfer_command(name, balance)
#        if mode == "activity": tr_command = active_transfer_command(name, balance)

#        print(cr_command)
#        print(tr_command)

#        with open(res_filename, "a") as comfile:
#            comfile.write(cr_command + "\n")
#            comfile.write(tr_command + "\n")

        index += 1
        print(index)
#        if index >= 10: break

#print(interactions)
print(index)
print(sum)
#sorted_list = sorted(full_list, key=lambda x: x["sum"], reverse=True)
#print(*(sorted_list[0:10]), sep = "\n")
result = sorted(result, key = lambda x: x["balance"], reverse=True)
str_result = [x["name"] + "\t" + ('%.4f' % x["balance"]) for x in result]
print(*str_result, sep = "\n")
