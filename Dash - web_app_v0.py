import pandas as pd
# import numpy as np
# import chart_studio.plotly as py
import cufflinks as cf
# import seaborn as sns

# import yfinance as yf
import plotly.express as px
# %matplotlib inline
# import talib as ta
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime as dt
# import talib as ta
import ta

cf.go_offline()


## carregar dados
prices_indice_temp1 = pd.read_csv("prices_indice.csv") # evolução do índice 
pa_segmentos = pd.read_csv("ranking_segmento.csv") # ranking dos segmentos
pa_long_segmentos = pd.read_csv("pa_long_segmentos.csv") # evolução do retorno dos segmentos
pa_long = pd.read_csv("price_action_tabelao.csv") 

# dados auxiliares
pa_long = pa_long.sort_values(by=['ranking_ativo'],ascending=True)
acoes_lista = pa_long['ativo'].unique()
segmentos_lista = pa_segmentos['segmento'] # lista dos segmentos
pa_segmentos = pa_segmentos.round(decimals=1)
pa_long_segmentos = pa_long_segmentos.round(decimals=1) # dataframe da evolução dos retornos dos segmentos
pa_long_segmentos = pa_long_segmentos.sort_values('data')
pa_long = pa_long.round(1)
pa_long = pa_long.sort_values('data')
prices_temp3 = pd.read_csv("prices_long_holc.csv") 
prices_temp3 = prices_temp3.sort_values('Date')
ativos_lista = prices_temp3['ativo'].unique()


