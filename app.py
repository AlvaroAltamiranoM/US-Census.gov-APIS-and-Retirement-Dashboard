# -*- coding: utf-8 -*-
"""
Created on Sat Jun 8 20:38:30 2022
@author: unily
"""
import dash
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc   
import plotly.graph_objects as go
from urllib.request import urlopen
import json


######################
#       APP          #
######################


#FIPS
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


indicators = ['Share of population 65+ (%)', 'Population 65+',
              'Share of population 85+ (%)', 'Population 85+',
              'People 65+ living below poverty (%)','People 65+ living below poverty',
              'Employment at 65-74 (%)','Employment at 75+ (%)',
              'People 60+ with retirement income (%)','People 60+ with social security income (%)']

breakdown = ['Total','Sex: Men', 'Sex: Women',
              'Race: White', 'Race: Black']



df_table_s = pd.read_csv('table_state.csv', index_col=0)


################
### DASH APP ###    
################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN],
                meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.8,'}])
server = app.server

#Dash tab styles
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '20px',
    'fontWeight': 'bold',
    'color': '#1f77b4'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1f77b4',
    'color': 'white',
    'padding': '20px'
}

app.title = 'CRI-states' 

app.layout = html.Div([

        dbc.Row(children = [dbc.Col(
                        html.H2('Demographic & Retirement Statistics',
                                style={'color':'black'}),
                        width={'size': '7'},
                        lg={'size': '6'}),
                dbc.Col(children= [
                        dbc.CardImg(src="/assets/logo.jpg", 
                        top=True, style={"width": "5rem"}),
                        ], width={'size': '2', 'offset': '3'},
                        lg={'size': '2', 'offset': '4'}),
                        ]),                      
        html.H4(children='Based on census.gov data',
        style={'textAlign': 'left', 'marginTop': '0.1em', 'marginBottom': '1em', 'color': '#1f77b4'},
                ),
    dcc.Tabs([
    dcc.Tab(label='State maps', style=tab_style, selected_style=tab_selected_style,
            children=[
                html.Div([html.P("Select an indicator:",
                 style={'marginTop': '2em','marginBottom': '1em', "font-weight": "bold",
                        'display': 'inline-block'}),
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in indicators],
                    placeholder='Select an indicator',
                    value = 'Share of population 65+ (%)',
                    multi = False),
                    ],
                    style={'marginTop': '1em','marginBottom': '4em',
                            'display': 'inline-block', 'width': '48%'},
                          ),
                html.Div([html.P("Breakdown by:",
                 style={'marginTop': '2em','marginBottom': '1em', "font-weight": "bold",
                        'display': 'inline-block'}),       
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in breakdown],
                    placeholder='Select a group',
                    value = 'Total',
                    multi = False)
                    ],
                    style={'marginTop': '1em','marginBottom': '4em',
                            'display': 'inline-block', 'width': '48%'},
                          ),
                dcc.Loading(
                    id="loading-1",
                    children=[html.Div([html.Div(id="loading-output-1"),
                    dbc.Row([
                            dbc.Col(dcc.Graph(id='graph1',
                                    style={"displaylogo": False},
                                  config = {'displaylogo': False,
                                             'modeBarButtonsToRemove': ['toImage']},
                                  ),
                                  width={'size': '12', 'offset': '0'},
                                lg={'size': '12', 'offset': '0'}
                                ),
                ]),
            ]),
                      ], type="circle",
            ),
        ]),

    dcc.Tab(label='States summary table', style=tab_style, selected_style=tab_selected_style,
        children=[
            dcc.Loading(
                id="loading-3",
                children=[html.Div([html.Div(id="loading-output-3"),
        dbc.Row(children = [dbc.Col(dash_table.DataTable(
            id = 'StatesTable',
            columns=[ {'id': c, 'name' : c} for c in df_table_s.columns if c not in ['Unnamed:0']],
            style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
            },
        data=df_table_s.to_dict('records'),
            sort_action="native",
            sort_mode="multi",
            row_deletable= False,
            style_as_list_view=True,
            style_cell={'padding': '5px','textAlign': 'center',
                        'height': 'auto',
                        'whiteSpace': 'normal'},
            style_header={
                'fontWeight': 'normal',
                'color': 'white',
                'backgroundColor': 'black',
                'height': 45
                },
            style_table = { 'marginTop': '2em','marginBottom': '1em'} ,
                style_cell_conditional=[
                    {'if': {'column_id': ['Fund\'s name', 'Sector']},
                        'textAlign': 'left'
                        },
                    ],
               
            ),
                width={'size': 'auto'}, 
                lg={'size': '12'}
            ),

            ]),
        ]),
                  ], type="circle",
        ),
    ]),        

    ]),
        
    html.Div(["This project was developed in Python. The code for the APIs calls and the Dashboard is ", html.A("here.",
                    href='https://github.com/AlvaroAltamiranoM/US-Census.gov-APIS-and-Retirement-Dashboard', target="_blank"),' A one-pager definition of the indicators can be downloaded '
              , html.A("here.",
                    href='https://github.com/AlvaroAltamiranoM/US-Census.gov-APIS-and-Retirement-Dashboard/blob/main/Definitions%20of%20indicators.pdf', target="_blank")
              ], style={'marginTop': '6em',
                                'marginBottom': '1em','display': 'block',
                                'borderTop': '1px solid #d6d6d6',
                                'borderBottom': '1px solid #d6d6d6',
                                'backgroundColor': '#1f77a1',
                                'color': 'white',
                                'padding': '10px'})
            
    ],
    style={'object-fit': 'contain', 
    'height':'Auto', 'width': '100wv',
     'padding':'30px 30px 30px 30px'}
    )
    

