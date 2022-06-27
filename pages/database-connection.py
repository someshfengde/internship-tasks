import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import plotly.express as px
import pandas as pd
import json
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from data_prep import *
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

# setting up the data
import plotly.express as px
import plotly.graph_objs as go


dash.register_page(__name__, path="/database-sucessful", theme=dbc.themes.SKETCHY)


selection_card = dbc.Col(
    dbc.Card(
        [
            dbc.CardHeader("Database & Datatable selection"),
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4(
                                    "Select database from list", className="card-title"
                                ),
                                dcc.Dropdown(id="database-selection", className="p-4"),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.H4(
                                    "Select Datatable from list", className="card-title"
                                ),
                                dcc.Dropdown(id="datatable-selection", className="p-4"),
                            ]
                        ),
                    ]
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "visualize !",
                            color="primary",
                            className="mb-2 align-center",
                            id="command-vis",
                            n_clicks=0,
                        ),
                        className="d-grid gap-2 col-5 mx-auto",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Describe datatable",
                            color="primary",
                            className="mb-2",
                            id="command-describe",
                            n_clicks=0,
                        ),
                        className="d-grid gap-2 col-5 mx-auto",
                    ),
                ],
            ),
        ],
    ),
    className="w-90",
)


layout = html.Div(
    children=[
        dbc.Row(
            html.H1(
                id="dash_div",
                children="Analytics page",
                className=" text-black p-4 mb-2 text-left",
            )
        ),
        dbc.Row(
            selection_card,
        ),
        dbc.Row(id="vis-out"),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(
                        "Please select database and datatable values from above dropdown!"
                    )
                ),
                dbc.ModalBody(
                    "Visualizations are right there after you select database and datatable."
                ),
            ],
            id="modal-sm",
            size="sm",
            is_open=False,
        ),
        html.Div(
            id="desc-div",
            children=[
                dbc.Modal(id="desc-modal", children=[], is_open=False),
            ],
        ),
    ]
)

all_vis_data = [
    dbc.Row(
        [
            html.H1(id = "dashboard-main-title"),
            html.Br(),
            dcc.RadioItems(
                ["RxBitRate", "TxBitRate", "Throughput"],
                id="demo-dropdown",
                value="RxBitRate",
                inline=True,
            ),
            html.Br(),
        ]
    ),
    dbc.Row(
        [
            html.Br(),
            html.H2("Select range to visualize data"),
            dcc.DatePickerRange(
                id="my-date-picker-range",
                min_date_allowed=date(1999, 6, 7),
                max_date_allowed=date(2022, 6, 16),
                initial_visible_month=date(2022, 6, 7),
                start_date=date(2022, 6, 7),
                end_date=date(2022, 6, 16),
            ),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Graph(id="template-x-graph"),
                ],
                # className="four columns",
                width="8",
            ),
            # displaying dataframe in plotly
            dbc.Col(
                dcc.Graph(id="percentage-indicator"),
                # className="four columns"
                width="4",
            ),
        ],
    ),
    dbc.Row(
        [
            html.H2("Select the threshhold value"),
            dcc.Slider(
                id="slider-input-to-graph",
                min=0,
                max=1000,
                value=10,
                step=10,
            ),
        ]
    ),
    dbc.Row(
        [
            html.H1("Observed metric values"),
            html.Div(id="min-value"),
            html.Div(id="max-value"),
            html.Div(id="std-value"),
            html.Div(id="mean-value"),
            html.Div(id="median-value"),
        ]
    ),
]


# main dashboard

@callback([
    Output("dashboard-main-title", "children"), 
    Input("datatable-selection", "value"),
])
def change_title(value):
    """
    Inupt:
        datatable-selection value.
    Output:
        Changes the title of the dashboard
    """
    return [f"dashboard for {value}"]



