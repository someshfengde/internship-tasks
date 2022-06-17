import dash
from fsspec import Callback
import plotly.express as px
import pandas as pd
from data_prep import *
from datetime import date
import matplotlib.pyplot as plt
# setting up the data
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objs as go


# creatgin the local server
app = Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)



app.layout = html.Div(
    [
        dcc.RadioItems(
            ["RxRateBitrate", "TxRateBitrate"],
            id="demo-dropdown",
            value="RxRateBitrate",
            inline=True,
        ),
        html.H2("Select range to visualize data"),
        dcc.DatePickerRange(
            id="my-date-picker-range",
            min_date_allowed=date(2021, 9, 4),
            max_date_allowed=date(2022, 6, 15),
            initial_visible_month=date(2021, 9, 4),
            start_date=date(2021, 9, 4),
            end_date=date(2021, 12, 15),
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="template-x-graph"),
                    ],
                    className="eight columns",
                ),
                # displaying dataframe in plotly
                html.Div(
                    dcc.Graph(id="percentage-indicator"), className="four columns"
                ),
            ],
        ),
        html.H2("Select the threshhold value"),
        dcc.Slider(
            id="slider-input-to-graph",
            min=0,
            max=90,
            value=10,
            step=10,
        ),
        html.P("Dataframe"),
    ]
)


@app.callback(
    Output("template-x-graph", "figure"),
    [
        Input("demo-dropdown", "value"),
        Input("slider-input-to-graph", "value"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def change_graph(value, slider_val, start_date, end_date):
    command = f"select ClientMacAddress,RxRateBitrate,TxRateBitrate,RxRateChWidth,TxRateChWidth,TimeStamp from uc_client_logs WHERE TimeStamp BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59' "
    data = execute_command(
        command,
        [
            "ClientMacAddress",
            "RxRateBitrate",
            "TxRateBitrate",
            "RxRateChWidth",
            "TxRateChWidth",
            "TimeStamp",
        ],
    )
    data = preprocess_data(data)
    # converting bit per second to megabyptes per second
    data["RxRateBitrate"] = data["RxRateBitrate"] / 1000
    data["TxRateBitrate"] = data["TxRateBitrate"] / 1000
    # converting bit per second to megabyptes per second
    bit_rate_data = data[value].to_numpy()
    fig = px.histogram(bit_rate_data, x=bit_rate_data)  # , nbins=50)
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
    return fig


@app.callback(
    Output("percentage-indicator", "figure"),
    [
        Input("slider-input-to-graph", "value"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def show_percentage_devices(slider_val, start_date, end_date):
    command = f"select ClientMacAddress,RxRateBitrate,TxRateBitrate,RxRateChWidth,TxRateChWidth,TimeStamp from uc_client_logs WHERE TimeStamp BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59' "
    data = execute_command(
        command,
        [
            "ClientMacAddress",
            "RxRateBitrate",
            "TxRateBitrate",
            "RxRateChWidth",
            "TxRateChWidth",
            "TimeStamp",
        ],
    )
    data = preprocess_data(data)
    # converting bit per second to megabyptes per second
    data["RxRateBitrate"] = data["RxRateBitrate"] / 1000
    data["TxRateBitrate"] = data["TxRateBitrate"] / 1000
    print(data["TxRateBitrate"].value_counts())
    percentage_devices = len(data[data["TxRateBitrate"] > slider_val]) / len(data)
    # creating plotly pie chart for showing the percentage of devices
    fig = px.pie(
        values=[percentage_devices, 1 - percentage_devices],
        hole=0.4,
        names=["receiving high speed", "lower speed than threshhold"],
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
