#%%
import pandas as pd 
import numpy as np
from pyparsing import col 


# %%

def read_and_return_data():
    data = pd.read_csv("uc_client_logs (1).csv", sep = ",")
    return data 