#################################
# CALLBACKS
#################################
#State-level graph's callbacks
@app.callback(
    Output('graph1', 'figure'),
    [Input('xaxis-column', 'value')],
    Input('yaxis-column', 'value'))

def update_graph1(xaxis_column_name, yaxis_column_name):
        
    if xaxis_column_name == 'Share of population 65+ (%)' and yaxis_column_name == 'Total':
        df_s = pd.read_csv('pop_states.csv')
           
        fig2 = go.Figure(data = go.Choropleth(
        locations = df_s['states'], # Spatial coordinates
        z = df_s['%65+'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Blues',
        colorbar_title = "Share of population 65+ (%)",
        autocolorscale=False,
        text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
            'Percent of the population aged 65 and older: ' + df_s['%65+'].astype(str) +'%'
            ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )
        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 16.9%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2
    
    if xaxis_column_name == 'Share of population 65+ (%)' and yaxis_column_name == 'Sex: Men':
        
        df_s = pd.read_csv('pop_states_sex_men.csv')

        fig2 = go.Figure(data = go.Choropleth(
        locations = df_s['states'], # Spatial coordinates
        z = df_s['%65+'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Blues',
        colorbar_title = "Share of men 65+ (%)",
        autocolorscale=False,
        text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
            'Percent of the male population aged 65 and older: ' + df_s['%65+'].astype(str) +'%'
            ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )
        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 15.4%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2

    if xaxis_column_name == 'Share of population 65+ (%)' and yaxis_column_name == 'Sex: Women':
        df_s = pd.read_csv('pop_states_sex_women.csv')

        fig2 = go.Figure(data = go.Choropleth(
        locations = df_s['states'], # Spatial coordinates
        z = df_s['%65+'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Blues',
        colorbar_title = "Share of female 65+ (%)",
        autocolorscale=False,
        text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
            'Percent of the female population aged 65 and older: ' + df_s['%65+'].astype(str) +'%'
            ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )
        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 18.5%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2

    if xaxis_column_name == 'Population 65+' and yaxis_column_name == 'Total':
        df_s = pd.read_csv('pop_states.csv')

        fig2 = go.Figure(data = go.Choropleth(
                            locations = df_s['states'], # Spatial coordinates
                            z = df_s['26'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Blues',
                            autocolorscale=False,
                            colorbar_title = "Population 65+",
                            text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
                                'Total population aged 65 and older: ' + df_s['26'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 54 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2

    if xaxis_column_name == 'Population 65+' and yaxis_column_name == 'Sex: Men':
        df_s = pd.read_csv('pop_states_sex_men.csv')

        fig2 = go.Figure(data = go.Choropleth(
                            locations = df_s['states'], # Spatial coordinates
                            z = df_s['26'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Blues',
                            autocolorscale=False,
                            colorbar_title = "Male population 65+",
                            text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
                                'Total male population aged 65 and older: ' + df_s['26'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 24 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2

    if xaxis_column_name == 'Population 65+' and yaxis_column_name == 'Sex: Women':
        df_s = pd.read_csv('pop_states_sex_women.csv')

        fig2 = go.Figure(data = go.Choropleth(
                            locations = df_s['states'], # Spatial coordinates
                            z = df_s['26'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Blues',
                            autocolorscale=False,
                            colorbar_title = "Female population 65+",
                            text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
                                'Total female population aged 65 and older: ' + df_s['26'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 30 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2
    
    if xaxis_column_name == 'Share of population 85+ (%)' and yaxis_column_name == 'Total':
        df_s = pd.read_csv('pop_states.csv')

        fig2 = go.Figure(data = go.Choropleth(
        locations = df_s['states'], # Spatial coordinates
        z = df_s['%85+'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Share of population 85+ (%)",
        autocolorscale=False,
        text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
            'Percent of the population aged 85 and older: ' + df_s['%85+'].astype(str) +'%'
            ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average: 2%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2
    
    if xaxis_column_name == 'Share of population 85+ (%)' and yaxis_column_name == 'Sex: Men':
        df_s = pd.read_csv('pop_states_sex_men.csv')

        fig2 = go.Figure(data = go.Choropleth(
        locations = df_s['states'], # Spatial coordinates
        z = df_s['%85+'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Share of the male population 85+ (%)",
        autocolorscale=False,
        text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
            'Percent of the male population aged 85 and older: ' + df_s['%85+'].astype(str) +'%'
            ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average: 1.4%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2

    if xaxis_column_name == 'Share of population 85+ (%)' and yaxis_column_name == 'Sex: Women':
        df_s = pd.read_csv('pop_states_sex_women.csv')

        fig2 = go.Figure(data = go.Choropleth(
        locations = df_s['states'], # Spatial coordinates
        z = df_s['%85+'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Share of the female population 85+ (%)",
        autocolorscale=False,
        text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
            'Percent of the female population aged 85 and older: ' + df_s['%85+'].astype(str) +'%'
            ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average: 2.5%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2
    
    
    if xaxis_column_name == 'Population 85+' and yaxis_column_name == 'Total':
        df_s = pd.read_csv('pop_states.csv')

        fig2 = go.Figure(data = go.Choropleth(
                            locations = df_s['states'], # Spatial coordinates
                            z = df_s['27'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Reds',
                            autocolorscale=False,
                            colorbar_title = "Population 85+",
                            text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
                                'Total population aged 85 and older: ' + df_s['27'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 6.4 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2
    
    if xaxis_column_name == 'Population 85+' and yaxis_column_name == 'Sex: Men':
        df_s = pd.read_csv('pop_states_sex_men.csv')

        fig2 = go.Figure(data = go.Choropleth(
                            locations = df_s['states'], # Spatial coordinates
                            z = df_s['27'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Reds',
                            autocolorscale=False,
                            colorbar_title = "Male population 85+",
                            text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
                                'Total male population aged 85 and older: ' + df_s['27'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 2.3 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2

    if xaxis_column_name == 'Population 85+' and yaxis_column_name == 'Sex: Women':
        df_s = pd.read_csv('pop_states_sex_women.csv')

        fig2 = go.Figure(data = go.Choropleth(
                            locations = df_s['states'], # Spatial coordinates
                            z = df_s['27'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Reds',
                            autocolorscale=False,
                            colorbar_title = "Female population 85+",
                            text = df_s['NAME'] + ' (year: 2019)' + '<br>' + \
                                'Total female population aged 85 and older: ' + df_s['27'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 4.1 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2


    if xaxis_column_name == 'People 65+ living below poverty (%)' and yaxis_column_name == 'Total':
        table_p_s = pd.read_csv('poverty_state.csv', index_col=0,encoding="utf-8",
         dtype={'Percent_Poor': 'float64', 'Below_poverty': 'int32', 'states': 'str' })
        
        fig2 = go.Figure(data = go.Choropleth(
        locations = table_p_s['states'], # Spatial coordinates
        z = table_p_s['Percent_Poor'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Percent of People 65+ living below poverty (%)",
        autocolorscale=False,
        text = table_p_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of people aged 65 and older'+ '<br>' +'living below the federal poverty line: ' + table_p_s['Percent_Poor'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 8.9%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2
    
    if xaxis_column_name == 'People 65+ living below poverty (%)' and yaxis_column_name == 'Sex: Men':
        table_p_s = pd.read_csv('poverty_state_men.csv', index_col=0,encoding="utf-8",
         dtype={'Percent_Poor': 'float64', 'Below_poverty': 'int32', 'states': 'str' })

        fig2 = go.Figure(data = go.Choropleth(
        locations = table_p_s['states'], # Spatial coordinates
        z = table_p_s['Percent_Poor'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Percent of men 65+ living below poverty (%)",
        autocolorscale=False,
        text = table_p_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of men aged 65 and older'+ '<br>' +'living below the federal poverty line: ' + table_p_s['Percent_Poor'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 7.3%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2

    if xaxis_column_name == 'People 65+ living below poverty (%)' and yaxis_column_name == 'Sex: Women':
        table_p_s = pd.read_csv('poverty_state_women.csv', index_col=0,encoding="utf-8",
         dtype={'Percent_Poor': 'float64', 'Below_poverty': 'int32', 'states': 'str' })
        
        fig2 = go.Figure(data = go.Choropleth(
        locations = table_p_s['states'], # Spatial coordinates
        z = table_p_s['Percent_Poor'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Percent of women 65+ living below poverty (%)",
        autocolorscale=False,
        text = table_p_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of women aged 65 and older'+ '<br>' +'living below the federal poverty line: ' + table_p_s['Percent_Poor'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 10.3%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2
    
    if xaxis_column_name == 'People 65+ living below poverty' and yaxis_column_name == 'Total':
        table_p_s = pd.read_csv('poverty_state.csv', index_col=0,encoding="utf-8",
                               dtype={'Percent_Poor': 'float64', 'Below_poverty': 'int32', 'states': 'str' })

        fig2 = go.Figure(data = go.Choropleth(
                            locations = table_p_s['states'], # Spatial coordinates
                            z = table_p_s['Below_poverty'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Reds',
                            autocolorscale=False,
                            colorbar_title = "People 65+ living below poverty",
                            text = table_p_s.index.values + ' (year: 2019)' + '<br>' + \
                                'People aged 65 and older'+ '<br>' +'living below the federal poverty line: ' + table_p_s['Below_poverty'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 5 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2

    if xaxis_column_name == 'People 65+ living below poverty' and yaxis_column_name == 'Sex: Men':
        table_p_s = pd.read_csv('poverty_state_men.csv', index_col=0,encoding="utf-8",
                               dtype={'Percent_Poor': 'float64', 'Below_poverty': 'int32', 'states': 'str' })

        fig2 = go.Figure(data = go.Choropleth(
                            locations = table_p_s['states'], # Spatial coordinates
                            z = table_p_s['Below_poverty'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Reds',
                            autocolorscale=False,
                            colorbar_title = "Men 65+ living below poverty",
                            text = table_p_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Men aged 65 and older'+ '<br>' +'living below the federal poverty line: ' + table_p_s['Below_poverty'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 1.8 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2


    if xaxis_column_name == 'People 65+ living below poverty' and yaxis_column_name == 'Sex: Women':
        table_p_s = pd.read_csv('poverty_state_women.csv', index_col=0,encoding="utf-8",
                               dtype={'Percent_Poor': 'float64', 'Below_poverty': 'int32', 'states': 'str' })

        fig2 = go.Figure(data = go.Choropleth(
                            locations = table_p_s['states'], # Spatial coordinates
                            z = table_p_s['Below_poverty'].astype(int), # Data to be color-coded
                            locationmode = 'USA-states', # set of locations match entries in `locations`
                            colorscale = 'Reds',
                            autocolorscale=False,
                            colorbar_title = "Women 65+ living below poverty",
                            text = table_p_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Women aged 65 and older'+ '<br>' +'living below the federal poverty line: ' + table_p_s['Below_poverty'].astype(str)
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                           title_text = 'National Total in 2019: 3 M',                
                          title_font_color="black",
                          title_font_size=18, legend_title_font_color="black",
                          title={'x':0.4,'xanchor':'center'}
                                 )

        return fig2


    if xaxis_column_name == 'Employment at 65-74 (%)' and yaxis_column_name == 'Total':
        table_emp_s = pd.read_csv('emp_state.csv', index_col=0,encoding="utf-8",
         dtype={'Employed_65_74': 'float64', 'states': 'str' })
        
        fig2 = go.Figure(data = go.Choropleth(
        locations = table_emp_s['states'], # Spatial coordinates
        z = table_emp_s['Employed_65_74'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "Employment at 65-74 (%)",
        autocolorscale=False,
        text = table_emp_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of people aged 65-74 employed: ' + table_emp_s['Employed_65_74'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 26.8%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2

    if xaxis_column_name == 'Employment at 65-74 (%)' and yaxis_column_name == 'Sex: Men':
        table_emp_s = pd.read_csv('emp_state_men.csv', index_col=0,encoding="utf-8",
         dtype={'Employed_65_74': 'float64', 'states': 'str' })
        
        fig2 = go.Figure(data = go.Choropleth(
        locations = table_emp_s['states'], # Spatial coordinates
        z = table_emp_s['Employed_65_74'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "Male employment at 65-74 (%)",
        autocolorscale=False,
        text = table_emp_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of men aged 65-74 employed: ' + table_emp_s['Employed_65_74'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 30.7%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2


    if xaxis_column_name == 'Employment at 65-74 (%)' and yaxis_column_name == 'Sex: Women':
        table_emp_s = pd.read_csv('emp_state_women.csv', index_col=0,encoding="utf-8",
         dtype={'Employed_65_74': 'float64', 'states': 'str' })
        
        fig2 = go.Figure(data = go.Choropleth(
        locations = table_emp_s['states'], # Spatial coordinates
        z = table_emp_s['Employed_65_74'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "Female employment at 65-74 (%)",
        autocolorscale=False,
        text = table_emp_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of women aged 65-74 employed: ' + table_emp_s['Employed_65_74'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average in 2019: 23%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2


    if xaxis_column_name == 'Employment at 75+ (%)' and yaxis_column_name == 'Total':
        table_emp_s = pd.read_csv('emp_state.csv', index_col=0,encoding="utf-8",
         dtype={'Employed_75+': 'float64', 'states': 'str' })
        

        fig2 = go.Figure(data = go.Choropleth(
        locations = table_emp_s['states'], # Spatial coordinates
        z = table_emp_s['Employed_75+'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "Employment at 75+ (%)",
        autocolorscale=False,
        text = table_emp_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of people aged 75+ employed: ' + table_emp_s['Employed_75+'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average: 7%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2
    

    if xaxis_column_name == 'Employment at 75+ (%)' and yaxis_column_name == 'Sex: Men':
        table_emp_s = pd.read_csv('emp_state_men.csv', index_col=0,encoding="utf-8",
         dtype={'Employed_75+': 'float64', 'states': 'str' })
        

        fig2 = go.Figure(data = go.Choropleth(
        locations = table_emp_s['states'], # Spatial coordinates
        z = table_emp_s['Employed_75+'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "Male employment at 75+ (%)",
        autocolorscale=False,
        text = table_emp_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of men aged 75+ employed: ' + table_emp_s['Employed_75+'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average: 10.2%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2


    if xaxis_column_name == 'Employment at 75+ (%)' and yaxis_column_name == 'Sex: Women':
        table_emp_s = pd.read_csv('emp_state_women.csv', index_col=0,encoding="utf-8",
         dtype={'Employed_75+': 'float64', 'states': 'str' })
        

        fig2 = go.Figure(data = go.Choropleth(
        locations = table_emp_s['states'], # Spatial coordinates
        z = table_emp_s['Employed_75+'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "Female employment at 75+ (%)",
        autocolorscale=False,
        text = table_emp_s.index.values + ' (year: 2019)' + '<br>' + \
                                'Percent of women aged 75+ employed: ' + table_emp_s['Employed_75+'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average: 5.2%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2


    if xaxis_column_name == 'People 60+ with retirement income (%)' and yaxis_column_name == 'Total':
        table_retir_s = pd.read_csv('retir_state.csv', index_col=0,encoding="utf-8",
         dtype={'Retirement_income': 'float64', 'states': 'str' })
        

        fig2 = go.Figure(data = go.Choropleth(
        locations = table_retir_s['states'], # Spatial coordinates
        z = table_retir_s['Retirement_income'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "People 60+ with retirement income (%)",
        autocolorscale=False,
        text = table_retir_s.index.values + ' (year: 2019)' + '<br>' + \
                                'People 60+ with retirement income: ' + table_retir_s['Retirement_income'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average: 52.2%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2
        

    if xaxis_column_name == 'People 60+ with social security income (%)' and yaxis_column_name == 'Total':
        table_retir_s = pd.read_csv('retir_state.csv', index_col=0,encoding="utf-8",
         dtype={'Social_security': 'float64', 'states': 'str' })
        

        fig2 = go.Figure(data = go.Choropleth(
        locations = table_retir_s['states'], # Spatial coordinates
        z = table_retir_s['Social_security'].astype(int), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "'People 60+ with social security income (%)'",
        autocolorscale=False,
        text = table_retir_s.index.values + ' (year: 2019)' + '<br>' + \
                                'People 60+ with retirement income: ' + table_retir_s['Social_security'].astype(str)+'%'
                                    ))
            
        fig2.update_traces(
               hovertemplate=" %{text}<br><extra></extra>"
              )

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'National Average: 74.8%',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.4,'xanchor':'center'}
                                   )

        return fig2

#Unavailable data graph's callbacks

    if xaxis_column_name == 'People 60+ with retirement income (%)' and yaxis_column_name == 'Sex: Men':
        fig2 = go.Figure(data = go.Choropleth(
        locations = [], # Spatial coordinates
        z = [], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "''",
        autocolorscale=False,
        )) 

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'This breakdown is not available',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.5,'xanchor':'center'}
                                   )
        return fig2

    if xaxis_column_name == 'People 60+ with retirement income (%)' and yaxis_column_name == 'Sex: Women':
        fig2 = go.Figure(data = go.Choropleth(
        locations = [], # Spatial coordinates
        z = [], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "''",
        autocolorscale=False,
        )) 

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'This breakdown is not available',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.5,'xanchor':'center'}
                                   )
        return fig2

    if xaxis_column_name == 'People 60+ with social security income (%)'  and yaxis_column_name == 'Sex: Men':
        fig2 = go.Figure(data = go.Choropleth(
        locations = [], # Spatial coordinates
        z = [], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "''",
        autocolorscale=False,
        )) 

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'This breakdown is not available',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.5,'xanchor':'center'}
                                   )
        return fig2

    if xaxis_column_name == 'People 60+ with social security income (%)'  and yaxis_column_name == 'Sex: Women':
        fig2 = go.Figure(data = go.Choropleth(
        locations = [], # Spatial coordinates
        z = [], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Greens',
        colorbar_title = "''",
        autocolorscale=False,
        )) 

        fig2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        fig2.update_layout(geo_scope='usa',
                            title_text = 'This breakdown is not available',                
                            title_font_color="black",
                            title_font_size=18, legend_title_font_color="black",
                            title={'x':0.5,'xanchor':'center'}
                                   )
        return fig2



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, threaded=True)