### Dash

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container([

    dbc.Row(
            dbc.Col(html.H1("Painel Price Action",
                        className='text-center text-primary mb-4'),
                    width=12)
            ),

    dbc.Row([

    
        dbc.Col([
# evolução do índice  
                    html.H2(children = 'Evolução do Índice',
                            style = {
                                'text-align': 'center',
                                'color':'#456FBV'
                                } 
                            ),            

                      dcc.DatePickerRange(
                       id='DatePickerRange',  # ID to be used for callback
                       end_date_placeholder_text="Return",  # text that appears when no end date chosen
                       with_portal=False,  # if True calendar will open in a full screen overlay portal
                       first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                       reopen_calendar_on_clear=True,
                       is_RTL=False,  # True or False for direction of calendar
                       clearable=True,  # whether or not the user can clear the dropdown
                       number_of_months_shown=1,  # number of months shown when calendar is open
                       # min_date_allowed=dt(2018, 1, 1),  # minimum date allowed on the DatePickerRange component
                       # max_date_allowed=dt(2020, 6, 20),  # maximum date allowed on the DatePickerRange component
                       # initial_visible_month=dt(2020, 5, 1),  # the month initially presented when the user opens the calendar
                       start_date=dt(2020, 11, 3).date(),
                       end_date=dt(2021, 2, 9).date(),
                       display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
                       month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                       minimum_nights=2,  # minimum number of days between start and end date
                       persistence=True,
                       persisted_props=['start_date'],
                       persistence_type='session',  # session, local, or memory. Default is 'local'
                       updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered                       
                       ) ,     

                    dcc.Graph(id='indice'),

                ], width={'size':5, 'offset':1, 'order':1},
                   # xs=12, sm=12, md=12, lg=5, xl=5
                
                ),  
        
        dbc.Col([
# Retorno por segmentos (gráfico de barras)   
                    html.H2(children = 'Retornos por segmentos',
                            style = {
                                'text-align': 'center',
                                'color':'#456FBV'
                                } 
                            ),            

                    dcc.Dropdown(id='dropdown_segmento_barra', options=[  
                        {'label': i, 'value': i} for i in segmentos_lista ## list of unique segments
                        ],
                        value=segmentos_lista[0],
                        multi=True, placeholder='Filtrar por segmentos...'), 

                    dbc.Col(dcc.Graph(id='retorno-segmentos'))
        
        
               ], width={'size':5, 'offset':1, 'order':1},
                   # xs=12, sm=12, md=12, lg=5, xl=5
                
                ),    
        
        ], no_gutters=True, justify='start'),  # Horizontal:start,center,end,between,around

    dbc.Row([
    
        dbc.Col([

                html.H2(children = 'Ativos por Segmentos',
                        style = {
                                'text-align': 'center',
                                'color':'#456FBV'
                                } 
                        ),
      
                        dcc.Dropdown(id='dropdown_ativos_segmentos', options=[  
                        {'label': i, 'value': i} for i in segmentos_lista ## list of unique segments
                        ],
                            value=segmentos_lista[0],
                            multi=True, placeholder='Filtrar por segmentos...'), 
          
                        dbc.Col(dcc.Graph(id='retorno_ativos_segmentos')),                      
        
               ], width={'size':5, 'offset':1, 'order':1},
                   # xs=12, sm=12, md=12, lg=5, xl=5            
                
                ),  
        
        dbc.Col([

                ## Price Action: seleção de ativos

                html.H2(children = 'Seleção de ativos',
                        style = {
                            'text-align': 'center',
                            'color':'#456FBV'
                            } 
                        ),
    
                dcc.Dropdown(id='dropdown_selecao_ativos', options=[  
                    {'label': i, 'value': i} for i in acoes_lista ## list of unique segments
                    ],
                    value=acoes_lista[0],
                    multi=True, placeholder='Filtrar por ativo...'), 
          
                dbc.Col(dcc.Graph(id='retorno_selecao_ativos')),    

                ], width={'size':5, 'offset':1, 'order':1},
                   # xs=12, sm=12, md=12, lg=5, xl=5
                
                ),    
        
        ], no_gutters=True, justify='start'),  # Horizontal:start,center,end,between,around

    dbc.Row([
    
        dbc.Col([

                html.H2(children = 'Candle por ativo',
                        style = {
                                'text-align': 'center',
                                'color':'#456FBV'
                                } 
                        ),
      
                    dcc.Dropdown(id='dropdown_candle', options=[  
                        {'label': i, 'value': i} for i in ativos_lista ## list of unique segments
                        ],
                        value='WEGE3',
                        multi=True, placeholder='Filtrar por ...'), 
                        
 
                    dbc.Col(dcc.Graph(id='candle_ativo')), 
                
        
               ], width={'size':5, 'offset':1, 'order':1},
                   # xs=12, sm=12, md=12, lg=5, xl=5            
                
                )
                
        ], no_gutters=True, justify='start'),  # Horizontal:start,center,end,between,around

          
], fluid=True)


# Evolução do Índice
@app.callback(
    dash.dependencies.Output('indice', 'figure'),
    [dash.dependencies.Input('DatePickerRange', 'start_date'),
      dash.dependencies.Input('DatePickerRange', 'end_date')])

def update_graph(start_date, end_date):

    prices_indice = prices_indice_temp1[(prices_indice_temp1['Date'] >= start_date) & (prices_indice_temp1['Date'] <= end_date)]
    # print(dff[:5])

    fig = go.Figure(data=[go.Candlestick(x=prices_indice['Date'],
                open=prices_indice['Open'],
                high=prices_indice['High'],
                low=prices_indice['Low'],
                close=prices_indice['Adj Close'],
                name= 'Preço Ajustado')])

    fig.add_trace(go.Scatter(x=prices_indice['Date'],
                y=prices_indice['ema_7'],
                    mode='lines',
                    line = dict(color='purple', width=4, dash='dash'),
                    name='EMA 7 dias'))

    fig.add_trace(go.Scatter(x=prices_indice['Date'],
                y=prices_indice['ema_21'],
                    mode='lines',
                    line = dict(color='black', width=4, dash='dash'),
                    name='EMA 21 dias'))
    return fig