@callback(
    [
        Output("template-x-graph", "figure"),
        Output("percentage-indicator", "figure"),
        Output("min-value", "children"),
        Output("max-value", "children"),
        Output("std-value", "children"),
        Output("mean-value", "children"),
        Output("median-value", "children"),
    ],
    [
        Input("demo-dropdown", "value"),
        Input("slider-input-to-graph", "value"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
        Input("database-selection", "value"),
        Input("datatable-selection", "value"), 
        Input("store-data", "data")
    ],
)
def change_graph(value, slider_val, start_date, end_date,db , dt,  creds):
    command = f"select MacAddress,RxBitRate,TxBitRate,Throughput,CheckinTime from {db}.{dt} WHERE CheckinTime BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59' "
    creds = json.loads(creds)
    sql_obj, connected = connect_to_db(
        username=creds["username"], password=creds["password"]
    )
    data = execute_command(
        command,
        sql_obj,
        ["MacAddress", "RxBitRate", "TxBitRate","Throughput","CheckinTime"],
    )
    data = preprocess_data(data)
    value_counts_df = pd.DataFrame(data[value].value_counts())
    color_col = []
    for x in data[value]:
        if int(x) < data[value].max() * 0.10:
            color_col.append("red")
        elif int(x) < data[value].max() * 0.50:
            color_col.append("yellow")
        else:
            color_col.append("green")
    data["color"] = color_col
    print(data.head())
    fig = px.bar(data , x = data[value].value_counts().keys(), y = value, color = "color" )  # , nbins=50)
    fig.update_layout(
        title_text=value,
        xaxis_title=f"{value}",  # x-axis label
        yaxis_title="Frequency",  # y-axis label
    )
    fig.add_vline(
        x=slider_val,
        line_color="red",
        line_width=2,
        line_dash="dash",
        name="slider_val",
    )
    percentage_devices = len(data[data[value] > slider_val]) / len(data)
    # creating plotly pie chart for showing the percentage of devices
    pie_fig = px.pie(
        values=[percentage_devices, 1 - percentage_devices],
        hole=0.4,
        names=["receiving high speed", "lower speed than threshhold"],
    )
    return (
        fig,
        pie_fig,
        f"minimum {value} is {data[value].min()}",
        f"maximum for {value} is{data[value].max()}",
        f"standard deviation in {value} is {data[value].std()}",
        f"mean for {value} is {data[value].mean()}",
        f"median for {value} is {data[value].median()}",
    )



# database and datatable selection dropdown
@callback(
    Output("database-selection", "options"),
    [Input("store-data", "data")],
)
def update_output(data):
    x = json.loads(data)
    sql_obj, connected = connect_to_db(username=x["username"], password=x["password"])
    curs = sql_obj.cursor()
    curs.execute("show databases")
    data = curs.fetchall()
    curs.close()
    sql_obj.close()
    databases_avail = [x[0] for x in data]
    return databases_avail


@callback(
    Output("datatable-selection", "options"),
    [Input("database-selection", "value"), Input("store-data", "data")],
)
def show_datatables(selected_opt, creds):
    creds = json.loads(creds)
    sql_obj, connected = connect_to_db(
        username=creds["username"], password=creds["password"], database=selected_opt
    )
    curs = sql_obj.cursor()
    curs.execute(f"use {selected_opt}")
    curs.execute("show tables")
    data = curs.fetchall()
    curs.close()
    sql_obj.close()
    tables_avail = [x[0] for x in data]
    return tables_avail


# utils functions (Modal and hidden functionality)
@callback(
    [Output("modal-sm", "is_open"), Output("vis-out", "children")],
    [
        Input("command-vis", "n_clicks"),
        Input("datatable-selection", "value"),
        Input("database-selection", "value"),
        State("modal-sm", "is_open"),
    ],
)
def show_modal(is_clicked, selected_database, selected_table, modal_ip):
    """
    This function is used to show the modal for the command visualization.

    """
    if is_clicked and (selected_database == None or selected_table == None):
        modal_ip = not modal_ip
        return modal_ip, ""
    elif is_clicked and (selected_database != None and selected_table != None):
        return modal_ip, all_vis_data


# callback for showing modal with datatable description
@callback(
    [
        Output("desc-modal", "children"),
        Output("desc-modal", "size"),
        Output("desc-modal", "is_open"),
    ],
    [
        Input("command-describe", "n_clicks"),
        State("desc-modal", "is_open"),
        Input("datatable-selection", "value"),
        Input("database-selection", "value"),
        Input("store-data", "data"),
    ],
)
def show_modal_content(is_clicked, modal_ip, datatable, database, creds):
    """
    Inputs:
        is_clicked: if the button for desc_datatable is clicked
        modal_ip: if the modal is already open or not
        database: selected database ( should not be equal to None for querying the database)
        datatable: selected datatable ( should not be equal to None for querying the datatable)
        creds: credentials for the database.
    Outputs:
        Shows modal with the proper description of the datatable.
    """
    if is_clicked and (database != None and datatable != None):
        # loading the credentials
        creds = json.loads(creds)
        sql_obj, connected = connect_to_db(
            username=creds["username"], password=creds["password"]
        )  # setting up connection to the database
        curs = sql_obj.cursor()  # getting cursor
        curs.execute(f"use {database}")  # switching to selected database
        curs.execute(f"desc {datatable}")  # executing query for collecting the data
        data = curs.fetchall()  # fetching the output generated
        data = pd.DataFrame(
            data, columns=["Field", "Type", "Null", "Key", "Default", "Extra"]
        )
        curs.close()
        sql_obj.close()  # closing the connections

        # creating the table for the description
        table = dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i, "deletable": True} for i in data.columns],
            data=data.to_dict("records"),
            page_size=10,
            editable=True,
            cell_selectable=True,
            filter_action="native",
            sort_action="native",
            style_table={"overflowX": "auto"},
        )
        children_components = [
            dbc.ModalHeader(dbc.ModalTitle("DataTable Description")),
            dbc.ModalBody(dbc.Row(table)),
        ]
        size = "xl"
        toggle_modal = not modal_ip
        return children_components, size, toggle_modal

    elif is_clicked and (database == None or datatable == None):
        children_components = [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    "You are trying to visualize datatable without selecting it first!!"
                )
            ),
            dcc.Markdown("Please select the `Database` and `DataTable` first"),
        ]
        size = "md"
        toggle_modal = not modal_ip
        return children_components, size, toggle_modal

