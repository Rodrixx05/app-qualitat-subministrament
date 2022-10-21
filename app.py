import utils.power_vision_lib as pvl

from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

app.layout = html.Div([
    dbc.Row([dbc.Col(
        dcc.Upload(
            id='upload-global',
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
            accept = '.txt'
            ), width = 6),
            dbc.Col(dcc.Upload(
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
            accept = '.txt'
            ), width = 6)]), 
    html.Div(id='output-data-upload'),
])


if __name__ == "__main__":
    app.run_server(debug=True)
