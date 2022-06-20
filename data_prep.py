#%%
import pandas as pd
import numpy as np
from pyparsing import col
# connect to mysql dataset
import mysql.connector
import pandas as pd
import numpy as np
from pyparsing import col

# %%


def read_and_return_data():
    data = pd.read_csv("new_whole_data1.csv", sep=",")
    data["TxRateBitrate"].replace([r"\N", r"\\N", r"\\N\\N"], np.nan, inplace=True)
    data["RxRateBitrate"].replace([r"\N", r"\\N", r"\\N\\N"], np.nan, inplace=True)
    data["TxRateBitrate"] = data["TxRateBitrate"].astype(float)
    data["RxBitRate"] = data["RxBitRate"].astype(float)
    return data


# function to connect to database
def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="NewPassword",
        database="new_database",
    )   
    return mydb


def preprocess_data(data):
    data["TxBitRate"].replace([r"\N", r"\\N", r"\\N\\N"], np.nan, inplace=True)
    data["RxBitRate"].replace([r"\N", r"\\N", r"\\N\\N"], np.nan, inplace=True)
    data["TxBitRate"] = data["TxBitRate"].astype(float)
    data["RxBitRate"] = data["RxBitRate"].astype(float)

    return data

# %%
def execute_command(command, col_names_in_command=None):
    mydb = connect_to_db()
    mycursor = mydb.cursor()
    mycursor.execute(command)
    data = mycursor.fetchall()
    # encapsulate data into pandas dataframe
    data = pd.DataFrame(data)
    if col_names_in_command is not None:
        data.columns = col_names_in_command
    return data



