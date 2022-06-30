from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
)

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SKETCHY, dbc_css],
    suppress_callback_exceptions=True,
)
load_figure_template("bootstrap")

# change name and emoji of dash app
app.title = "Visualizing database data"
pages_things = html.Div(
    [
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"]),
            hidden=True,
        )
        for page in dash.page_registry.values()
    ]
)
app.layout = html.Div(
    [
        pages_things,
        dcc.Store(id="store-data", storage_type="session"),
        dash.page_container,
    ],
    className="dbc",
)

if __name__ == "__main__":
    app.run_server(debug=True, threaded=True,host='0.0.0.0', port = 8080)
