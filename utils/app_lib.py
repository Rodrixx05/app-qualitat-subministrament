import base64
import io
import pandas as pd
import os
import pickle

with open(os.path.join(os.path.dirname(__file__), 'trad_columns.pkl'), 'rb') as file:
    trad_columns = pickle.load(file)

def decode_content_df(content):
    content_str = content.split(',')[1]
    decoded = base64.b64decode(content_str)
    df = pd.read_csv(io.StringIO(decoded.decode('latin_1')), header = 0, encoding = 'latin1')
    return df

def clean_df(df_general, df_fp, year):
    df = df_general.merge(df_fp, how = 'left', on = ['Fecha Tiempo'])
    df.rename(columns = trad_columns, inplace = True)
    df['dia_hora'] = pd.to_datetime(df['dia_hora'])
    df['dia_hora'] = df['dia_hora'].apply(lambda x: x.replace(year = year))
    columnes_divisio = [column for column in df.columns if 'corrent' in column or 'pot' in column]
    df[columnes_divisio] = df[columnes_divisio] / 1000
    return df