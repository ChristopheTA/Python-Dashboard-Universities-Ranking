import pandas as pd
from os import makedirs
from dash.dcc.Interval import Interval
import plotly_express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import callback_context
import folium

df1= pd.read_csv('Data_Projet/country-coordinates-world.csv',na_values=["-"])
df2= pd.read_csv('Data_Projet/timesData.csv', na_values=["-"])

df1= df1.rename(columns = {"Country" : "country"})

data_proj=pd.merge(df1,df2)
data_proj=data_proj

dfc = data_proj.groupby(by = ["country"])["country"].count().to_frame("count")
#print(dfc)
col=list(data_proj.columns)
col_names=col[5:10]
teaching=data_proj[col[5]]
international=data_proj[col[6]]
research=data_proj[col[7]]
citations=data_proj[col[8]]
income=data_proj[col[9]]
type_proj=[teaching, international, research, citations, income]

info="teaching"
 #data_proj["latitude"],data_proj["longitude"]
coords=(46.539758, 2.430331)
my_map = folium.Map(location=coords,tiles='OpenStreetMap', zoom_start=6)
my_map.save('map_alpha.html')
year=2011
years=data_proj["year"].unique()
data_year={ year:data_proj.query("year == @year") for year in years}



if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    fig = px.histogram(data_year[year],x='teaching') # (4)


    app.layout = html.Div(children=[
                            html.H1(id = "titre", children=f'University {info} rating',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            html.Label("Type"),
                            
                            dcc.Dropdown(
                                id="type-dropdown",
                                options=[ {'label': i, 'value': i} for i in col_names
                                   ],
                                value=col_names[0],
                            ),

                            html.Label('Year'),
                            
                            dcc.Slider(
                                id="year-slider",
                                min=2011,
                                max=2016,
                                marks={
                                    2011:{'label': '2011'},#, 'value': 1952},
                                    2012:{'label': '2012'},#, 'value': 1957},
                                    2013:{'label': '2013'},#, 'value': 1962},
                                    2014:{'label': '2014'},#, 'value': 1967},
                                    2015:{'label': '2015'},#, 'value': 1972},
                                    2016:{'label': '2016'},#, 'value': 1977},
                                },
                                value=2011,
                            ),
                            
                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

                            html.Button(
                                'Play', 
                                id='Play', 
                                n_clicks=0
                            ),
                            html.Button(
                                'Pause', 
                                id='Pause', 
                                n_clicks=0
                            ),
                            html.Div(id='button'),

                            html.H2('World Map Alpha'),
                            html.Iframe(id='map', srcDoc=open('map_alpha.html','r').read(),width='100%',height='500'),
                            
                            dcc.Interval(id='interval',
                                interval=2*1000, # in milliseconds
                                n_intervals=0,
                                #disabled=True
                            ),
                            
                ]
    )
@app.callback(
        Output(component_id='graph1', component_property='figure'), # (1)
        [Input(component_id='year-slider', component_property='value'),
        Input(component_id='type-dropdown', component_property='value')] # (2)
    )
    
def update_figure(year, type): # (3)
    if type==True:
        return px.histogram(data_year[year[0]],x=type, nbins=20)
    else:
        return px.histogram(data_year[year],x=type, nbins=20)


@app.callback(
    Output(component_id='titre', component_property='children'), # (1)
    [Input(component_id='type-dropdown', component_property='value')] # (2)
)
def update_title(input_value): # (3)
    return (f'University {input_value} rating')

@app.callback(  
        Output('year-slider', 'value'),
        [Input('interval', 'n_intervals')])

def on_tick(n_intervals):
    if n_intervals is None: return 0
    return years[(n_intervals+1)%len(years)]
#
# RUN APP
#
@app.callback(
    Output('interval','disabled'),
    #Input('button', 'children'),
    Input('Play','n_clicks'),
    Input('Pause', 'n_clicks')
)


def update_status(Play,Pause):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'Pause' in changed_id:
        return True
    elif 'Play' in changed_id:
        return False



"""
html.Label('Year'),
                            
dcc.Slider(
                    id="type-proj",
                    marks={
                        te:{'label': '1952'},#, 'value': 1952},
                        1957:{'label': '1957'},#, 'value': 1957},
                        1962:{'label': '1962'},#, 'value': 1962},
                        1967:{'label': '1967'},#, 'value': 1967},
                        1972:{'label': '1972'},#, 'value': 1972},
                        1977:{'label': '1977'},#, 'value': 1977},
                        1982:{'label': '1982'},#, 'value': 1982},
                        1987:{'label': '1987'},#, 'value': 1987},
                        1992:{'label': '1992'},#, 'value': 1992},
                        1997:{'label': '1997'},#, 'value': 1997},
                        2002:{'label': '2002'},#, 'value': 2002},
                        2007:{'label': '2007'},#, 'value': 2007},
                    },
                    value=1952,
                ),                 

dcc.Slider(
                                id="type_proj",
                                marks={
                                    'teaching':{'label': 'teaching'},
                                    'international':{'label': 'international'},
                                    'research':{'label': 'research'},
                                    'citations':{'label': 'citations'},
                                    'income':{'label': 'income'},
                                },
                                value='teaching',
                            ),           


                             {'label': 'teaching', 'value': col_names[0]},
                                    {'label': 'international', 'value': col_names[1]},
                                    {'label': 'research', 'value': col_names[2]},
                                    {'label': 'citations', 'value': col_names[3]},
                                    {'label': 'income', 'value': col_names[4]},
                                      




html.Div(children=f'''
                                The graph above shows relationship between life expectancy and
                                GDP per capita for year {year}. Each continent data has its own
                                colour and symbol size is proportionnal to country population.
                                Mouse over for details.
                            '''), # (7)

html.Label('Year'),
                            
dcc.Slider(
    id="year-slider",
    min=2011,
    max=2016,
    marks={
        2011:{'label': '2011'},#, 'value': 1952},
        2012:{'label': '2012'},#, 'value': 1957},
        2013:{'label': '2013'},#, 'value': 1962},
        2014:{'label': '2014'},#, 'value': 1967},
        2015:{'label': '2015'},#, 'value': 1972},
        2016:{'label': '2016'},#, 'value': 1977},
    },
    value=2011,
),


@app.callback(
    Output(component_id='graph1', component_property='figure'), # (1)
    [Input(component_id='year-slider', component_property='value')] # (2)
)
    
def update_figure(input_value): # (3)
    return px.scatter(type_proj[input_value], x=input_value,nbins=20) # (4)

"""


app.run_server(debug=True)
