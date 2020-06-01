import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

notebooks = [
    {
        'id': 0,
        'title': '0_0_Tripdata-Datenbeschaffung',
        'src': '/assets/ipynb-html/0_0_Tripdata-Datenbeschaffung.html',
        'body':
            '''
            **Datenbeschaffung Tripdaten**
            
            In diesem Notebook werden die Tripdaten von [tripdata](https://s3.amazonaws.com/tripdata/index.html) heruntergeladen und entpackt. Man hat dann eine Menge von CSVs mit einer Grösse von ca. 18GB. Diese Daten werden in den folgenden Notebooks aufbereitet.
            '''
    },
    {
        'id': 1,
        'title': '0_1_Tripdata-Datenaufbereitung',
        'src': '/assets/ipynb-html/0_1_Tripdata-Datenaufbereitung.html',
        'body':
            '''
            **Datenaufbereitung Tripdaten**
            
            Die entpackten Tripdaten werden mit diesem Notebook aufbereitet. Dabei sind vor allem folgende Punkte erwähnenswert:
            
            _Datum und Zeit_
            * Parsen unterschiedlicher Formate in den Quellen
            * Hinzufügen der Zeitzone ```US/Eastern``` für späteres Zusammenführen mit Wetterdaten
            * Beachtung Daylight Saving Time (DST)
            
            _Analyse fehlender Daten_
            * CSV vom Juni 2013 komplett ignoriert, da zu viele Daten fehlen
            * Fehlende ```User Type``` auf ```Customer``` gesetzt
            * Zeilen mit fehlender ```Start/End Station ID``` entfernt
            
            _Berechnung zusätzlicher Merkmale_
            * Distanz Luftlinie zwischen Start und End Station
            * Alter im Jahr 2020
            
            _Unrealistische Daten (diese werden für die tägliche Zusammenfassung nicht berücksichtigt)_
            * Trips die länger als 6h dauern
            * Stationen die weiter als 30km auseinander liegen
            * Trips die von über 81 jährigen gefahren wurden
            
            '''
    },
    {
        'id': 2,
        'title': '0_2_Weatherdata-Datenaufbereitung',
        'src': '/assets/ipynb-html/0_2_Weatherdata-Datenaufbereitung.html',
        'body':
            '''
            **Datenaufbereitung Wetterdaten**
            
            Die Wetterdaten, die über von [OpenWeather](https://openweathermap.org/) für 10$ gekauft wurden, werden hier aufbereitet.
            
            _Bemerkung: Die Daten wurden nicht öffentlich gestellt, weil hier eine Lizenz erworben wurde. Erst die bearbeiteten, gefilterten und mit den Tripdaten zusammengeführten Daten stehen zur Verfügung!_  
            '''
    },
    {
        'id': 3,
        'title': '0_3_Merge-Weatherdata2Tripdata',
        'src': '/assets/ipynb-html/0_3_Merge-Weatherdata2Tripdata.html',
        'body':
            '''
            **Zusammenführung Tripdaten und Wetterdaten**
            
            Die erstellten Tripdaten und Wetterdaten werden hier zusammengeführt und die Datensätze, auf welchen die eigentlichen Analysen stattfinden, generiert.
            
            Wichtige Artefakte die für die Analysen verwendet werden _(die Aggregation und Stichprobenauswahl wurde in den Notebooks der Datenaufbereitung gemacht, hier wird nur zusammengeführt!)_:
            
            * 5000 zufällige Stichproben vom Monat Oktober 2019 (```samples_5000_201910-citibike-tripweather-data.parquet```)
            * Täglich aggregierte Daten von Jahresmitgliedern über alle Jahre ```summary-daily-subscribers_only-citibike-tripweather.parquet```
            * Täglich aggregierte Daten von Jahresmitgliedern über alle Jahre, gruppiert nach Geschlecht ```summary-daily-subscribers_only-gender_grouped-citibike-tripweather.parquet```
            '''
    },
    {
        'id': 10,
        'title': '1_0_SemArb-StatDa_Deskriptive-Analyse',
        'src': '/assets/ipynb-html/1_0_SemArb-StatDa_Deskriptive-Analyse.html',
        'body':
            '''
            **Deskriptive Analyse**
            
            Behandlung des Themas _Deskriptive Analyse_ für das Modul Statistische Datenanalyse.
            '''
    },
    {
        'id': 20,
        'title': '2_0_SemArb-StatDa_Regressionsanalyse',
        'src': '/assets/ipynb-html/2_0_SemArb-StatDa_Regressionsanalyse.html',
        'body':
            '''
            **Regressionsanalyse**
            
            Behandlung des Themas _Regressionsanalyse_ für das Modul Statistische Datenanalyse.
            '''
    },
    {
        'id': 50,
        'title': '5_0_SemArb-StatDa_Zeitreihenanalyse',
        'src': '/assets/ipynb-html/5_0_SemArb-StatDa_Zeitreihenanalyse.html',
        'body':
            '''
            **Zeitreihenanalyse**
            
            Behandlung des Themas _Zeitreihenanalyse_ für das Modul Statistische Datenanalyse.
            '''
    },
]


