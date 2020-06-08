import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
from dash.dependencies import Output, Input

import navbar
from apps import index
from apps.locationDistribution import locationDistribution
from apps.notebooks import notebooks
from apps.tripCount import tripCount
from apps.tripCountV2 import tripCountV2
from apps.tripCountV3 import tripCountV3

server = flask.Flask(__name__)
app = dash.Dash(prevent_initial_callbacks=True,
                suppress_callback_exceptions=False,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                server=server,
                meta_tags=[
                    {'http-equiv': 'Cache-Control', 'content': 'max-age=0'},
                    {'http-equiv': 'Cache-Control', 'content': 'no-cache'},
                    {'http-equiv': 'expires', 'content': '0'},
                    {'http-equiv': 'expires', 'content': 'Tue, 01 Jan 1980 1:00:00 GMT'},
                    {'http-equiv': 'pragma', 'content': 'no-cache'}
                ])

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        navbar.layout,
        dbc.Container(
            id='page-content',
            className='p-5',
            fluid=True
        )
    ]
)

# "complete" layout for validation when app is starting
app.validation_layout = html.Div([
    app.layout,
    navbar.layout,
    index.layout,
    tripCount.layout,
    tripCountV2.layout,
    tripCountV3.layout,
    locationDistribution.layout,
    notebooks.layout
])


# routing for the different apps
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/home':
        return index.layout
    elif pathname == '/trip-count':
        return tripCount.layout
    elif pathname == '/trip-count-v2':
        return tripCountV2.layout
    elif pathname == '/trip-count-v3':
        return tripCountV3.layout
    elif pathname == '/location-and-distribution':
        return locationDistribution.layout
    elif pathname == '/notebooks':
        return notebooks.layout
    else:
        return '404'


navbar.register_callbacks(app)
tripCount.register_callbacks(app)
tripCountV2.register_callbacks(app)
tripCountV3.register_callbacks(app)
locationDistribution.register_callbacks(app)
notebooks.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False, port=5030)
