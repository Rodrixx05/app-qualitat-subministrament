import pandas as pd
import numpy as np
import os
import datetime
import plotly.express as px
import plotly.graph_objects as go
import pickle

with open(os.path.join(os.path.dirname(__file__), 'trad_columns.pkl'), 'rb') as file:
    trad_columns = pickle.load(file)

def taula_tensio_simple_resum(df, llengua = 'cat'):
    columnes_original = ['tensio_1', 'tensio_2', 'tensio_3', 'tensio_tri_fn']
    columnes = ['L1 (V)', 'L2 (V)', 'L3 (V)', 'Tri (V)']
    index_cat = ['Mitjana', 'Màxim', 'Mínim']
    index_cas = ['Media', 'Máximo', 'Mínimo']
    
    mitjana = df[columnes_original].apply(np.mean).apply(round, args = [2])
    maxim = df[columnes_original].apply(max).apply(round, args = [2])
    minim = df[columnes_original].apply(min).apply(round, args = [2])
    
    df_final = pd.DataFrame([mitjana, maxim, minim])
    df_final.columns = columnes
    if llengua == 'cas':
        df_final.index = index_cas
    else:
        df_final.index = index_cat
        
        df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula

def taula_tensio_simple_desviacions(df, llengua = 'cat'):
    columnes_original = ['tensio_1', 'tensio_2', 'tensio_3', 'tensio_tri_fn']
    columnes = ['L1 (%)', 'L2 (%)', 'L3 (%)', 'Tri (%)']
    index_cat = ['Mitjana', 'Màxim', 'Mínim']
    index_cas = ['Media', 'Máximo', 'Mínimo']
    
    desviacions_df = (df[columnes_original] / 230 - 1) * 100
    
    mitjana = desviacions_df.apply(np.mean).apply(round, args = [2])
    maxim = desviacions_df.apply(max).apply(round, args = [2])
    minim = desviacions_df.apply(min).apply(round, args = [2])
    
    df_final = pd.DataFrame([mitjana, maxim, minim])
    df_final.columns = columnes
    if llengua == 'cas':
        df_final.index = index_cas
    else:
        df_final.index = index_cat
    
    df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula

def taula_tensio_simple_desequilibris(df, llengua = 'cat'):
    columnes_original = ['tensio_l1', 'tensio_l2', 'tensio_l3', 'tensio_tri_fn']
    columnes = ['L1 (%)', 'L2 (%)', 'L3 (%)', 'Tri (%)']
    index = 'Media' if llengua == 'cas' else 'Mitjana'
    
    resum_df = taula_tensio_simple_resum(df, llengua)
    mitjana = np.mean(resum_df.loc[index])
    
    serie_final = round((resum_df.loc[index] / mitjana - 1) * 100, 2)
    df_final = pd.DataFrame(serie_final).transpose()
    df_final.columns = columnes
    df_final.index = ['Desequilibri']
    
    df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula


def taula_tensio_composta_resum(df, llengua = 'cat'):
    columnes_original = ['tensio_1_2', 'tensio_2_3', 'tensio_3_1', 'tensio_tri_ff']
    columnes = ['L1-L2 (V)', 'L2-L3 (V)', 'L3-L1 (V)', 'Tri (V)']
    index_cat = ['Mitjana', 'Màxim', 'Mínim']
    index_cas = ['Media', 'Máximo', 'Mínimo']
    
    mitjana = df[columnes_original].apply(np.mean).apply(round, args = [2])
    maxim = df[columnes_original].apply(max).apply(round, args = [2])
    minim = df[columnes_original].apply(min).apply(round, args = [2])
    
    df_final = pd.DataFrame([mitjana, maxim, minim])
    df_final.columns = columnes
    if llengua == 'cas':
        df_final.index = index_cas
    else:
        df_final.index = index_cat
        
        df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula

def taula_tensio_composta_desviacions(df, llengua = 'cat'):
    columnes_original = ['tensio_1_2', 'tensio_2_3', 'tensio_3_1', 'tensio_tri_ff']
    columnes = ['L1-L2 (%)', 'L2-L3 (%)', 'L3-L1 (%)', 'Tri (%)']
    index_cat = ['Mitjana', 'Màxim', 'Mínim']
    index_cas = ['Media', 'Máximo', 'Mínimo']
    
    desviacions_df = (df[columnes_original] / 400 - 1) * 100
    
    mitjana = desviacions_df.apply(np.mean).apply(round, args = [2])
    maxim = desviacions_df.apply(max).apply(round, args = [2])
    minim = desviacions_df.apply(min).apply(round, args = [2])
    
    df_final = pd.DataFrame([mitjana, maxim, minim])
    df_final.columns = columnes
    if llengua == 'cas':
        df_final.index = index_cas
    else:
        df_final.index = index_cat

        df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula

