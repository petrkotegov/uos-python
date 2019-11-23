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

def create_acc_command(name, key):
    begin = 'cleos system newaccount accregistrar '
    if (len(name) < 12):
        begin = 'cleos system newaccount eosio '
    end = ' --stake-net "1.0000 UOS" --stake-cpu "1.0000 UOS" --buy-ram-kbytes 8'
    command = begin + name + " " + key + end
    return command

def transfer_command(name, sum):
    begin = 'cleos transfer uos.holder uosactvlock1 "'
    command = begin + ('%.4f' % sum) + '" "' + name + '"'
    return command


index = 0
sum = 0
full_list = []
with open(filename) as fp:
    for line in fp:
#        print(line)
        values = line.split(",")
        values[:] = [x.replace('"',"").replace("\n","") for x in values]
        eos_value = float(values[3])
        uos_value = round(eos_value / 10, 4);

#        entry = {}
#        entry["name"] = values[1]
#        entry["key"] = values[2]
#        entry["sum"] = eos_value
#        full_list.append(entry)

        sum += uos_value

#        print(sum)
#        print(values)
#        print(eos_value)
#        print('%.4f' % uos_value)

        cr_command = create_acc_command(values[1], values[2])
        tr_command = transfer_command(values[1], uos_value)

#        print(cr_command)
#        print(tr_command)

        with open("eos_snapshot.txt", "a") as comfile:
            comfile.write(cr_command + "\n")
            comfile.write(tr_command + "\n")

        index += 1
        print(index)
#        if index >= 10: break

#print(interactions)
print(index)
#print(sum)
#sorted_list = sorted(full_list, key=lambda x: x["sum"], reverse=True)
#print(*(sorted_list[0:10]), sep = "\n")
