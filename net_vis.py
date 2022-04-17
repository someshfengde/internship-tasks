
#%%
# importing required libraries.
import pandas as pd
import numpy as np 
import dash 
import dash_html_components as html 
import dash_core_components as dcc 
from dash.dependencies import Input, Output 
import plotly.graph_objs as go 
import networkx as nx
class clr:
    S = '\033[1m' + '\033[96m'
    E = '\033[0m'

# %%
# reading the data from dataframe in this 
# case I am combining the data I have. 
scan_1 = pd.read_csv("nap-scan.csv")
scan_2 = pd.read_csv("nap-scan-2.csv")
cols = ["ApId",
"NApMacAddress",
"LastCheckinTime",
"LastStatusId",         
"SSID",                 
"TSF",                  
"Frequency",            
"Rssi",                  
"PrimaryChannel",       
"SecondaryChannel",     
"ChannelWidth",         
"StaChannelWidth",      
"FirstCenterFrequency", 
"SecondCenterFrequency",
"Authentication",       
"Security"]
scan_1.columns = cols
# checking the column 
print(scan_2[r'\N'].value_counts(), len(scan_2[r'\N']))
# seems like the \N col is having only newline values dropping it 
scan_2 = scan_2.drop(r"\N", axis = 1 ) 
scan_2.columns = cols
total_scan = scan_1.append(scan_2, ignore_index=True)

# %%
total_scan
# %%
def draw_graph(id_ind,df):
    """
        Inputs: 
            id_ind APid which we want to visualize
            df: dataframe which contains Ap_id ,RSSI values and channel values
        Outputs:
            plotly interactive graph with visualizing nodes based on Rssi distance
    """
    data = df.query(f"ApId == {str(id_ind)}")
    if len(data) ==0 :
        #raise Exception 
        print(clr.S + "dataframe doesn't contain any information about the node provided in inputs" + clr.E)
    G = nx.Graph()
    point_data = []
    for x in data["Rssi"]:
        point_data.append((x,0))
    G.add_edges_from(point_data)
    G.add_nodes_from(point_data)
    pos = nx.layout.spring_layout(G)
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),  
        line=dict(width=2)))
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))
        node_trace['text']+=tuple([node_info])
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Network Graph of '+str(num_nodes)+' rules',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    fig.show()
    return fig
draw_graph(2187, total_scan)

# %%

# %%

# %%

# %%
