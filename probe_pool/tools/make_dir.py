# pluaron
# 20221009
# Determine if the folder exists, if not, create a new one


import os 
from probe_pool.tools.subprocess_call import Subp_call

def Mk_not_dir(dir_path, cover="no"):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        if cover == "no":
            print(f"The directory of {dir_path} already exists")
        elif cover == "yes":
            Subp_call(f"rm -rf {dir_path}")
            Subp_call(f"mkdir -p {dir_path}")
            print(f"The directory of {dir_path} relaces successfully")
    return