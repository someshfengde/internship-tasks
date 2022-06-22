import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import json 
import dash_bootstrap_components as dbc
from pyparsing import dblSlashComment 

dash.register_page(__name__, path="/database-sucessful")

layout = html.Div(
    children=[
        html.H1(id="dash_div", children="This is our Analytics page"),
        dbc.Button("click_to_see_data" , id = "click_to_see_data"),
        html.Div(id="table-container",),
    ]
)

@callback(
    Output("table-container", "children"),
    [Input("click_to_see_data", "n_clicks"),
    Input("store-data", "data")],
)
def update_output(n_clicks, data):
    print("arrived here ! ")
    print(n_clicks)
    print(data)
    print("username should be " , data)
    x = json.loads(data)
    print("loaded data ")
    print(x, "---------------------")
    return x["username"]
