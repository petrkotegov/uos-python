import json
import os
import subprocess
from subprocess import check_output
import shlex
import sys
import uos_rpc

names = uos_rpc.get_all_accounts()

result = []
for name in names:
    if "testuser" in name: continue

    command = "cleos get table eosio.token " + name + " accounts"
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if "UOSF" not in str(output): continue
    resp = json.loads(output)
    for row in resp["rows"]:
        if "UOSF" in str(row["balance"]):
            balance = row["balance"].replace(" UOSF", "")
            print(name + "\t" + balance)
            result.append({"name":name, "balance":balance})

print("")

result = sorted(result, key = lambda x: float(x["balance"]), reverse=True)
str_result = [x["name"] + "\t" + x["balance"] for x in result]
print(*str_result, sep = "\n")