def create_item(id_button, id_collapse, name, body, is_open):
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    html.Button(
                        name,
                        id=id_button,
                        className='btn btn-link btn-block text-left'
                    ),
                    className='mb-0'
                )
            ),
            dbc.Collapse(
                dbc.CardBody(dcc.Markdown(body)),
                id_collapse,
                is_open=is_open
            )
        ]
    )


def create_sidepanel():
    sidepanel = html.Div(
        [
            html.H2('Jupyter Notebooks'),
            dcc.Markdown('''
            Die Jupyter Notebooks wurden zu statischem HTML konvertiert und hier aufgelistet.
                       
            Mit einem Klick auf [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/iwanimsand/ffhs-semarb-statda-davi-public/master?urlpath=lab%2Ftree%2Fnotebooks) wird ein Container gestartet und die Notebooks können direkt im Jupyter Lab angesehen werden. **Alle ausser ```0_*.ipynb``` können auch ausgeführt werden.** Es kann einen Moment dauern, bis der Container gestartet wurde.
            '''),
            html.Div(
                [
                    create_item(f"group-{idx}-toggle", f"collapse-{idx}", notebook['title'],
                                notebook['body'], is_open=idx == 0) for idx, notebook in enumerate(notebooks)
                ],
                className='accordion mb-4'
            ),
            dcc.Markdown('''
            **HINWEIS zu ```0_*.ipynb```**: Bei Notebooks, die alle Datenquellen (**18GB!**) einlesen und verarbeiten (d.h alle Notebooks mit ```0_*``` beginnend.), dauert eine Ausführung **mehrere Stunden**! Dies weil der zur Verfügung gestellte Container nicht sehr performant ist. Lokal auf einem leistungsfähigen Computer (16-Core Processor, 64GB Memory) funktioniert dies aber einwandfrei.
            
            Die aufbereiteten Datenfiles sind aber vorhanden und die restlichen Notebooks können in akzeptabler Zeit ausgeführt werden.
            ''',
                         className='small'),
        ]
    )

    return sidepanel


layout = dbc.Row(
    [
        dbc.Col(
            [
                create_sidepanel()
            ],
            md=3
        ),
        dbc.Col(
            [
                html.Iframe(id='notebook-embed',
                            src=notebooks[0]['src'],
                            className='w-100',
                            style={'height': '80vh'}),
            ],
            md=9
        ),
    ]
)


def register_callbacks(app):
    @app.callback(
        [Output(f"collapse-{idx}", "is_open") for idx, _ in enumerate(notebooks)],
        [Input(f"group-{idx}-toggle", "n_clicks") for idx, _ in enumerate(notebooks)],
        [State(f"collapse-{idx}", "is_open") for idx, _ in enumerate(notebooks)],
    )
    def toggle_accordion(*args):

        print(args)

        ctx = dash.callback_context

        if not ctx.triggered:
            return ""
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            idx = button_id.split('-')[1]
            print(button_id)
            print(idx)

        is_open = [False for i in range(len(notebooks))]
        is_open[int(idx)] = True

        return is_open

    @app.callback(
        Output('notebook-embed', 'src'),
        [Input(f"collapse-{idx}", "is_open") for idx, _ in enumerate(notebooks)],
    )
    def change_notebook_src(*args):
        return notebooks[args.index(True)]['src']
