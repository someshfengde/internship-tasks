#%%
import pandas as pd
import numpy as np
from pyparsing import col


# %%


def read_and_return_data():
    data = pd.read_csv("whole_data.csv", sep=",")
    return data
