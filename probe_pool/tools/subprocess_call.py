# pluaron
# 20221009
# Using CLI commands and their parallelism in a Python environment

import subprocess as subp

def Subp_call(cmd):
    print(cmd)
    subp.check_call(cmd, shell=True)
    return


def Subp_popen(cmd):
    print(cmd)
    process = subp.Popen(cmd, shell=True)
    return process


## test
if __name__ == "__main__":
    process = Subp_popen("top")
    #process.wait()
    Subp_call("mkdir test_check_call")
