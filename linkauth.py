import json
import subprocess
from subprocess import check_output
import shlex
import sys
import time


def run_cmd(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8"), error.decode("utf-8")

cmd_linkauth_format = 'cleos push action -s -j -d eosio linkauth \'{"account" : "%s","code" : "%s","type" : "%s","requirement" : "social"}\' -p %s@active'
cmd_wrap_format = 'cleos wrap exec -s -j -d eosio.wrap \'%s\''
cmd_push_format = 'cleos push transaction \'%s\''

links = []
links.append({"code":"uos.activity","type":"socialactndt"})
links.append({"code":"uaccountinfo","type":"setprofile"})
links.append({"code":"uos.calcs","type":"withdrawal"})
links.append({"code":"eosio.msig","type":"propose"})
links.append({"code":"eosio.msig","type":"approve"})
links.append({"code":"eosio.msig","type":"exec"})


filename = 'soc_names'
index = 0
with open(filename) as fp:
    for name in fp:
        name = name.replace('\n', '')
        print(str(index) + " " + name)
        index += 1
        if index < 427: continue
        for link in links:
            print(link)
            cmd_linkauth = cmd_linkauth_format % (name, link["code"],link["type"],name)
            output, error = run_cmd(cmd_linkauth)
            change = json.loads(output)
            change["expiration"] = "2019-12-04T11:15:44"
            change["ref_block_num"] = 0
            change["ref_block_prefix"] = 0
            #print(json.dumps(change))


            cmd_wrap = cmd_wrap_format % json.dumps(change)
            output, error = run_cmd(cmd_wrap)
            wrap_change = json.loads(output)
            wrap_change["expiration"] = "2019-12-04T11:15:45"
            wrap_change["ref_block_num"] = 0
            wrap_change["ref_block_prefix"] = 0
            #print(json.dumps(wrap_change))


            cmd_push = cmd_push_format % json.dumps(wrap_change)
            output, error = run_cmd(cmd_push)
#            print(output)
            print(error)
            push_result = json.loads(output)
            trx_status = push_result["processed"]["receipt"]["status"]
            print(trx_status)
            if trx_status != "executed":
                print(output)
                sys.exit()

            time.sleep(1)
#        sys.exit()
