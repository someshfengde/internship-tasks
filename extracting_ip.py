#%% 

import pandas as pd 
import re

# %%
def required_val(file_path = "./ipconfig_output.txt"):
    required_op = ""
    with open(file_path , "r") as f: 
        str_from_ip = str(f.read())
        output_finding = str_from_ip[re.search("inet addr:", str_from_ip).span()[0]:re.search("inet addr:", str_from_ip).span()[1]+ 20] 
        list_op  = output_finding.split(" ")
        for i in list_op:
            if i == '':
                break 
            else:
                required_op += i
    
    return required_op.split(":")
# %%
required_val()
# %%

# creating rest api for accessing particular sql query 


# %%

# %%