def taula_tensio_composta_desequilibris(df, llengua = 'cat'):
    columnes_original = ['tensio_1_2', 'tensio_2_3', 'tensio_3_1', 'tensio_tri_ff']
    columnes = ['L1-L2 (%)', 'L2-L3 (%)', 'L3-L1 (%)', 'Tri (%)']
    index = 'Media' if llengua == 'cas' else 'Mitjana'
    
    resum_df = taula_tensio_composta_resum(df, llengua)
    mitjana = np.mean(resum_df.loc[index])
    
    serie_final = round((resum_df.loc[index] / mitjana - 1) * 100, 2)
    df_final = pd.DataFrame(serie_final).transpose()
    df_final.columns = columnes
    df_final.index = ['Desequilibri']
    
    df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula

def taula_potencies_cos_fi(df, llengua = 'cat'):
    columnes_original = ['pot_act_tri', 'pot_apa_tri']
    if llengua == 'cas':
        columnes = ['P. Activa (kW)', 'P. Aparente (kVA)', 'cos(' + r'$\phi$' + ')']
    else:
        columnes = ['P. Activa (kW)', 'P. Aparent (kVA)', 'cos(' + r'$\phi$' + ')']
    index = 'Media' if llengua == 'cas' else 'Mitjana'
    
    serie_final = np.mean(df[columnes_original])
    serie_final['cos_phi'] = serie_final['pot_act_tri'] / serie_final['pot_apa_tri']
    serie_final.index = columnes
    
    df_final = pd.DataFrame(round(serie_final, 2)).transpose()
    df_final.index = ['Mitjana']
    
    df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula

def taula_corrent_resum(df, llengua = 'cat'):
    columnes_original = ['corrent_1', 'corrent_2', 'corrent_3', 'corrent_n']
    columnes = ['L1 (A)', 'L2 (A)', 'L3 (A)', 'LN (A)']
    index_cat = ['Mitjana', 'Màxim', 'Mínim']
    index_cas = ['Media', 'Máximo', 'Mínimo']
    
    mitjana = df[columnes_original].apply(np.mean).apply(round, args = [2])
    maxim = df[columnes_original].apply(max).apply(round, args = [2])
    minim = df[columnes_original].apply(min).apply(round, args = [2])
    
    df_final = pd.DataFrame([mitjana, maxim, minim])
    df_final.columns = columnes
    if llengua == 'cas':
        df_final.index = index_cas
    else:
        df_final.index = index_cat
        
    df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula

def taula_corrent_desequilibris(df, llengua = 'cat'):
    columnes_original = ['corrent_1', 'corrent_2', 'corrent_3']
    columnes = ['L1-L2 (%)', 'L2-L3 (%)', 'L3-L1 (%)']
    index = 'Media' if llengua == 'cas' else 'Mitjana'
    
    df_inicial = df[columnes_original].copy()
    for index_fila, row in df_inicial.iterrows():
        df_inicial.loc[index_fila, 'corrent_mitjana'] = np.mean(row)
    
    df_inicial['corrent_1_2'] = (df_inicial['corrent_1'] - df_inicial['corrent_2']) / df_inicial['corrent_mitjana'] * 100
    df_inicial['corrent_2_3'] = (df_inicial['corrent_2'] - df_inicial['corrent_3']) / df_inicial['corrent_mitjana'] * 100
    df_inicial['corrent_3_1'] = (df_inicial['corrent_3'] - df_inicial['corrent_1']) / df_inicial['corrent_mitjana'] * 100
    
    df_inicial[['corrent_1_2', 'corrent_2_3', 'corrent_3_1']].apply(np.mean)
    serie_final = df_inicial[['corrent_1_2', 'corrent_2_3', 'corrent_3_1']].apply(np.mean)
    serie_final.index = columnes
    
    df_final = pd.DataFrame(round(serie_final, 2)).transpose()
    df_final.index = ['Desequilibri']
    
    df_final.reset_index(names = '', inplace = True)

    taula = go.Figure(data = [go.Table(
        header = dict(values = list(df_final.columns),
                        align = 'center'),
        cells = dict(values = [df_final[col] for col in df_final.columns],
                        align = 'center')
    )])
    taula.update_layout(height = len(df_final) * 35, margin=dict(r=5, l=5, t=5, b=5))
    return taula

