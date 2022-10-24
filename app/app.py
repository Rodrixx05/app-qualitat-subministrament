import utils.power_vision_lib as pvl
import utils.app_lib as lib

from dash import Dash, dcc, html, Input, Output, State, MATCH
import dash_bootstrap_components as dbc

from datetime import datetime, timedelta

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1('Informe de qualitat de subministrament elèctric', style = {'textAlign': 'center', 'margin-bottom': '30px'}))),
    dbc.Row([dbc.Col([
                dbc.Row(dbc.Col(html.H4('Arxiu de variables generals', style = {'textAlign': 'center'}))), 
                dbc.Row(dbc.Col(
                    dcc.Upload(
                    id='upload-general',
                    children=html.Div([
                        'Arrastra o ',
                        html.A('Selecciona arxiu')
                    ]),
                    style={
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    accept = '.txt'))),
                dbc.Row(dbc.Col(html.Div(id = 'child-general', style = {'textAlign': 'center'})))], width = 4),
            dbc.Col([
                dbc.Row(dbc.Col(html.H4('Arxiu de variables de factor de potència', style = {'textAlign': 'center'}))), 
                dbc.Row(dbc.Col(
                    dcc.Upload(
                    id='upload-fp',
                    children=html.Div([
                        'Arrastra o ',
                        html.A('Selecciona arxiu')
                    ]),
                    style={
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    accept = '.txt'))),
                dbc.Row(dbc.Col(html.Div(id = 'child-fp', style = {'textAlign': 'center'})))], width = 4)], justify = 'evenly', style = {"margin-bottom": "30px"}),
    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col(html.H4('Llengua', style = {'textAlign': 'center'}))),
            dbc.Row(dbc.Col(dcc.RadioItems(id = 'llengua', options = {'cat': 'Català', 'cas': 'Castellà'}, value = 'cat', inputStyle={"margin-left": "8px", "margin-right": "5px"}), style = {'textAlign': 'center'}))
        ], width = 4),
        dbc.Col([
            dbc.Row(dbc.Col(html.H4('Any de lectura', style = {'textAlign': 'center'}))),
            dbc.Row(dbc.Col(dcc.Input(id = 'any', type = 'number', placeholder = 'Any', value = datetime.now().year, style = {'textAlign': 'center'}), style = {'textAlign': 'center'}))
        ], width = 4)], justify = 'evenly', style = {"margin-bottom": "30px"}),
    dbc.Row(dbc.Col(dbc.Button(id = 'carregar', children = 'Carregar'), style = {'textAlign': 'center'}), style = {"margin-bottom": "50px"}),
    html.Div(id = 'info-layout')
])

@app.callback(
    Output('child-general', 'children'),
    Input('upload-general', 'contents'),
    State('upload-general', 'filename')
)
def actualitzar_arxiu_general(clicks, filename):
    return html.Div(filename)

@app.callback(
    Output('child-fp', 'children'),
    Input('upload-fp', 'contents'),
    State('upload-fp', 'filename')
)
def actualitzar_arxiu_fp(clicks, filename):
    return html.Div(filename)


