import utils.power_vision_lib as pvl
import utils.app_lib as lib

from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

from datetime import datetime

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1('Informe qualitat subministrament elèctric', style = {'textAlign': 'center', 'margin-bottom': '30px'}))),
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
            dbc.Row(dbc.Col(dcc.RadioItems(id = 'llengua', options = ['Català', 'Castellà'], value = 'Català', inputStyle={"margin-left": "8px", "margin-right": "5px"}), style = {'textAlign': 'center'}))
        ], width = 4),
        dbc.Col([
            dbc.Row(dbc.Col(html.H4('Any de lectura', style = {'textAlign': 'center'}))),
            dbc.Row(dbc.Col(dcc.Input(id = 'any', type = 'number', placeholder = 'Any', value = datetime.now().year, style = {'textAlign': 'center'}), style = {'textAlign': 'center'}))
        ], width = 4)], justify = 'evenly', style = {"margin-bottom": "30px"}),
    dbc.Row(dbc.Col(dbc.Button(id = 'carregar', children = 'Carregar'), style = {'textAlign': 'center'})),
    html.Div(dbc.Container(html.Div(id = 'info-layout')))
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
            return html.Div(["L'arxiu general no té el format correcte"])
        
        try:
            if '.TXT' in filename_fp.upper():
                df_fp = lib.decode_content_df(contents_fp)

        except Exception as e:
            print(e)
            return html.Div(["L'arxiu de factors de potència no té el format correcte"], style = {'textAlign': 'center'})
        
        df = lib.clean_df(df_general, df_fp, any)

        return html.Div(dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True))

if __name__ == "__main__":
    app.run_server(debug=True)
