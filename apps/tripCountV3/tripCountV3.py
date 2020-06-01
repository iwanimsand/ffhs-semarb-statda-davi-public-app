import typing

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Output, Input

from data import read_df_month

# Prefix for IDs: tc3

df_month = read_df_month()

center_lat = (df_month['Start Station Latitude'].max() - df_month['Start Station Latitude'].min()) / 2 + df_month[
    'Start Station Latitude'].min()
center_lon = (df_month['Start Station Longitude'].max() - df_month['Start Station Longitude'].min()) / 2 + df_month[
    'Start Station Longitude'].min()

i18n = {
    '0': 'Unbekannt',
    '1': 'männlich',
    '2': 'weiblich',
    'Customer': '24h- oder 3-Tagespass',
    'Subscriber': 'Jahresmitglied'
}

colormap = {
    'Subscriber': px.colors.sequential.OrRd[5],
    'Customer': px.colors.sequential.OrRd[3],
    '0': px.colors.sequential.Plotly3[4],
    '1': px.colors.sequential.Plotly3[2],
    '2': px.colors.sequential.Plotly3[10],
    'Subscriber-0': px.colors.sequential.OrRd[5],
    'Subscriber-1': px.colors.sequential.Plotly3[0],
    'Subscriber-2': px.colors.sequential.Plotly3[8],
    'Customer-0': px.colors.sequential.OrRd[3],
    'Customer-1': px.colors.sequential.Plotly3[2],
    'Customer-2': px.colors.sequential.Plotly3[10],
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


def filter_data(data, user_types, genders):
    df_result = []

    if user_types is not None and len(user_types) > 0:
        for user_type in user_types:
            if genders is not None and len(genders) > 0:
                for gender in genders:
                    df_filtered = data[(data['User Type'] == user_type) & (data['Gender'] == gender)]
                    df_result.append(
                        (
                            '{}-{}'.format(user_type, gender),
                            '{} & {}'.format(i18n[user_type], i18n[gender]),
                            df_filtered
                        )
                    )
            else:
                df_filtered = data[data['User Type'] == user_type]
                df_result.append(
                    (
                        '{}'.format(user_type),
                        '{}'.format(i18n[user_type]),
                        df_filtered
                    )
                )
    else:
        if genders is not None and len(genders) > 0:
            for gender in genders:
                df_filtered = data[data['Gender'] == gender]
                df_result.append(
                    (
                        '{}'.format(gender),
                        '{}'.format(i18n[gender]),
                        df_filtered
                    )
                )

    return df_result


def get_trip_stats(data):
    total = get_start_count_month(df_month)['Trip Count'].sum()
    if isinstance(data, typing.List):
        # filtered statistics, show numbers of each filter
        stats = 'Gesamt: **{:,d}**  \n'.format(total)
        for data_entry in data:
            trip_sum = get_start_count_month(data_entry[2])['Trip Count'].sum()
            stats = stats + data_entry[1] + ': **{:,d}**  \n'.format(trip_sum) + '  '
        return stats
    else:
        # no filter active, normal dataset given
        actual_showing = data['Trip Count'].sum()
        stats = '''
            Gesamt: **{:,d}**  
            Aktuell angezeigt: **{:,d}**
            '''.format(total, actual_showing)
        return stats


def get_station_stats(data):
    total = get_start_count_month(df_month)['Trip Count'].count()
    if isinstance(data, typing.List):
        # filtered statistics, show numbers of each filter
        stats = 'Gesamt: **{:,d}**  \n'.format(total)
        for data_entry in data:
            station_count = get_start_count_month(data_entry[2])['Trip Count'].count()
            stats = stats + data_entry[1] + ': **{:,d}**  \n'.format(station_count) + '  '
        return stats
    else:
        # no filter active, normal dataset given
        actual_showing = data['Trip Count'].count()
        stats = '''
            Gesamt: **{:,d}**  
            Aktuell angezeigt: **{:,d}**
            '''.format(total, actual_showing)
        return stats


def create_sidepanel():
    sidepanel = html.Div(
        [
            html.H4(['Nutzung Stationen', html.Small(' (Version 3)', className='text-muted')]),
            dcc.Markdown('_Datengrundlage_: **5000 zufällige Stichproben aus dem Monat Oktober 2019**'),
            dcc.Markdown('''
            **Fehler Version 2**
            
            * Wenn in der Version 2 nur das Geschlecht verglichen wird, so wird der Anschein erweckt, dass die Frauen
            mehr fahren als die Männer. Schaut man sich dann aber die Zahlen an, widersprechen diese dem visuellen
            Eindruck. Grund dafür ist die Berechnung der maximalen Kreisfläche. Diese wurde in Version 2 für jeden gefilterten
            Datensatz isoliert berechnet. Somit bekam ein Datensatz mit einem kleinen maximalen Wert die gleiche maximale
            Kreisfläche zugeteilt, wie ein Datensatz mit einem grossen maximalen Wert.
            * Die Symbole in der Legende werden sehr klein und die Farbe ist dadurch nur noch schwer erkennbar.
            
            **Verbesserungen in Version 3**
            
            * Der Bug wurde behoben und bei der Berechnung der maximalen Kreisfläche wird das maximum über alle Datensätze
            ermittelt.
            * Die Grösse des Symbols in der Legende wurde auf ```constant``` gesetzt, dadurch ist es egal wie klein/gross 
            die Kreise auf der Karte sind, das Symbol in der Legende wird immer gleich gross angezeigt.
            
            **Nächste Optimierungen**
            
            * Die Farbwahl für bestimmte Vergleiche ist unglücklich gewählt und sollte verbessert werden 
            (z.B. ```Jahresmitglied & männlich``` vs ```24h- oder 3-Tagespass & männlich```).
            * Fährt man mit der Maus über eine Station, sollten zusätzlich noch die Anzahl Fahrten angezeigt werden.
            '''),
            dbc.Card(
                [
                    dbc.CardHeader('Filterauswahl'),
                    dbc.CardBody(
                        [
                            html.H5('Benutzerart', className='card-title'),
                            dcc.Dropdown(
                                id='tc3-dropdown-user-type',
                                options=[
                                    dict(label=i18n['Subscriber'], value='Subscriber'),
                                    dict(label=i18n['Customer'], value='Customer')
                                ],
                                multi=True,
                                className='mb-3'
                            ),
                            html.H5('Geschlecht', className='card-title'),
                            dcc.Dropdown(
                                id='tc3-dropdown-gender',
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

            dbc.Card(
                [
                    dbc.CardHeader('In Zahlen'),
                    dbc.CardBody(
                        [
                            html.H5('Fahrten', className='card-title'),
                            dcc.Markdown(get_trip_stats(get_start_count_month(df_month)),
                                         id='tc3-numbers-trip-stats-output'),
                            html.Hr(),
                            html.H5('Stationen', className='card-title'),
                            dcc.Markdown(get_station_stats(get_start_count_month(df_month)),
                                         id='tc3-numbers-station-stats-output'),
                        ]
                    )
                ],
                className='mb-3'
            )

        ]
    )

    return sidepanel


def create_scattermapbox(data):
    figure = go.Figure()

    data_plot = get_start_count_month(data)

    scattermapbox = go.Scattermapbox(
        lat=data_plot['Latitude'], lon=data_plot['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=data_plot['Trip Count'],
            color=data_plot['Trip Count'],
            opacity=0.7,
            showscale=True,
            sizemode='area',
            sizeref=data_plot['Trip Count'].max() / 50 ** 2,
            colorbar=dict(
                title='Anzahl Fahrten',
                tickformat='.%2f'
            )
        ),
        text=data_plot['Name'],
        hoverinfo='text',
    )

    _ = figure.add_trace(scattermapbox)

    _ = figure.update_layout(
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
        width=1200, height=1600,
        legend=dict(
            itemsizing='constant',
        )
    )

    return figure


def create_scattermapbox_filtered(list_data):
    figure = go.Figure()

    data = {}
    max_trip_count = 0
    for data_tuple in list_data:
        data[data_tuple[1]] = get_start_count_month(data_tuple[2])
        actual_max_trip_count = data[data_tuple[1]]['Trip Count'].max()
        if actual_max_trip_count > max_trip_count:
            max_trip_count = actual_max_trip_count

    for data_tuple in list_data:
        data_plot = data[data_tuple[1]]
        scattermapbox = go.Scattermapbox(
            lat=data_plot['Latitude'], lon=data_plot['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=data_plot['Trip Count'],
                opacity=0.7,
                sizemode='area',
                sizeref=max_trip_count / 50 ** 2,
                color=colormap[data_tuple[0]]
            ),
            text=data_plot['Name'],
            hoverinfo='text',
            showlegend=True,
            name=data_tuple[1],
        )

        _ = figure.add_trace(scattermapbox)

    _ = figure.update_layout(
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
        width=1200, height=1600,
        legend=dict(
            itemsizing='constant',
        )
    )

    return figure


layout = dbc.Row(
    [
        dbc.Col(
            [
                html.Div(create_sidepanel()),
                html.Div(
                    [
                        html.Div(id='tc3-scattermapbox-fig-output'),
                        html.Div(id='tc3-scattermapbox-fig-selected-output'),
                        html.Div(id='tc3-scattermapbox-fig-hover-output'),
                    ],
                    hidden=True
                ),

                html.Div(
                    [
                        html.Div(id='tc3-dropdown-user-type-output'),
                        html.Div(id='tc3-dropdown-gender-output'),
                    ]
                )

            ],
            md=4
        ),
        dbc.Col(
            [
                html.Div(
                    dcc.Graph(
                        id='tc3-scattermapbox-fig',
                        figure=create_scattermapbox(df_month),
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
        Output('tc3-scattermapbox-fig-output', 'children'),
        [Input('tc3-scattermapbox-fig', 'clickData')]
    )
    def callback_scattermapbox_fig(click_data):
        return 'click_data: {}'.format(click_data)

    @app.callback(
        Output('tc3-scattermapbox-fig-selected-output', 'children'),
        [Input('tc3-scattermapbox-fig', 'selectedData')]
    )
    def callback_scattermapbox_fig(selected_data):
        return 'selected-data: {}'.format(selected_data)

    @app.callback(
        Output('tc3-scattermapbox-fig-hover-output', 'children'),
        [Input('tc3-scattermapbox-fig', 'hoverData')]
    )
    def callback_scattermapbox_fig_hover(hover_data):
        return 'hover_data: {}'.format(hover_data)

    @app.callback(
        [Output('tc3-scattermapbox-fig', 'figure'),
         Output('tc3-numbers-station-stats-output', 'children'),
         Output('tc3-numbers-trip-stats-output', 'children')],
        [Input('tc3-dropdown-user-type', 'value'),
         Input('tc3-dropdown-gender', 'value')]
    )
    def callback_filter(user_type_value, gender_value):
        if (user_type_value is None or len(user_type_value) == 0) and (gender_value is None or len(gender_value) == 0):
            fig = create_scattermapbox(df_month)
            trip_stats = get_trip_stats(get_start_count_month(df_month))
            station_stats = get_station_stats(get_start_count_month(df_month))
            return fig, station_stats, trip_stats
        else:
            filtered_data = filter_data(df_month, user_type_value, gender_value)
            fig = create_scattermapbox_filtered(filtered_data)

            station_stats = get_station_stats(filtered_data)
            trip_stats = get_trip_stats(filtered_data)

            return fig, station_stats, trip_stats
