import dash 
import plotly.express as px 
import pandas as pd
from data_prep import * 
# setting up the data 
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

# setting up the data
data = read_and_return_data()
bit_rate_data = data["RxRateBitrate"].value_counts()
fig  = px.hist(x = bit_rate_data.keys(), y = bit_rate_data.values, title = "Bitrate")
print(bit_rate_data)
# creatgin the local server 
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="template-x-graph", figure=fig),
    html.P("Title"),
    #displaying dataframe in plotly 
    html.P("Dataframe"),
    dash_table.DataTable(data.to_dict('records'), [{"name": i, "id": i} for i in data.columns])
    
])



if __name__ == "__main__":
    app.run_server(debug=True)