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
        html.H1("Dashboards for ap_status_rfclients"),
        dcc.RadioItems(
            ["RxBitRate", "TxBitRate","Throughput"],
            id="demo-dropdown",
            value="RxBitRate",
            inline=True,
        ),
        html.H2("Select range to visualize data"),
        dcc.DatePickerRange(
            id="my-date-picker-range",
            min_date_allowed=date(2022, 6, 7),
            max_date_allowed=date(2022, 6, 16),
            initial_visible_month=date(2022, 6, 7),
            start_date=date(2022, 6, 7),
            end_date=date(2022, 6, 16),
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
        html.H1("Observed metric values"),
        html.Div(id="min-value"),
        html.Div(id="max-value"),
        html.Div(id="std-value"),
        html.Div(id="mean-value"),
        html.Div(id="median-value"),
    ]
)


@app.callback(
    [
        Output("template-x-graph", "figure"),
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
    ],
)
def change_graph(value, slider_val, start_date, end_date):
    command = f"select MacAddress,RxBitRate,TxBitRate,CheckinTime,Throughput,AssociatedFrequency from ap_status_rfclients WHERE CheckinTime BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59' "
    data = execute_command(
        command,
        ["MacAddress", "RxBitRate", "TxBitRate", "CheckinTime","Throughput","AssociatedFrequency"],
    )
    data = preprocess_data(data)

    print(f"{data['AssociatedFrequency'].value_counts()}")
    # # converting bit per second to megabyptes per second
    # data["RxBitRate"] = data["RxBitRate"] / 1000
    # data["TxBitRate"] = data["TxBitRate"] / 1000
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
    return (
        fig,
        f"minimum {value} is {data[value].min()}",
        f"maximum for {value} is{data[value].max()}",
        f"standard deviation in {value} is {data[value].std()}",
        f"mean for {value} is {data[value].mean()}",
        f"median for {value} is {data[value].median()}",
    )


@app.callback(
    Output("percentage-indicator", "figure"),
    [
        Input("demo-dropdown", "value"),
        Input("slider-input-to-graph", "value"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def show_percentage_devices(selected_val, slider_val, start_date, end_date):
    command = f"select MacAddress,RxBitRate,TxBitRate,CheckinTime from ap_status_rfclients WHERE CheckinTime BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59' "
    data = execute_command(
        command,
        ["MacAddress", "RxBitRate", "TxBitRate", "CheckinTime"],
    )
    data = preprocess_data(data)
    # converting bit per second to megabyptes per second
    # data["RxBitRate"] = data["RxBitRate"] / 1000
    # data["TxBitRate"] = data["TxBitRate"] / 1000
    percentage_devices = len(data[data[selected_val] > slider_val]) / len(data)
    # creating plotly pie chart for showing the percentage of devices
    fig = px.pie(
        values=[percentage_devices, 1 - percentage_devices],
        hole=0.4,
        names=["receiving high speed", "lower speed than threshhold"],
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)



