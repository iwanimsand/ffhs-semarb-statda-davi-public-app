import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

from data import read_df_month

power_button_on_color = plotly.colors.qualitative.Plotly[2]

df_month = read_df_month()

column_excludes = [
    'timezone',
    'lat',
    'lon',
]

numeric_columns = []
for col in df_month.columns:
    if (col not in column_excludes and (
            df_month[col].dtype == np.float64
            or df_month[col].dtype == np.int64
            or isinstance(df_month[col].dtype, pd.Int64Dtype))):
        numeric_columns.append(col)


def get_histogram_options(disabled):
    return [
        dict(id='', label='Y-Achse logarithmisch', value='log', disabled=disabled),
    ]


def get_boxplot_options(disabled):
    return [
        dict(label='Durchschnitt anzeigen', value='mean', disabled=disabled)
    ]


def create_histogram_options():
    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        daq.PowerButton(
                            id='histogram-on',
                            on=True,
                            color=power_button_on_color
                        ),
                    ],
                    className='mb-3',
                    md=3
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Checklist(
                                    options=get_histogram_options(False),
                                    value=[],
                                    id='histogram-options',
                                    inline=False,
                                    switch=True
                                )
                            ]
                        )
                    ],
                    md=8
                )
            ]
        )
    ]


def create_boxplot_options():
    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        daq.PowerButton(
                            id='boxplot-on',
                            on=False,
                            color=power_button_on_color
                        ),
                    ],
                    className='mb-3',
                    md=3
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Checklist(
                                    options=get_boxplot_options(True),
                                    value=[],
                                    id='boxplot-options',
                                    inline=False,
                                    switch=True
                                )
                            ]
                        )
                    ],
                    md=8
                )
            ]
        )
    ]


def get_feature_option(disabled):
    return [{'label': val, 'value': val, 'disabled': disabled} for val in numeric_columns]


def create_checklist_features():
    return dbc.FormGroup(
        [
            dbc.Checklist(
                options=get_feature_option(False),
                value=[],
                switch=True,
                id='checklist-features-input'
            )
        ]
    )


def create_sidepanel():
    sidepanel = html.Div(
        [
            html.H2('Histogramm und Boxplot'),
            dcc.Markdown('_Datengrundlage_: **5000 zufällige Stichproben aus dem Monat Oktober 2019**'),
            dcc.Markdown('''
            Darstellung von Boxplots und Histogrammen für die verschiedenen Merkmale.
            '''),
            dbc.Card(
                [
                    dbc.CardHeader('Histogramm'),
                    dbc.CardBody(
                        create_histogram_options()
                    )
                ],
                className='mb-3'
            ),
            dbc.Card(
                [
                    dbc.CardHeader('Boxplot'),
                    dbc.CardBody(
                        create_boxplot_options()
                    )
                ],
                className='mb-3'
            ),
            dbc.Card(
                [
                    dbc.CardHeader('Merkmale'),
                    dbc.CardBody(
                        create_checklist_features()
                    )
                ],
                className='mb-3'
            ),
        ]
    )

    return sidepanel


def create_figure(data, column, hist_show, hist_yaxis_log, box_show, box_mean):
    n_rows = (1 if hist_show else 0) + (1 if box_show else 0)

    fig = make_subplots(
        rows=n_rows, cols=1,
        shared_xaxes=True,
        print_grid=False,
        vertical_spacing=0.05,
        y_title=column,
        row_heights=[0.5, 1] if hist_show and box_show else [1]
    )

    if box_show:
        boxplot = go.Box(
            name='',
            x=data[column],
            boxmean=box_mean
        )
        _ = fig.add_trace(boxplot, 1, 1)

    if hist_show:
        hist_row_number = (2 if box_show else 1)
        histogram = go.Histogram(
            name='',
            x=data[column]
        )
        _ = fig.add_trace(histogram, hist_row_number, 1)

        fig.update_yaxes(
            type='log' if hist_yaxis_log else 'linear',
            row=hist_row_number
        )

    fig.update_layout(
        showlegend=False,
        margin={'r': 30, 't': 30, 'l': 60, 'b': 30},
    )

    return fig


def create_box_hist_graphs(data, columns, hist_show, hist_yaxis_log, box_show, box_mean):
    if len(columns) == 0:
        return None

    dbc_cols = []
    for idx, col in enumerate(columns):
        dbc_col = dbc.Col(
            [
                dcc.Graph(figure=create_figure(data,
                                               column=col,
                                               hist_show=hist_show,
                                               hist_yaxis_log=hist_yaxis_log,
                                               box_show=box_show,
                                               box_mean=box_mean))
            ],
            className='mb-3'
        )
        dbc_cols.append(dbc_col)

    return dbc_cols


layout = dbc.Row(
    [
        dbc.Col(
            [
                create_sidepanel()
            ],
            md=4
        ),
        dbc.Col(
            id='box-hist-graphs',
            md=8
        ),
    ]
)


def register_callbacks(app):
    @app.callback(
        [Output('box-hist-graphs', 'children'),
         Output('histogram-options', 'options'),
         Output('boxplot-options', 'options'),
         Output('checklist-features-input', 'options')],
        [Input('checklist-features-input', 'value'),
         Input('histogram-on', 'on'),
         Input('boxplot-on', 'on'),
         Input('histogram-options', 'value'),
         Input('boxplot-options', 'value')]
    )
    def callback_change_histogram(checklist_features_value,
                                  histogram_on, boxplot_on,
                                  histogram_options_values,
                                  boxplot_options_values):
        if histogram_on is False and boxplot_on is False:
            return None, get_histogram_options(True), get_boxplot_options(True), get_feature_option(True)

        graphs = create_box_hist_graphs(
            df_month,
            columns=checklist_features_value,
            hist_show=histogram_on,
            hist_yaxis_log='log' in histogram_options_values,
            box_show=boxplot_on,
            box_mean='mean' in boxplot_options_values
        )

        return graphs, get_histogram_options(histogram_on is False), get_boxplot_options(
            boxplot_on is False), get_feature_option(histogram_on is False and boxplot_on is False)
