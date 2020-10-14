# -*- encoding: utf-8 -*-




import subprocess
import os
import sys


def unixping(ip):
    try:
        p = subprocess.Popen(["ping -c 1 -W 20 " +ip],stdin = subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)
        out = p.stdout.read()

        if "ttl" in str(out):
            return ip
        else:
            return False

    except:

        return False

def winping(ip):
    try:
        p = subprocess.Popen(['ping','-n','1','-w','20',ip],
                    stdout=subprocess.PIPE,
                    stdin = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True)
        output = p.stdout.read().decode("gbk").upper()

        if "TTL" in output:
            return  ip
        else:
            return False
    except:
        return False
    
    
if __name__ == "__main__":
    ip = sys.argv[1]
    if os.name =="nt":
        winping(ip)
    else:
        unixping(ip)
