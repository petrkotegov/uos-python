import subprocess
from subprocess import check_output
import shlex
import sys
import time

filename = 'commands.txt'
with open(filename) as fp:
    for line in fp:
        print(line)
        time.sleep(0.1)
        process = subprocess.Popen(shlex.split(line), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error and 'Error' in error.decode("utf-8"):
            print(error.decode("utf-8"))
            sys.exit()