## segmento barra    
@app.callback(dash.dependencies.Output('retorno-segmentos', 'figure'),
              dash.dependencies.Input('dropdown_segmento_barra', 'value'))

def update_graph(value_segmento_barra):
    

    if type(value_segmento_barra)!=str:
        price_action_segmentos = pa_segmentos[pa_segmentos['segmento'].isin(value_segmento_barra) ]
    else:
        price_action_segmentos = pa_segmentos[pa_segmentos['segmento']==value_segmento_barra]

    fig_pa_segmentos = px.bar(price_action_segmentos, x='segmento', y='retorno_ult_segmento', color='segmento')
    
    return fig_pa_segmentos



# Price Action: Seleção de Ativos por Segmentos
@app.callback(dash.dependencies.Output('retorno_ativos_segmentos', 'figure'),
              dash.dependencies.Input('dropdown_ativos_segmentos', 'value'))


def update_graph(value_segmento_ativos):
    if type(value_segmento_ativos)!=str:
        pa_ativos_segmentos = pa_long[pa_long['segmento'].isin(value_segmento_ativos) ]
    else:
        pa_ativos_segmentos = pa_long[pa_long['segmento']==value_segmento_ativos]
    
    fig_pa_ativos_segmentos = px.line(pa_ativos_segmentos,x='data', y='rentabilidade', color='ativo')
    
    return fig_pa_ativos_segmentos


## Price Action: Seleção de Ativos
@app.callback(dash.dependencies.Output('retorno_selecao_ativos', 'figure'),
              dash.dependencies.Input('dropdown_selecao_ativos', 'value'))

def update_graph(value_selecao_ativos):

    if type(value_selecao_ativos)!=str:
        price_action_segmentos_ativos = pa_long[pa_long['ativo'].isin(value_selecao_ativos) ]
    else:
        price_action_segmentos_ativos = pa_long[pa_long['ativo']==value_selecao_ativos]
    
    fig_pa_segmentos_ativos = px.line(price_action_segmentos_ativos,x='data', y='rentabilidade', color='ativo')
    
    return fig_pa_segmentos_ativos
    
## Candle por ativo
@app.callback(dash.dependencies.Output('candle_ativo', 'figure'),
              dash.dependencies.Input('dropdown_candle', 'value'))    

def update_graph(value_candle_ativo):
    
    if type(value_candle_ativo)!=str:
        candle_ativo = prices_temp3[prices_temp3['ativo'].isin(value_candle_ativo) ]
        # candle_ativo['ema_21'] = ta.EMA(candle_ativo['Adj Close'],21) # média móvel exponencial de 21 dias
        # candle_ativo['ema_7'] = ta.EMA(candle_ativo['Adj Close'],7) # média móvel exponencial de 7 dias
    else:
        candle_ativo = prices_temp3[prices_temp3['ativo']==value_candle_ativo]        
        # candle_ativo['ema_21'] = ta.EMA(candle_ativo['Adj Close'],21) # média móvel exponencial de 21 dias
        # candle_ativo['ema_7'] = ta.EMA(candle_ativo['Adj Close'],7) # média móvel exponencial de 7 dias
    
    fig = go.Figure(data=[go.Candlestick(x=candle_ativo['Date'],
                open=candle_ativo['Open'],
                high=candle_ativo['High'],
                low=candle_ativo['Low'],
                close=candle_ativo['Adj Close'],
                name='Preço Ajustado'),])
    
    # fig.add_trace(go.Scatter(x=candle_ativo['Date'],
    #             y=candle_ativo['ema_7'],
    #                 mode='lines',
    #                 line = dict(color='purple', width=4, dash='dash'),
    #                 name='EMA 7 dias'))

    # fig.add_trace(go.Scatter(x=candle_ativo['Date'],
    #             y=candle_ativo['ema_21'],
    #                 mode='lines',
    #                 line = dict(color='black', width=4, dash='dash'),
    #                 name='EMA 21 dias'))
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, port=8053)