def grafic_tensio_simple(df, llengua = 'cat', data_inici = None, data_final = None):
    columnes_original = ['tensio_1', 'tensio_2', 'tensio_3', 'tensio_tri_fn']
    titol = 'Evolución de la tensión simple' if llengua == 'cas' else 'Evolució de la tensió simple'
    colors = ['#FF2222', '#00A6FF', '#929292', '#0013FF']
    
    if llengua == 'cas':
        eixos = {'value': 'Tensión simple (V)', 'dia_hora': 'Fecha', 'variable': 'Leyenda'}
    else:
        eixos = {'value': 'Tensió simple (V)', 'dia_hora': 'Data', 'variable': 'Llegenda'}
    
    variables = {'tensio_1': 'L1', 'tensio_2': 'L2', 'tensio_3': 'L3', 'tensio_tri_fn': 'Tri'}

    if data_inici is None:
        data_inici_dt = min(df['dia_hora'])
    else:
        data_inici_dt = datetime.datetime.strptime(data_inici, '%d/%m/%Y')
    if data_final is None:
        data_final_dt = max(df['dia_hora'])
    else:
        data_final_dt = datetime.datetime.strptime(data_final, '%d/%m/%Y')      
    
    grafic = px.line(data_frame = df, x = 'dia_hora', y = columnes_original, title = titol, labels = eixos, range_x = [data_inici_dt, data_final_dt], color_discrete_sequence = colors)
    grafic.for_each_trace(lambda t: t.update(name = variables[t.name]))
    return grafic

def grafic_tensio_composta(df, llengua = 'cat', data_inici = None, data_final = None):
    columnes_original = ['tensio_1_2', 'tensio_2_3', 'tensio_3_1', 'tensio_tri_ff']
    titol = 'Evolución de la tensión compuesta' if llengua == 'cas' else 'Evolució de la tensió composta'
    colors = ['#FF2222', '#00A6FF', '#929292', '#0013FF']
    
    if llengua == 'cas':
        eixos = {'value': 'Tensión compuesta (V)', 'dia_hora': 'Fecha', 'variable': 'Leyenda'}
    else:
        eixos = {'value': 'Tensió compuesta (V)', 'dia_hora': 'Data', 'variable': 'Llegenda'}
    
    variables = {'tensio_1_2': 'L1-L2', 'tensio_2_3': 'L2-L3', 'tensio_3_1': 'L3-L1', 'tensio_tri_ff': 'Tri'}
    
    if data_inici is None:
        data_inici_dt = min(df['dia_hora'])
    else:
        data_inici_dt = datetime.datetime.strptime(data_inici, '%d/%m/%Y')
    if data_final is None:
        data_final_dt = max(df['dia_hora'])
    else:
        data_final_dt = datetime.datetime.strptime(data_final, '%d/%m/%Y')     
    
    grafic = px.line(data_frame = df, x = 'dia_hora', y = columnes_original, title = titol, labels = eixos, range_x = [data_inici_dt, data_final_dt], color_discrete_sequence = colors)
    grafic.for_each_trace(lambda t: t.update(name = variables[t.name]))
    return grafic

def grafic_potencia_activa(df, llengua = 'cat', data_inici = None, data_final = None):
    columnes_original = ['pot_act_1', 'pot_act_2', 'pot_act_3', 'pot_act_tri']
    titol = 'Curva de carga' if llengua == 'cas' else 'Corba de càrrega'
    colors = ['#FF2222', '#00A6FF', '#929292', '#0013FF']
    
    if llengua == 'cas':
        eixos = {'value': 'Potencia activa (kW)', 'dia_hora': 'Fecha', 'variable': 'Leyenda'}
    else:
        eixos = {'value': 'Potència activa (kW)', 'dia_hora': 'Data', 'variable': 'Llegenda'}
    
    variables = {'pot_act_1': 'L1', 'pot_act_2': 'L2', 'pot_act_3': 'L3', 'pot_act_tri': 'Tri'}

    if data_inici is None:
        data_inici_dt = min(df['dia_hora'])
    else:
        data_inici_dt = datetime.datetime.strptime(data_inici, '%d/%m/%Y')
    if data_final is None:
        data_final_dt = max(df['dia_hora'])
    else:
        data_final_dt = datetime.datetime.strptime(data_final, '%d/%m/%Y')     
    
    grafic = px.line(data_frame = df, x = 'dia_hora', y = columnes_original, title = titol, labels = eixos, range_x = [data_inici_dt, data_final_dt], color_discrete_sequence = colors)
    grafic.for_each_trace(lambda t: t.update(name = variables[t.name]))
    return grafic

