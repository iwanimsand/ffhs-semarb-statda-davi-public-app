import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Output, Input

from data import read_df_month

# Prefix for IDs: tc

df_month = read_df_month()

i18n = {
    '0': 'Unbekannt',
    '1': 'männlich',
    '2': 'weiblich',
    'Customer': '24h- oder 3-Tagespass',
    'Subscriber': 'Jahresmitglied'
}


def get_start_count_month(data):
    df_start_count_month = pd.pivot_table(
        data,
        index=['Start Station Name', 'Start Station Latitude', 'Start Station Longitude'],
        values=['Trip Duration'],
        aggfunc='count'
    )

    df_start_count_month = df_start_count_month.reset_index().rename(columns={
        'Start Station Name': 'Name',
        'Start Station Latitude': 'Latitude',
        'Start Station Longitude': 'Longitude',
        'Trip Duration': 'Trip Count'
    })

    return df_start_count_month


def filter_data(user_types, genders):
    df_filtered = df_month
    if user_types is not None and len(user_types) > 0:
        df_filtered = df_filtered[df_filtered['User Type'].isin(user_types)]
    if genders is not None and len(genders) > 0:
        df_filtered = df_filtered[df_filtered['Gender'].isin(genders)]
    return df_filtered


def get_trip_stats(data):
    total = get_start_count_month(df_month)['Trip Count'].sum()
    actual_showing = data['Trip Count'].sum()
    stats = '''
        Gesamt: **{:,d}**  
        Aktuell angezeigt: **{:,d}**
        '''.format(total, actual_showing)
    return stats


def get_station_stats(data):
    total = get_start_count_month(df_month)['Trip Count'].count()
    actual_showing = data['Trip Count'].count()
    stats = '''
        Gesamt: **{:,d}**  
        Aktuell angezeigt: **{:,d}**
        '''.format(total, actual_showing)
    return stats


def create_sidepanel():
    sidepanel = html.Div(
        [
            html.H4(['Nutzung Stationen', html.Small(' (Version 1)', className='text-muted')]),
            dcc.Markdown('_Datengrundlage_: **5000 zufällige Stichproben aus dem Monat Oktober 2019**'),
            dcc.Markdown('''
            In der Karte werden die Stationen in Form eines Kreises angezeigt.
            
            * Die Fläche des Kreises zeigt dabei an wie viele Fahrten von dieser Station aus gestartet wurden.
            * Die Farbe des Kreises zeigt an wie viele Fahrten von dieser Station aus gestartet wurden. Anhand des
            Farbbalkens rechts neben der Karte, kann die ungefähre Anzahl Fahrten abgelesen werden.
            
            Fährt man mit der Maus über die Sation, erscheint der Stationsname.
            
            Mit Hilfe der unten verfügbaren Filter, lassen sich bestimmte Merkmale filtern.
            '''),
            dbc.Card(
                [
                    dbc.CardHeader('Filterauswahl'),
                    dbc.CardBody(
                        [
                            html.H5('Benutzerart', className='card-title'),
                            dcc.Dropdown(
                                id='tc-dropdown-user-type',
                                options=[
                                    dict(label=i18n['Subscriber'], value='Subscriber'),
                                    dict(label=i18n['Customer'], value='Customer')
                                ],
                                multi=True,
                                className='mb-3'
                            ),
                            html.H5('Geschlecht', className='card-title'),
                            dcc.Dropdown(
                                id='tc-dropdown-gender',
                                options=[
                                    dict(label=i18n['0'], value='0'),
                                    dict(label=i18n['1'], value='1'),
                                    dict(label=i18n['2'], value='2')
                                ],
                                multi=True
                            ),
                        ]
                    )
                ],
                className='mb-3'
            ),
        ]
    )

    return sidepanel


def create_figure(data):
    """
    Creates a scatter mapbox figure.
    :param data:
    :return: The created figure.
    """
    fig_go = go.Figure()

    scattermapbox = go.Scattermapbox(
        lat=data['Latitude'], lon=data['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=data['Trip Count'],
            color=data['Trip Count'],
            opacity=0.7,
            showscale=True,
            sizemode='area',
            sizeref=data['Trip Count'].max() / 50 ** 2,
            colorbar=dict(
                title='Anzahl Fahrten',
                tickformat='.%2f'
            )
        ),
        text=data['Name'],
        hoverinfo='text',
    )

    _ = fig_go.add_trace(scattermapbox)

    center_lat = (data['Latitude'].max() - data['Latitude'].min()) / 2 + data['Latitude'].min()
    center_lon = (data['Longitude'].max() - data['Longitude'].min()) / 2 + data['Longitude'].min()

    _ = fig_go.update_layout(
        margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
        mapbox=dict(
            style='open-street-map',
            center=dict(
                lat=center_lat,
                lon=center_lon
            ),
            pitch=0,
            zoom=12
        ),
        width=1200, height=1600
    )

    return fig_go


layout = dbc.Row(
    [
        dbc.Col(
            [
                html.Div(create_sidepanel()),
                html.Div(
                    [
                        html.Div(id='tc-scattermapbox-fig-output'),
                        html.Div(id='tc-scattermapbox-fig-selected-output'),
                        html.Div(id='tc-scattermapbox-fig-hover-output'),
                    ],
                    hidden=True
                ),
                html.Div(
                    [
                        html.Div(id='tc-dropdown-user-type-output'),
                        html.Div(id='tc-dropdown-gender-output'),
                    ]
                )

            ],
            md=4
        ),
        dbc.Col(
            [
                html.Div(
                    dcc.Graph(
                        id='tc-scattermapbox-fig',
                        figure=create_figure(get_start_count_month(df_month)),
                        style={'width': '100%', 'height': '80vh', 'margin': "auto", "display": "block"},
                        responsive=True
                    )
                ),
            ],
            md=8
        ),
    ]
)


def register_callbacks(app):
    @app.callback(
        Output('tc-scattermapbox-fig-output', 'children'),
        [Input('tc-scattermapbox-fig', 'clickData')]
    )
    def callback_scattermapbox_fig(click_data):
        return 'click_data: {}'.format(click_data)

    @app.callback(
        Output('tc-scattermapbox-fig-selected-output', 'children'),
        [Input('tc-scattermapbox-fig', 'selectedData')]
    )
    def callback_scattermapbox_fig(selected_data):
        return 'selected-data: {}'.format(selected_data)

    @app.callback(
        Output('tc-scattermapbox-fig-hover-output', 'children'),
        [Input('tc-scattermapbox-fig', 'hoverData')]
    )
    def callback_scattermapbox_fig_hover(hover_data):
        return 'hover_data: {}'.format(hover_data)

    @app.callback(
        Output('tc-scattermapbox-fig', 'figure'),
        [Input('tc-dropdown-user-type', 'value'),
         Input('tc-dropdown-gender', 'value')]
    )
    def callback_filter(user_type_value, gender_value):
        filtered_data = filter_data(user_type_value, gender_value)
        data = get_start_count_month(filtered_data)
        fig = create_figure(data)

        return fig
