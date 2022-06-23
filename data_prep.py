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


def preprocess_data(data):
    data["TxBitRate"].replace([r"\N", r"\\N", r"\\N\\N"], np.nan, inplace=True)
    data["RxBitRate"].replace([r"\N", r"\\N", r"\\N\\N"], np.nan, inplace=True)
    data["TxBitRate"] = data["TxBitRate"].astype(float)
    data["RxBitRate"] = data["RxBitRate"].astype(float)

    return data


# %%
def execute_command(command, col_names_in_command=None):
    mydb, conn = connect_to_db()
    mycursor = mydb.cursor()
    mycursor.execute("use new_database")
    mycursor.execute(command)
    data = mycursor.fetchall()
    # encapsulate data into pandas dataframe
    data = pd.DataFrame(data)
    if col_names_in_command is not None:
        data.columns = col_names_in_command
    return data


def connect_to_db(username="root", password="NewPassword", database=None):
    try:
        if database != None:
            mydb = mysql.connector.connect(
                host="localhost", user=username, passwd=password, database=database
            )
        else:
            mydb = mysql.connector.connect(
                host="localhost",
                user=username,
                passwd=password,
            )

        print("connection_established")
        return mydb, True
    except:
        return None, False
