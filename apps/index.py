import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

layout = dbc.Jumbotron(
    [
        html.H1('Willkommen auf der DaVi-Dash-App', className='display-3 text-center'),
        dcc.Markdown(
            '''
            Im Rahmen des Kurses Datenvisualisierung (DaVi) des DAS Data Science an der FFHS Fernfachhochschule Schweiz,
            wurde eine Dash Applikation für die Semesterarbeit erstellt.
            ''',
            className='text-center'
        ),
        html.Hr(className="my-2"),
        html.H2('Applikationsteile', className='mb-3 text-center'),
        dcc.Markdown(
            '''
            Aktuell besteht die Applikation aus 3 Teilen die unten näher beschrieben werden. Diese sind über die
            Navigation ganz oben erreichbar.
            ''',
            className='text-center'
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4('Nutzung Stationen', className='card-title'),
                                    dcc.Markdown(
                                        '''
                                        Hier wurde versucht, die Visualisierung der Fragestellung _Welche Stationen werden am meisten
                                        genutzt?_ umzusetzen. Es gibt mehrere Versionen die aufgerufen werden können. Was in jeder
                                        Version enthalten ist und was in einer höheren Version verbessert wurde, wird in jeder Version
                                        auf der linken Seite beschrieben.
                                        '''
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Button(
                                                    "Version 1", color="primary", className="mt-auto",
                                                    href='/trip-count'
                                                ),
                                                className='text-center'
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "Version 2", color="primary", className="mt-auto",
                                                    href='/trip-count-v2'
                                                ),
                                                className='text-center'
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "Version 3", color="primary", className="mt-auto",
                                                    href='/trip-count-v3'
                                                ),
                                                className='text-center'
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4('Deskriptive Analyse', className='card-title'),
                                    dcc.Markdown(
                                        '''
                                        Es wurden verschiedene Komponenten von Dash ausprobiert. Entstanden ist dabei der Applikationsteil 
                                        _Deskriptive Analyse_. Aktuell gibt es nur die Möglichkeit, unter _Lage & Streuung_ Histogramme und Boxplots
                                        darzustellen. So sollen Merkmale schnell analysiert werden können.
                                        '''
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Button(
                                                    "Lage & Streuung", color="success", className="mt-auto",
                                                    href='/location-and-distribution'
                                                ),
                                                className='text-center'
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4('Notebooks', className='card-title'),
                                    dcc.Markdown(
                                        '''
                                        Da auch Jupyter Notebooks erstellt wurden, sollten diese auch irgendwie anständig publiziert werden können.
                                        Hieraus ist der Applikationsteil “Notebooks” entstanden. Dieser listet die vorhandenen Notebooks auf und 
                                        beschreibt kurz deren Inhalt.
                                        
                                        Wer will kann die Notebooks auch direkt innerhalb eines Containers im Jupyter Lab ansehen. Klicke dazu auf
                                        [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/iwanimsand/ffhs-semarb-statda-davi-public/master?urlpath=lab%2Ftree%2Fnotebooks)
                                        '''
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Button(
                                                    "Jupyter Notebooks", color="warning", className="mt-auto",
                                                    href='/notebooks'
                                                ),
                                                className='text-center'
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                ),
            ],
            className='mb-4'
        ),
        html.Hr(className="my-2")
    ]
)