@app.callback(
    Output('info-layout', 'children'),
    Input('carregar', 'n_clicks'),
    State('upload-general', 'contents'),
    State('upload-general', 'filename'),
    State('upload-fp', 'contents'),
    State('upload-fp', 'filename'),
    State('llengua', 'value'),
    State('any', 'value'), 
)
def carregar_info(clicks, contents_general, filename_general, contents_fp, filename_fp, llengua, any):
    if clicks:
        try:
            if '.TXT' in filename_general.upper():
                df_general = lib.decode_content_df(contents_general)

        except Exception as e:
            print(e)
            return html.Div(["L'arxiu general no té el format correcte"], style = {'textAlign': 'center'})
        
        try:
            if '.TXT' in filename_fp.upper():
                df_fp = lib.decode_content_df(contents_fp)

        except Exception as e:
            print(e)
            return html.Div(["L'arxiu de factors de potència no té el format correcte"], style = {'textAlign': 'center'})
        
        df = lib.clean_df(df_general, df_fp, any)
        min_date = df['dia_hora'].min()
        max_date = df['dia_hora'].max()

        info_layout = [
            dbc.Container([
                dbc.Row(dbc.Col(html.H2('Tensió Composta', style = {'textAlign': 'center', 'margin-top': '60px'}))),
                dbc.Row(dbc.Col(dcc.Graph(id = {'type': 'graph', 'index': 'tensio-composta'}, figure = pvl.grafic_tensio_composta(df, llengua)))),
                dbc.Row(dbc.Col(dcc.DatePickerRange(id = {'type': 'date', 'index': 'tensio-composta'}, start_date = min_date, end_date = max_date, min_date_allowed = min_date.date(), max_date_allowed = max_date.date() + timedelta(days = 1), start_date_placeholder_text = 'Data inicial', end_date_placeholder_text = 'Data final'), style = {'textAlign': 'center', 'margin-bottom': '30px'})),
                dbc.Row([
                    dbc.Col(dbc.Table.from_dataframe(pvl.taula_tensio_composta_resum(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'), width = 6),
                    dbc.Col(dbc.Table.from_dataframe(pvl.taula_tensio_composta_desviacions(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'), width = 6)
                ]),
                dbc.Row(dbc.Col(dbc.Table.from_dataframe(pvl.taula_tensio_composta_desequilibris(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'))),
                dbc.Row(dbc.Col(html.H2('Tensió Simple', style = {'textAlign': 'center', 'margin-top': '60px'}))),
                dbc.Row(dbc.Col(dcc.Graph(id = {'type': 'graph', 'index': 'tensio-simple'}, figure = pvl.grafic_tensio_simple(df, llengua)))),
                dbc.Row(dbc.Col(dcc.DatePickerRange(id = {'type': 'date', 'index': 'tensio-simple'}, start_date = min_date, end_date = max_date, min_date_allowed = min_date.date(), max_date_allowed = max_date.date(), start_date_placeholder_text = 'Data inicial', end_date_placeholder_text = 'Data final'), style = {'textAlign': 'center', 'margin-bottom': '30px'})),
                dbc.Row([
                    dbc.Col(dbc.Table.from_dataframe(pvl.taula_tensio_simple_resum(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'), width = 6),
                    dbc.Col(dbc.Table.from_dataframe(pvl.taula_tensio_simple_desviacions(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'), width = 6)
                ]),
                dbc.Row(dbc.Col(dbc.Table.from_dataframe(pvl.taula_tensio_simple_desequilibris(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'))),
                dbc.Row(dbc.Col(html.H2('Potències', style = {'textAlign': 'center', 'margin-top': '60px'}))),
                dbc.Row(dbc.Col(dcc.Graph(id = {'type': 'graph', 'index': 'potencia-activa'}, figure = pvl.grafic_potencia_activa(df, llengua)))),
                dbc.Row(dbc.Col(dcc.DatePickerRange(id = {'type': 'date', 'index': 'potencia-activa'}, start_date = min_date, end_date = max_date, min_date_allowed = min_date.date(), max_date_allowed = max_date.date(), start_date_placeholder_text = 'Data inicial', end_date_placeholder_text = 'Data final'), style = {'textAlign': 'center', 'margin-bottom': '30px'})),
                dbc.Row(dbc.Col(dbc.Table.from_dataframe(pvl.taula_potencies_cos_fi(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'))),
                dbc.Row(dbc.Col(dcc.Graph(id = {'type': 'graph', 'index': 'factor-potencia'}, figure = pvl.grafic_factor_potencia(df, llengua)))),
                dbc.Row(dbc.Col(dcc.DatePickerRange(id = {'type': 'date', 'index': 'factor-potencia'}, start_date = min_date, end_date = max_date, min_date_allowed = min_date.date(), max_date_allowed = max_date.date(), start_date_placeholder_text = 'Data inicial', end_date_placeholder_text = 'Data final'), style = {'textAlign': 'center', 'margin-bottom': '30px'})),
                dbc.Row(dbc.Col(html.H2('Distorsions harmòniques', style = {'textAlign': 'center', 'margin-top': '60px'}))),
                dbc.Row(dbc.Col(dcc.Graph(id = {'type': 'graph', 'index': 'tdhv'}, figure = pvl.grafic_dist_har_tensio(df, llengua)))),
                dbc.Row(dbc.Col(dcc.DatePickerRange(id = {'type': 'date', 'index': 'tdhv'}, start_date = min_date, end_date = max_date, min_date_allowed = min_date.date(), max_date_allowed = max_date.date(), start_date_placeholder_text = 'Data inicial', end_date_placeholder_text = 'Data final'), style = {'textAlign': 'center', 'margin-bottom': '30px'})),
                dbc.Row(dbc.Col(dcc.Graph(id = {'type': 'graph', 'index': 'tdhi'}, figure = pvl.grafic_dist_har_corrent(df, llengua)))),
                dbc.Row(dbc.Col(dcc.DatePickerRange(id = {'type': 'date', 'index': 'tdhi'}, start_date = min_date, end_date = max_date, min_date_allowed = min_date.date(), max_date_allowed = max_date.date(), start_date_placeholder_text = 'Data inicial', end_date_placeholder_text = 'Data final'), style = {'textAlign': 'center', 'margin-bottom': '30px'})),
                dbc.Row(dbc.Col(html.H2("Detall d'harmònics de corrent", style = {'textAlign': 'center', 'margin-top': '60px'}))),
                dbc.Row(dbc.Col(dcc.Graph(id = {'type': 'graph', 'index': 'hi-freq'}, figure = pvl.grafic_har_corrent_frequencia(df, llengua), style = {'height': '1350px'}))),
                dbc.Row(dbc.Col(dcc.DatePickerRange(id = {'type': 'date', 'index': 'hi-freq'}, start_date = min_date, end_date = max_date, min_date_allowed = min_date.date(), max_date_allowed = max_date.date(), start_date_placeholder_text = 'Data inicial', end_date_placeholder_text = 'Data final'), style = {'textAlign': 'center', 'margin-bottom': '30px'})),
                dbc.Row(dbc.Col(html.H2('Corrent', style = {'textAlign': 'center'}))),
                dbc.Row(dbc.Col(dcc.Graph(id = {'type': 'graph', 'index': 'corrent', 'margin-top': '60px'}, figure = pvl.grafic_corrents(df, llengua)))),
                dbc.Row(dbc.Col(dcc.DatePickerRange(id = {'type': 'date', 'index': 'corrent'}, start_date = min_date, end_date = max_date, min_date_allowed = min_date.date(), max_date_allowed = max_date.date(), start_date_placeholder_text = 'Data inicial', end_date_placeholder_text = 'Data final'), style = {'textAlign': 'center', 'margin-bottom': '30px'})),
                dbc.Row([
                    dbc.Col(dbc.Table.from_dataframe(pvl.taula_corrent_resum(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'), width = 6),
                    dbc.Col(dbc.Table.from_dataframe(pvl.taula_corrent_desequilibris(df, llengua), striped=True, bordered=True, style = {'width': '450px', 'margin-left': 'auto', 'margin-right': 'auto', 'textAlign': 'center'}, class_name = 'center'), width = 6)
                ]),
            ])
        ]

        return info_layout

@app.callback(
    Output({'type': 'graph', 'index': MATCH}, 'figure'),
    Input({'type': 'date', 'index': MATCH}, 'start_date'),
    Input({'type': 'date', 'index': MATCH}, 'end_date'),
    State({'type': 'graph', 'index': MATCH}, 'figure')
)

def actualitzar_dates(start_date, end_date, figure):
    range = []
    for date in [start_date, end_date]:
        format_string = '%Y-%m-%dT%H:%M:%S' if 'T' in date else '%Y-%m-%d'
        date_dt = datetime.strptime(date, format_string)
        range.append(date_dt)

    figure['layout']['xaxis']= dict(range = range)
    return figure


if __name__ == "__main__":
    app.run_server(debug=False)
