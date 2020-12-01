# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:52:25 2020

@author: madit
"""

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
social_options=["Semua Bidang Social","Kesehatan","Pendidikan","Modal Sosial","Pemukiman"]
eco_options=["Semua Bidang Ekonomi","Keragaman Produksi","Perdagangan","Akses Distribusi","Akses Kredit","Lembaga Ekonomi","Keterbukaan Wilayah"]
env_options=["Semua Bidang Lingkungan","Kualitas Lingkungan","Potensi dan Tanggap Bencana"]

slicesDict = {
        "Semua Bidang Social":CONST_SOCIAL,
        "Semua Bidang Ekonomi":CONST_ECO,
        "Semua Bidang Lingkungan":CONST_ENV,
        "Kesehatan":kesehatan,
        "Pendidikan":pendidikan,
        "Modal Sosial":modal_sosial,
        "Pemukiman":pemukiman,
        "Keragaman Produksi":keragaman_produksi,
        "Perdagangan":perdagangan,
        "Akses Distribusi":akses_distribusi,
        "Akses Kredit":akses_kredit,
        "Lembaga Ekonomi":lembaga_ekonomi,
        "Keterbukaan Wilayah":keterbukaan_wilayah,
        "Kualitas Lingkungan":kualitas_lingkungan,
        "Potensi dan Tanggap Bencana":potensi_bencana
}

optionsDict ={
        "Social":social_options,
        "Eco":eco_options,
        "Env":env_options
        }


def cal_point(slices, arrayPoint):
    
    
    arrayPoint[0]=arrayValue.iloc[slices].sum()
    arrayPoint[1]=slices.stop*5-arrayPoint[0]
    return arrayPoint


@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'),
              Input('radio-mode','value'))
def render_content(tab,mode):
    
    
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
    else:
    
        df_selected = pd.DataFrame({
        "Status": ["Fullfiled", "Unfullfiled"],
        "Amount": cal_point(slicesDict[mode])
        })
        
        fig = px.pie(df_selected, values='Point', names='Status',title='IDM {}'.format(mode))
    
    
        return html.Div(children=[
                    
                dcc.Graph(
                        id='example-graph-1',
                        figure=fig
                ),
                html.Div([
                    dcc.RadioItems(
                        id='xaxis-type',
                        options=[{'label': i, 'value': i} for i in optionsDict[tab]],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ],
                style={'width': '48%', 'display': 'inline-block'}),
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df_labeled.columns],
                    data=df_labeled.iloc[slicesDict[mode]].to_dict('records'),
                    page_size=7,
                    style_table={'height': '300px', 'overflowY': 'auto'},
                    sort_action="native"
                )
            ])
        
        
    if tab == 'social':
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
