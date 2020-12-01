# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 00:15:38 2020

@author: madit
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:17:27 2020

@author: madit
"""

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

CONST_ALL = slice(0, 47)
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
all_options=["Semua Indeks Komposit"]
social_options=["Semua Bidang Sosial","Kesehatan","Pendidikan","Modal Sosial","Pemukiman"]
eco_options= ["Semua Bidang Ekonomi","Keragaman Produksi","Perdagangan","Akses Distribusi","Akses Kredit","Lembaga Ekonomi","Keterbukaan Wilayah"]
env_options= ["Semua Bidang Lingkungan","Kualitas Lingkungan","Potensi dan Tanggap Bencana"]
desa_options = ["Bojongsoang","Dayeuhkolot","Sukapura","Tarumajaya"]

maxSocialDivision = (32)*5
maxEcoDivision= (12)*5
maxEnvDivision= (3)*5

slicesDict = {
        "Semua Indeks Komposit":CONST_ALL,
        "Semua Bidang Sosial":CONST_SOCIAL,
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
        "Semua Bidang":all_options,
        "Sosial":social_options,
        "Ekonomi":eco_options,
        "Lingkungan":env_options
        }

desaDict={
        "Bojongsoang":0,
        "Dayeuhkolot":1,
        "Sukapura":2,
        "Tarumajaya":3
        }

df_value = pd.read_csv('dataset.csv', delimiter =";",skip_blank_lines=True)
df_label = pd.read_csv('dataset_label.csv', delimiter =";",skip_blank_lines=True, index_col=False,header=None)

df_labeled= pd.concat([df_label,df_value['Sukapura'].rename(columns={'values'})], axis=1)
df_labeled.columns=['label','index']



def cal_point(slices,arrayValue, arrayPoint,desa):
    
    
    arrayPoint[0]=arrayValue[desa][slices].sum()
    arrayPoint[1]=slices.stop*5-slices.start*5-arrayPoint[0]
    return arrayPoint

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
                        'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'
                        ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

#df_selected = pd.DataFrame({
#            "Status": ["Fullfiled", "Unfullfiled"],
#            "Point": [df_value.sum(), CONST_ALL.stop*5-df_value.sum()]
#        })
#    
#print(df_selected)
#fig = px.pie(df_selected, values='Point', names='Status',title='IDM Semua Bidang')

app.layout = html.Div(children=[ 
    
    html.Meta(charSet="utf-8"),
    html.Meta(name="viewport", content="width=device-width, initial-scale=1"),
    html.Section(id="nav-bar", children=[
        html.Nav(className="navbar navbar-expand-lg navbar-light", children=[
            html.A(className="navbar-brand",children=['''IDMJ''']),
            html.Div(id="navbarNav", className="collapse navbar-collapse", children=[
                html.Ul(className="navbar-nav ml-auto", children=[
                    html.Li(className="nav-item",children=[
                        html.A(className="nav-link", href="#",children=['''Beranda'''])        
                    ]),
                    html.Li(className="nav-item",children=[
                        html.A(className="nav-link", href="#",children=['''Tentang'''])        
                    ]), 
                    html.Li(className="nav-item",children=[
                        html.A(className="nav-link", href="#",children=['''Kontak'''])        
                    ]),
                    html.Li(className="nav-item",children=[
                        html.A(className="nav-link", href="#",children=['''Login'''])        
                    ]),
                ])        
            ])
        ])
    ]),
    html.Section(id="dashboard-section", children=[
        html.Div(className="card-section", children=[
            html.Div(className="col-lg-12 pt-4",children=[
                html.Div(className="card", children=[
                    html.Div(className="card-body", children=[
                        html.H1(className="row",children='Index Desa Membangun'),
                        dcc.Dropdown(id="dropdown-desa",
                            options=[{"label": i, "value": i} for i in desa_options
                            ],
                            value='Sukapura',
                            style={'margin-bottom':'50px'}
                        ),
                        html.Div(children=[
                        dcc.Tabs(className="row",id='tabs-example', value='Semua Bidang', children=[
                            dcc.Tab(label='Semua Bidang', value='Semua Bidang'),
                            dcc.Tab(label='Social', value='Sosial'),
                            dcc.Tab(label='Economy', value='Ekonomi'),
                            dcc.Tab(label='Environment', value='Lingkungan'),
                        ],
                            style={'margin-bottom':'50px'}),
                        html.Div(children=[
                            html.Div(className="row",id="tabs-content",children=[
                                html.Div(children=[
                                dcc.RadioItems(
                                    id='radio-mode',
                                    options=[{'label': i, 'value': i} for i in all_options],
                                    value='Semua Indeks Komposit',
                                    labelStyle={'display': 'inline-block'},
                                    inputStyle={'margin-left': '30px'}
                                )
                            ],
                            style={'width': '48%', 'display': 'inline-block'})
                            ]),
                            html.Div(
                                className="row justify-content-md-center",id='table-paging-with-graph-container'
                            ),
                            dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in df_labeled.columns],
                                style_cell={'textAlign': 'left',
                                            'whiteSpace': 'normal',
                                            'height': 'auto'},
                                style_data_conditional=[
                                {
                                    'if': {'filter_query': '{index} = 0',
                                    'column_id': 'index'},
                                    'backgroundColor': '#FF0000'
                                },{
                                    'if': {'filter_query': '{index} = 1',
                                    'column_id': 'index'},
                                    'backgroundColor': '#f90'
                                },
                                {
                                    'if': {'filter_query': '{index} = 2',
                                    'column_id': 'index'},
                                    'backgroundColor': '#ffff00'
                                },
                                {
                                    'if': {'filter_query': '{index} = 3',
                                    'column_id': 'index'},
                                    'backgroundColor': '#7fff00'
                                },
                                {
                                    'if': {'filter_query': '{index} = 4',
                                    'column_id': 'index'},
                                    'backgroundColor': '#007fff'
                                },
                                {
                                    'if': {'filter_query': '{index} = 5',
                                    'column_id': 'index'},
                                    'backgroundColor': '#e5e5e5'
                                }
                                ],
                                page_size=7,
                                page_current=0,
                                page_action='custom',
                                sort_action="custom",
                                sort_by=[],
                                style_table={'height': 'auto', 'overflowY': 'auto'}
                            ),
                            
                            ])
                        
                        ])
                    ])
                ])        
            ])
        ])
    ]),
    

    
])


@app.callback(Output('tabs-content', 'children'),
              Input('tabs-example', 'value'),
              Input('radio-mode','value')
              )
def render_content(tab,mode):
    if tab=="Semua Bidang":
        if mode not in optionsDict[tab]:
            defaultValue="Semua Indeks Komposit"
        else:
            defaultValue=mode
    elif tab=="Sosial":
        if mode not in optionsDict[tab]:
            defaultValue="Semua Bidang Sosial"
        else:
            defaultValue=mode
    elif tab=="Ekonomi":
        if mode not in optionsDict[tab]:
            defaultValue="Semua Bidang Ekonomi"
        else:
            defaultValue=mode
    elif tab=="Lingkungan":
        if mode not in optionsDict[tab]:
            defaultValue="Semua Bidang Lingkungan"
        else:
            defaultValue=mode
            
    return html.Div([
                dcc.RadioItems(
                    id='radio-mode',
                    options=[{'label': i, 'value': i} for i in optionsDict[tab]],
                    value=defaultValue,
                    labelStyle={'display': 'inline-block'}
                )
            ])

@app.callback(Output('table', 'data'),
              Input('tabs-example', 'value'),
              Input('radio-mode','value'),
              Input('table', "page_current"),
              Input('table', "page_size"),
              Input('table', 'sort_by'),
              Input('dropdown-desa','value')
              )
def render_table(tab,mode, page_current, page_size, sort_by,nama_desa):
#    if tab=="Semua Bidang":
#        if mode not in optionsDict[tab]:
#            defaultValue="Semua Indeks Komposit"
#        else:
#            defaultValue=mode
#    elif tab=="Sosial":
#        if mode not in optionsDict[tab]:
#            defaultValue="Semua Bidang Sosial"
#        else:
#            defaultValue=mode
#    elif tab=="Ekonomi":
#        if mode not in optionsDict[tab]:
#            defaultValue="Semua Bidang Ekonomi"
#        else:
#            defaultValue=mode
#    elif tab=="Lingkungan":
#        if mode not in optionsDict[tab]:
#            defaultValue="Semua Bidang Lingkungan"
#        else:
#            defaultValue=mode
    df_labeled= pd.concat([df_label,df_value[nama_desa].rename(columns={'values'})], axis=1)
    df_labeled.columns=['label','index']
    if len(sort_by):
        dff = df_labeled.iloc[slicesDict[mode]].sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df_labeled.iloc[slicesDict[mode]]
    
    
    return  dff.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
#html.Div(children=[
#                
#            dcc.Graph(
#                    id='example-graph',
#                    figure=fig
#            ),
#            html.Div([
#                dcc.RadioItems(
#                    id='radio-mode',
#                    options=[{'label': i, 'value': i} for i in optionsDict[tab]],
#                    value=defaultValue,
#                    labelStyle={'display': 'inline-block'}
#                )
#            ],
#            style={'width': '48%', 'display': 'inline-block'}),
#            dash_table.DataTable(
#                id='table',
#                columns=[{"name": i, "id": i} for i in df_labeled.columns],
#                data=dff.iloc[page_current*page_size:(page_current+ 1)*page_size ].to_dict('records'),
#                page_size=7,
#                sort_action="custom",
#                style_table={'height': '300px', 'overflowY': 'auto'}
#            )
#        ])
            
@app.callback(
    Output('table-paging-with-graph-container', "children"),
    Input('radio-mode','value'),
    Input('tabs-example', 'value'),
    Input('dropdown-desa','value'))
    
def update_graph(mode,tab,nama_desa):
    points = [0,0]
    df_selected = pd.DataFrame({
    "Status": ["Fullfiled", "Unfullfiled"],
    "Point": cal_point(slicesDict[mode],df_value,points,nama_desa)
    })
    fig = px.pie(df_selected, values='Point', names='Status',title='IDM {} - {}'.format(tab,mode))
    return html.Div(
        dcc.Graph(
            id="example-graph",
            figure=fig
        )
    )
            
    
if __name__ == '__main__':
    app.run_server(debug=False)