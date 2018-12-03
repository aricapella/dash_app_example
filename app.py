import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('DataProject3.csv')

available_indicators = df['NA_ITEM'].unique()
available_countries=df['GEO'].unique()
title2= 'Graph'
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Markdown('''## First exercise:
            
            '''),

            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Gross domestic product at market prices'
                ),
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                ),
            ],
            style={'width': '40%', 'display': 'inline-block','margin-bottom' : '30px'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Gross domestic product at market prices'
                ),
                dcc.RadioItems(
                    id='yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],style={'width': '48%', 'float': 'right', 'display': 'inline-block','margin-bottom' : '30px'})
        ]),

        dcc.Graph(id='indicator-graphic'),

        dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()}
        ),
        
        dcc.Markdown('''## Second exercise:
        
        '''),
    ]), 

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='geo-dropdown',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Belgium'
            ),
        ],style={'width': '40%', 'display': 'inline-block','margin-bottom' : '30px'}),

        html.Div([
            dcc.Dropdown(
                id='indi-dropdown',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
        ],style={'width': '40%', 'float': 'right', 'display': 'inline-block','margin-bottom' : '30px'}),

        dcc.Graph(id='country-graphic')

    ]) 
    
    
]) 

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff1 = df[df['UNIT']=='Current prices, million euro']
    dff = dff1[dff1['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 70 , 'b': 50, 't': 50, 'r': 0, 'autoexpand':True},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('country-graphic','figure'),
    [dash.dependencies.Input('geo-dropdown','value'),
     dash.dependencies.Input('indi-dropdown','value')])

def update_graph2(geo_dropdown_name,indi_dropdown_name):
    dff_1 = df[df['UNIT']=='Current prices, million euro']
    dff_2 = dff_1[dff_1['GEO'] == geo_dropdown_name]
    
    return {
        'data': [go.Scatter(
            x=dff_2['TIME'].unique(),
            y=dff_2[dff_2['NA_ITEM'] == indi_dropdown_name]['Value'],
            text=dff_2[dff_2['NA_ITEM'] == indi_dropdown_name]['TIME'],
            mode='lines',
        )],
        'layout': go.Layout(
            title=title2,
            autosize=True,
            xaxis={
                'title': 'Year'
            },
            yaxis={
                'title':indi_dropdown_name
            },
            margin={'l': 70 , 'b': 50, 't': 50, 'r': 0, 'autoexpand':True},
            hovermode='closest'
        )
    }
if __name__ == '__main__':
    app.run_server()
    