def grafic_factor_potencia(df, llengua = 'cat', data_inici = None, data_final = None):
    columnes_original = ['fp_1', 'fp_2', 'fp_3', 'fp_tri']
    titol = 'Evolución del factor de potencia' if llengua == 'cas' else 'Evolució del factor de potència'
    colors = ['#FF2222', '#00A6FF', '#929292', '#0013FF']
    
    if llengua == 'cas':
        eixos = {'value': 'Factor de potencia (-)', 'dia_hora': 'Fecha', 'variable': 'Leyenda'}
    else:
        eixos = {'value': 'Factor de potència (-)', 'dia_hora': 'Data', 'variable': 'Llegenda'}
    
    variables = {'fp_1': 'L1', 'fp_2': 'L2', 'fp_3': 'L3', 'fp_tri': 'Tri'}
    
    if data_inici is None:
        data_inici_dt = min(df['dia_hora'])
    else:
        data_inici_dt = datetime.datetime.strptime(data_inici, '%d/%m/%Y')
    if data_final is None:
        data_final_dt = max(df['dia_hora'])
    else:
        data_final_dt = datetime.datetime.strptime(data_final, '%d/%m/%Y')    
    
    grafic = px.line(data_frame = df, x = 'dia_hora', y = columnes_original, title = titol, labels = eixos, range_x = [data_inici_dt, data_final_dt], color_discrete_sequence = colors)
    grafic.for_each_trace(lambda t: t.update(name = variables[t.name]))
    return grafic

def grafic_dist_har_tensio(df, llengua = 'cat', data_inici = None, data_final = None):
    columnes_original = ['dist_har_v1', 'dist_har_v2', 'dist_har_v3']
    titol = 'Evolución la tasa de distorsión armónica en tensión' if llengua == 'cas' else 'Evolució de la taxa de distorió harmònica en tensió'
    colors = ['#FF2222', '#00A6FF', '#929292', '#0013FF']    
    
    if llengua == 'cas':
        eixos = {'value': 'Tasa de distorisón armónica (%V)', 'dia_hora': 'Fecha', 'variable': 'Leyenda'}
    else:
        eixos = {'value': 'Taxa de distorsió harmònica (%V)', 'dia_hora': 'Data', 'variable': 'Llegenda'}
    
    variables = {'dist_har_v1': 'L1', 'dist_har_v2': 'L2', 'dist_har_v3': 'L3'}
    
    if data_inici is None:
        data_inici_dt = min(df['dia_hora'])
    else:
        data_inici_dt = datetime.datetime.strptime(data_inici, '%d/%m/%Y')
    if data_final is None:
        data_final_dt = max(df['dia_hora'])
    else:
        data_final_dt = datetime.datetime.strptime(data_final, '%d/%m/%Y')    
    
    grafic = px.line(data_frame = df, x = 'dia_hora', y = columnes_original, title = titol, labels = eixos, range_x = [data_inici_dt, data_final_dt], color_discrete_sequence = colors)
    grafic.for_each_trace(lambda t: t.update(name = variables[t.name]))
    return grafic

