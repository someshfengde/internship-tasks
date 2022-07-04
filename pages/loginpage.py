import dash
from dash import html, dcc, callback, Input, Output, State
import mysql.connector
import dash_bootstrap_components as dbc
from dash import html
import json

dash.register_page(__name__, path="/")
email_input = dbc.Row(
    [
        dbc.Label("Username"),
        dbc.Input(type="username", id="username", placeholder="Enter username"),
        dbc.FormText(
            "Enter username for accessing database",
            color="secondary",
        ),
    ],
    className="text-black p-4 mb-3",
)

password_input = dbc.Row(
    [
        dbc.Label("Password"),
        dbc.Input(
            type="password",
            id="password",
            placeholder="Enter password",
        ),
        dbc.FormText(
            "A password stops mean people taking your stuff", color="secondary"
        ),
        # dbc.Button("Submit", className="p-4 mb-3", color="primary", id="submit-button"),
    ],
    className="p-4 mb-3",
)
submit_button = dbc.Row(
    [dbc.Button("Submit", className="p-4 mb-3", color="primary", id="submit-button")],
    className="p-4 mb-3",
)

# form = dbc.Form([email_input, password_input ,submit_button], id = "form_input")


form = (
    dbc.Row(
        [
            dbc.Label("Username"),
            dbc.Row(
                dbc.Input(type="username", placeholder="Enter username", id="username"),
                className="me-3",
            ),
            dbc.Label("Password"),
            dbc.Row(
                dbc.Input(type="password", placeholder="Enter password", id="password"),
                className="me-3",
            ),
            html.Br(),
            dbc.Row(dbc.Button("submit", color="primary", id="submit-button")),
        ],
        className="g-2",
    ),
)


layout = html.Div(
    children=[
        html.H1(
            children="Login to the database here!",
            className="bg-primary text-white p-4 mb-2 text-center",
        ),
        html.Div(children=form, className="p-4 mb-2 text-bold"),
        html.Div(id="Outdiv"),
    ]
)


def connect_to_db(username="root", password="NewPassword"):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=username,
            passwd=password,
        )
        print("connection_established")
        return mydb, True
    except:
        return None, False


@callback(
    [
        Output("store-data", "data"),
        Output("Outdiv", "children"),
    ],
    [
        Input("username", "value"),
        Input("password", "value"),
        Input("submit-button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def handle_submit(username, password, clicked):
    print(f"username and password we are getting {username},  {password}")
    data_dum = {"username": None, "password": None}
    if clicked:
        print("clicked")
        db, connection = connect_to_db(username, password)
        if connection:
            data_dum = {"username": username, "password": password}
            d = json.dumps(data_dum)
            return d, dcc.Location(id="redirect_to_db", pathname="/database-sucessful")
        else:
            d = json.dumps(data_dum)
            return d, "connection_failed"
    else:
        d = json.dumps(data_dum)
        return d, "nothing"
