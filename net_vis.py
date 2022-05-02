
#%%
# importing required libraries.
import pandas as pd
import numpy as np 
import dash 
from dash import html 
from dash import dcc 
from dash.dependencies import Input, Output 
import plotly.graph_objs as go 
import networkx as nx
import matplotlib.pyplot as plt
class clr:
    S = '\033[1m' + '\033[96m'
    E = '\033[0m'

# %%
# # reading the data from dataframe in this 
# # case I am combining the data I have. 
# scan_1 = pd.read_csv("nap-scan.csv")
# scan_2 = pd.read_csv("nap-scan-2.csv")
# cols = ["ApId",
# "NApMacAddress",
# "LastCheckinTime",
# "LastStatusId",         
# "SSID",                 
# "TSF",                  
# "Frequency",            
# "Rssi",                  
# "PrimaryChannel",       
# "SecondaryChannel",     
# "ChannelWidth",         
# "StaChannelWidth",      
# "FirstCenterFrequency", 
# "SecondCenterFrequency",
# "Authentication",       
# "Security"]
# scan_1.columns = cols
# # checking the column 
# print(scan_2[r'\N'].value_counts(), len(scan_2[r'\N']))
# # seems like the \N col is having only newline values dropping it 
# scan_2 = scan_2.drop(r"\N", axis = 1 ) 
# scan_2.columns = cols
# total_scan = scan_1.append(scan_2, ignore_index=True)

# %%
# total_scan
# %%
def draw_graph(id_ind,df, to_vis = "Rssi"):
    """
        Inputs: 
            id_ind APid which we want to visualize
            df: dataframe which contains Ap_id ,RSSI values and channel values
        Outputs:
            plotly interactive graph with visualizing nodes based on Rssi distance
    """
    
    data = df.query(f"ApId == {str(id_ind)}")
    fig  = plt.figure()
    if len(data) ==0 :
        #raise Exception 
        print(clr.S + "dataframe doesn't contain any information about the node provided in inputs" + clr.E)
    G = nx.Graph()
    point_data = []
    for x in data[to_vis]:
        point_data.append((x,0))
    G.add_edges_from(point_data)
    plt.title(f"Graph of AP {id_ind}")
    pos = nx.layout.spring_layout(G)
    nx.draw(G, with_labels=True, node_size=10, node_color='blue', edge_color='red', pos=pos)

# draw_graph(678, total_scan)

# # %%

# total_scan.query("ApId == 678")['Frequency'].value_counts()
# %%
