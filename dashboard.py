# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:57:07 2020

@author: madit
"""

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

CONST_SOCIAL = slice(0,32)
CONST_ECO = slice(32,44)
CONST_ENV = slice(44,47)
CONST_DESA = 0
kesehatan=slice(0,5)
pendidikan=slice(5,12)
modal_sosial=slice(12,24)
pemukiman=slice(24,32)
keragaman_produksi=slice(32,33)
perdagangan=slice(33,36)
akses_distribusi=slice(36,37)
akses_kredit=slice(37,39)
lembaga_ekonomi=slice(39,41)
keterbukaan_wilayah=slice(41,44)
kualitas_lingkungan=slice(44,45)
potensi_bencana=slice(45,47)
social_options=["Semua","Kesehatan","Pendidikan","Modal Sosial","Pemukiman"]
eco_options=["Semua","Keragaman Produksi","Perdagangan","Akses Distribusi","Akses Kredit","Lembaga Ekonomi","Keterbukaan Wilayah"]
env_options=["Semua","Kualitas Lingkungan","Potensi dan Tanggap Bencana"]
maxSocialDivision = (32)*5
maxEcoDivision= (12)*5
maxEnvDivision= (3)*5


df_value = pd.read_csv('dataset.csv', delimiter =";",skip_blank_lines=True, index_col=False,header=None)
df_label = pd.read_csv('dataset_label.csv', delimiter =";",skip_blank_lines=True, index_col=False,header=None)

df_labeled= pd.concat([df_label,df_value.loc[CONST_DESA].rename(columns={'values'})], axis=1)
df_labeled.columns=['label','index']

points = [0,0,0]

def cal_point(arrayValue,arrayPoint):
    
    
    arrayPoint[0]=arrayValue.iloc[CONST_DESA,CONST_SOCIAL].sum()
    arrayPoint[1]=arrayValue.iloc[CONST_DESA,CONST_ECO].sum()
    arrayPoint[2]=arrayValue.iloc[CONST_DESA,CONST_ENV].sum()
    return arrayPoint

points = cal_point(df_value, points)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df_social = pd.DataFrame({
    "Status": ["Fullfiled", "Unfullfiled"],
    "Amount": [points[0], maxSocialDivision-points[0]]
})
    
df_eco = pd.DataFrame({
    "Status": ["Fullfiled", "Unfullfiled"],
    "Amount": [points[1], maxEcoDivision-points[1]]
})

df_env = pd.DataFrame({
    "Status": ["Fullfiled", "Unfullfiled"],
    "Amount": [points[2], maxEnvDivision-points[2]]
})

df_all = pd.DataFrame({
    "Status": ["Fullfiled", "Unfullfiled"],
    "Amount": [sum(points), maxSocialDivision+maxEnvDivision+maxEcoDivision-sum(points)]
})

fig_sos = px.pie(df_social, values='Amount', names='Status',title='IDM Bidang Sosial')
fig_eco = px.pie(df_eco, values='Amount', names='Status',title='IDM Bidang Ekonomi')
fig_env = px.pie(df_env, values='Amount', names='Status',title='IDM Bidang Lingkungan')
fig_all = px.pie(df_all, values='Amount', names='Status',title='IDM Semua Bidang')
app.layout = html.Div(children=[
    html.H1(children='Index Desa Membangun'),
    dcc.Dropdown(
        options=[
            {'label': 'Sukapura', 'value': 'SKPR'}
        ],
        value='SKPR'
    ),
    

    html.Div(children=['''
        Ini example dari dashboard IDM.
    ''',
    dcc.Tabs(id='tabs-example', value='all', children=[
        dcc.Tab(label='Semua Bidang', value='all'),
        dcc.Tab(label='Social', value='social'),
        dcc.Tab(label='Economy', value='eco'),
        dcc.Tab(label='Environment', value='env'),
    ]),
    html.Div(id='tabs-example-content')
    ])

    
])

@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'all':
        return html.Div(children=[
            dcc.Graph(
                id='example-graph-0',
                figure=fig_all
            ),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_labeled.columns],
                data=df_labeled.to_dict('records'),
                page_size=7,
                style_table={'height': '300px', 'overflowY': 'auto'},
                sort_action="native"
            )
        ])
    elif tab == 'social':
        return html.Div(children=[
                
            dcc.Graph(
                    id='example-graph-1',
                    figure=fig_sos
            ),
            html.Div([
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in social_options],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_labeled.columns],
                data=df_labeled.iloc[CONST_SOCIAL].to_dict('records'),
                page_size=7,
                style_table={'height': '300px', 'overflowY': 'auto'},
                sort_action="native"
            )
        ])
    elif tab == 'eco':
        return html.Div(children=[
            dcc.Graph(
                id='example-graph-2',
                figure=fig_eco
            ),
            html.Div([
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in eco_options],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_labeled.columns],
                data=df_labeled.iloc[CONST_ECO].to_dict('records'),
                page_size=7,
                style_table={'height': '300px', 'overflowY': 'auto'},
                sort_action="native"
            )
        ])
    elif tab == 'env':
        return html.Div(children=[
            dcc.Graph(
                id='example-graph-3',
                figure=fig_env
            ),
            html.Div([
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in env_options],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_labeled.columns],
                data=df_labeled.iloc[CONST_ENV].to_dict('records'),
                page_size=7,
                style_table={'height': '300px', 'overflowY': 'auto'},
                sort_action="native"
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=False)