def grafic_dist_har_corrent(df, llengua = 'cat', data_inici = None, data_final = None):
    columnes_original = ['dist_har_i1', 'dist_har_i2', 'dist_har_i3']
    titol = 'Evolución la tasa de distorsión armónica en corriente' if llengua == 'cas' else 'Evolució de la taxa de distorió harmònica en corrent'
    colors = ['#FF2222', '#00A6FF', '#929292', '#0013FF']    
    
    if llengua == 'cas':
        eixos = {'value': 'Tasa de distorisón armónica (%I)', 'dia_hora': 'Fecha', 'variable': 'Leyenda'}
    else:
        eixos = {'value': 'Taxa de distorsió harmònica (%I)', 'dia_hora': 'Data', 'variable': 'Llegenda'}
    variables = {'dist_har_i1': 'L1', 'dist_har_i2': 'L2', 'dist_har_i3': 'L3'}
    
    if data_inici is None:
        data_inici_dt = min(df['dia_hora'])
    else:
        data_inici_dt = datetime.datetime.strptime(data_inici, '%d/%m/%Y')
    if data_final is None:
        data_final_dt = max(df['dia_hora'])
    else:
        data_final_dt = datetime.datetime.strptime(data_final, '%d/%m/%Y')       
    
    grafic = px.line(data_frame = df, x = 'dia_hora', y = columnes_original, title = titol, labels = eixos, range_x = [data_inici_dt, data_final_dt], color_discrete_sequence = colors)
    grafic.for_each_trace(lambda t: t.update(name = variables[t.name]))
    return grafic

def grafic_har_corrent_frequencia(df, llengua = 'cat', data_inici = None, data_final = None):
    columnes_original = [['har_2_i1', 'har_3_i1', 'har_4_i1', 'har_5_i1'], ['har_2_i2', 'har_3_i2', 'har_4_i2', 'har_5_i2'], ['har_2_i3', 'har_3_i3', 'har_4_i3', 'har_5_i3']]
    colors = ['#FF2222', '#00A6FF', '#929292', '#0013FF']    
    
    if data_inici is None:
        data_inici_dt = min(df['dia_hora'])
    else:
        data_inici_dt = datetime.datetime.strptime(data_inici, '%d/%m/%Y')
    if data_final is None:
        data_final_dt = max(df['dia_hora'])
    else:
        data_final_dt = datetime.datetime.strptime(data_final, '%d/%m/%Y')   
        
    for index, linia in enumerate(columnes_original):   
        titol = f'Evolución de los armónicos de corriente de L{index + 1}' if llengua == 'cas' else f'Evolució dels harmònics de corrent de L{index + 1}'
        if llengua == 'cas':
            eixos = {'value': 'Intensidad del armónico (%I)', 'dia_hora': 'Fecha', 'variable': 'Leyenda'}
        else:
            eixos = {'value': "Intensitat de l'harmonic (%I)", 'dia_hora': 'Data', 'variable': 'Llegenda'}
            variables = {f'har_2_i{index + 1}': 'Harmònic 2', f'har_3_i{index + 1}': 'Harmònic 3', f'har_4_i{index + 1}': 'Harmònic 4', f'har_5_i{index + 1}': 'Harmònic 5'}

        grafic = px.line(data_frame = df, x = 'dia_hora', y = linia, title = titol, labels = eixos, range_x = [data_inici_dt, data_final_dt], color_discrete_sequence = colors)
        grafic.for_each_trace(lambda t: t.update(name = variables[t.name]))
        grafic.show()

def grafic_corrents(df, llengua = 'cat', data_inici = None, data_final = None):
    columnes_original = ['corrent_1', 'corrent_2', 'corrent_3', 'corrent_n']
    titol = 'Evolución de la corriente' if llengua == 'cas' else 'Evolució del corrent'
    colors = ['#FF2222', '#00A6FF', '#929292', '#0013FF']
    
    if llengua == 'cas':
        eixos = {'value': 'Intensidad (A)', 'dia_hora': 'Fecha', 'variable': 'Leyenda'}
    else:
        eixos = {'value': 'Intensitat (A)', 'dia_hora': 'Data', 'variable': 'Llegenda'}
    
    variables = {'corrent_1': 'L1', 'corrent_2': 'L2', 'corrent_3': 'L3', 'corrent_n': 'LN'}

    if data_inici is None:
        data_inici_dt = min(df['dia_hora'])
    else:
        data_inici_dt = datetime.datetime.strptime(data_inici, '%d/%m/%Y')
    if data_final is None:
        data_final_dt = max(df['dia_hora'])
    else:
        data_final_dt = datetime.datetime.strptime(data_final, '%d/%m/%Y')      
    
    grafic = px.line(data_frame = df, x = 'dia_hora', y = columnes_original, title = titol, labels = eixos, range_x = [data_inici_dt, data_final_dt], color_discrete_sequence = colors)
    grafic.for_each_trace(lambda t: t.update(name = variables[t.name]))
    return grafic