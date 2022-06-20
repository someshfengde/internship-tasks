from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
)

app = Dash(
    __name__, use_pages=True, external_stylesheets=[dbc.themes.SKETCHY, dbc_css]
)
# change name and emoji of dash app
app.title = "Visualizing database data"

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                , hidden= True
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
