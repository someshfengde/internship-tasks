import dash
from fsspec import Callback
import plotly.express as px
import pandas as pd
from data_prep import *

# setting up the data
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objs as go

# setting up the data
data = read_and_return_data()

# creatgin the local server
app = Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)


# grouping data  by Unique ClientMacAddress and averaging the other fields
data_grouped = data.groupby(["ClientMacAddress"]).mean()
data = data_grouped

# converting bit per second to megabyptes per second
data["RxRateBitrate"] = data["RxRateBitrate"] / 10000
data["TxRateBitrate"] = data["TxRateBitrate"] / 10000


app.layout = html.Div(
    [
        dcc.RadioItems(
            ["RxRateBitrate", "TxRateBitrate"],
            id="demo-dropdown",
            value="RxRateBitrate",
            inline=True,
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
            min=data["RxRateBitrate"].min(),
            max=data["RxRateBitrate"].max(),
            value=data["RxRateBitrate"].mean(),
            step=10,
        ),
        html.P("Dataframe"),
        dash_table.DataTable(
            data.to_dict("records"), [{"name": i, "id": i} for i in data.columns]
        ),
    ]
)


@app.callback(
    Output("template-x-graph", "figure"),
    [Input("demo-dropdown", "value"), Input("slider-input-to-graph", "value")],
)
def change_graph(value, slider_val):
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
    Output("percentage-indicator", "figure"), [Input("slider-input-to-graph", "value")]
)
def show_percentage_devices(slider_val):
    percentage_devices = len(data[data["RxRateBitrate"] > slider_val]) / len(data)
    # creating plotly pie chart for showing the percentage of devices
    fig = px.pie(
        values=[percentage_devices, 1 - percentage_devices],
        hole=0.4,
        names=["receiving high speed", "lower speed than threshhold"],
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
