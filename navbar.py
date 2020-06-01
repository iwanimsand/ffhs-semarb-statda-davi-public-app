import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import psutil
from dash.dependencies import Output, Input, State

'''
For an example how tu use a Navbar with dash-bootstrap, see 
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
'''

items = dbc.Nav(
    [
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Version 1', href='trip-count'),
                dbc.DropdownMenuItem('Version 2', href='trip-count-v2'),
                dbc.DropdownMenuItem('Version 3', href='trip-count-v3'),
            ],
            nav=True,
            in_navbar=True,
            label='Nutzung Stationen',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Lage & Streuung', href='location-and-distribution'),
            ],
            nav=True,
            in_navbar=True,
            label='Deskriptive Analyse',
        ),
        dbc.NavItem(dbc.NavLink("Notebooks", href='notebooks'))
    ],
    navbar=True
)


def get_sysinfo():
    info = psutil.virtual_memory()

    return [
        html.Small(
            '{:.3f}GB Memory Used ({}%)'.format(info[3] / (1024 ** 3), info[2]),
            className='text-muted'
        ),
    ]


sysinfo = dbc.Row(
    [
        dbc.Col(get_sysinfo(), width='auto', id='live-sysinfo'),
        dcc.Interval(
            id='sysinfo-interval-component',
            interval=3 * 1000,  # in milliseconds
            n_intervals=0
        )
    ],
    align='center',
    no_gutters=True,
    className='ml-auto flex-nowrap mt-3 mt-md-0'
)

layout = dbc.Navbar(
    [
        dbc.NavLink(
            dbc.Row(
                [
                    dbc.Col(html.Img(src='/assets/onbicycle.svg', height='30px')),
                    dbc.Col(dbc.NavbarBrand('DaVi-Dash-App', className='ml-2'))
                ],
                align='center',
                no_gutters=True
            ),
            href='/',
        ),
        dbc.NavbarToggler(id='navbar-toggler'),
        dbc.Collapse([items, sysinfo], id='navbar-collapse', navbar=True),
    ],
)


def register_callbacks(app):
    # add callback for toggling the collapse on small screens
    @app.callback(
        Output('navbar-collapse', 'is_open'),
        [Input('navbar-toggler', 'n_clicks')],
        [State('navbar-collapse', 'is_open')],
    )
    def toggle_navbar_collapse(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

    @app.callback(Output('live-sysinfo', 'children'),
                  [Input('sysinfo-interval-component', 'n_intervals')])
    def update_graph_live(n):
        return get_sysinfo()
