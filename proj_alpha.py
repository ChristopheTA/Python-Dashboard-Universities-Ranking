import pandas as pd
import numpy as np
import json
import branca
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
df3= pd.read_csv('Data_Projet/continent.csv', na_values=["NaN"])
df1= df1.rename(columns = {"Country" : "country"})
df3= df3.rename(columns = {"name" : "country","region":"continent"})
df3=df3[["country","continent"]]
data_ext=pd.merge(df1,df3)
full_data=pd.merge(data_ext,df2)

dfc = full_data.groupby(by = ["country"])["country"].count().to_frame("count")
#print(dfc)
dfc_count=dfc.values.tolist()
col=list(full_data.columns)
col_dfc=list(dfc)
col_histo=col[6:12]
col_map=[]
#col_map[0]="count"
col_map[1:]=col[12:16]
info="teaching"

year=2011
years=full_data["year"].unique()
data_year={ year:full_data.query("year == @year") for year in years}

coords=(46.539758, 2.430331)
map = folium.Map(location=coords,tiles='OpenStreetMap', zoom_start=6)
#map.save('map_alpha.html')
country_location=full_data[["latitude","longitude","country"]]


country_location=full_data[["latitude","longitude","country"]].drop_duplicates()
dfc=full_data.groupby(by = ["country"])["country"].count().to_frame("count")
df_count=list(dfc["count"])
country_location["count"]=(df_count)


full_data["num_students"]=full_data["num_students"].str.replace(',','.')
full_data["num_students"]=full_data['num_students'].astype("float64")
df_num=full_data.groupby(by = ["country"])['num_students'].sum().to_frame("num_students")
list_num=list(df_num["num_students"])
country_location['num_students']=list_num


with open("Data_Projet/countries.geojson") as f:
    data_country=json.load(f)

folium.Choropleth(
    geo_data=data_country,
    data=country_location,
    columns=["country", "num_students"],
    key_on="feature.properties.ADMIN",
    fill_color="YlOrRd", 
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="Repartition of Universities",
    #reset=True,
    nan_fill_color='White'
).add_to(map)
map.save(outfile='map_beta.html')


if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    fig = px.histogram(
        data_year[year],
        x='teaching',
        color='continent',
        color_discrete_map={ # replaces default color mapping by value
            "Oceania": "red",
            "Europe": "green",
            "Asia": "blue",
            "Africa": "goldenrod", 
            "Americas": "magenta"
            },
        nbins=40) # (4)


    app.layout = html.Div(children=[
                            html.H1(id = "titre", children=f'University {info} rating',
                                        style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                            html.Label("Type"),
                            
                            dcc.Dropdown(
                                id="type-dropdown",
                                options=[ {'label': i, 'value': i} for i in col_histo
                                   ],
                                value=col_histo[0],
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

                            dcc.RadioItems(
                                id='map-value',
                                options = [{'label': i, 'value': i} for i in col_map
                                   ],
                                   value=col_map[0],
                                   labelStyle={"display":'inline-block'}
                            ),

                            html.H2('World Map Alpha'),
                            html.Iframe(id='map', srcDoc=open('map_beta.html','r').read(),width='80%',height='500'),
                            
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
    return px.histogram(
        data_year[year],
        x=type,
        color='continent',
        color_discrete_map={ # replaces default color mapping by value
            "Oceania": "red",
            "Europe": "green",
            "Asia": "blue",
            "Africa": "goldenrod", 
            "Americas": "magenta"
            },
        nbins=40)


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




app.run_server(debug=True)


"""
def map_country_locations():
    for i,loc_info in country_location.iterrows():

        folium.CircleMarker(
                location = (loc_info["latitude"], loc_info["longitude"]),
                radius = np.power(loc_info['count'], 1/2),
                color = 'crimson',
                fill= True,
                fill_color= 'crimson'
            ).add_to(map)
            
            #country_map=map_country_locations()
            
            """