import pandas as pd
import numpy as np
import json
from os import makedirs
from dash.dcc.Interval import Interval
import plotly_express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import callback_context
import folium

if __name__ == '__main__':

    try:
        df1= pd.read_csv('Data_Projet/country-coordinates-world.csv',na_values=["-"])
    except:
        print("Data_Projet/country-coordinates-world.csv not found")
        quit()

    try:
        df2= pd.read_csv('Data_Projet/timesData.csv', na_values=["-"])
    except:
        print("Data_Projet/timesData.csv not found")
        quit()

    try:
        df3= pd.read_csv('Data_Projet/continent.csv', na_values=["NaN"])
    except:
        print("Data_Projet/continent.csv not found")
        quit()

    try:
        with open("Data_Projet/countries.geojson") as f:
            data_country=json.load(f)
    except:
        print('Data_Projet/countries.geojson not found')
        quit()

    df1= df1.rename(columns = {"Country" : "country"})
    df2 = df2.rename(columns = {"teaching" : "Teaching", "internation" : "International", 
                            "research" : "Research", "citations" : "Citations", "income" : "Income",
                            "total_score" : "Total Score", "num_students" : "Number of Students",
                            "student_staff_ratio" : "Student / Staff Ratio"}) 
    df3= df3.rename(columns = {"name" : "country","region":"continent"})
    df3=df3[["country","continent"]]
    data_ext=pd.merge(df1,df3)
    full_data=pd.merge(data_ext,df2)

    coords=(46.539758, 2.430331)
    map = folium.Map(location=coords,tiles='OpenStreetMap', zoom_start=2)

    dfc = full_data.groupby(by = ["country"])["country"].count().to_frame("Number of Universities")
    col=list(full_data.columns)
    col_histo=col[6:12]
    col_dfc=list(dfc.columns)
    col_map=col_dfc+col[12:14]
    #first_histo='Teaching'

    df_map=full_data[["country","year"]].drop_duplicates()
    count=full_data.groupby(by = ["country","year"])["country"].count().to_frame("count")
    list_count=list(count["count"])
    df_map['Number of Universities']=list_count
    
    full_data["Number of Students"]=full_data["Number of Students"].str.replace(',','.')
    full_data["Number of Students"]=full_data['Number of Students'].astype("float64")
    num_students=full_data.groupby(by = ["country","year"])['Number of Students'].sum().to_frame("Number of Students")
    list_students=list(num_students["Number of Students"])
    df_map['Number of Students']=list_students

    full_data["Student / Staff Ratio"]=full_data['Student / Staff Ratio'].astype("float64")
    stu_sta_ratio=full_data.groupby(by = ["country","year"])['Student / Staff Ratio'].mean().to_frame("Student / Staff Ratio")
    list_stu_sta=list(stu_sta_ratio["Student / Staff Ratio"])
    df_map['Student / Staff Ratio']=list_stu_sta

    app = dash.Dash(__name__) # (3)

    app.layout = html.Div(children=[
        html.H1(id = "titre", children='World University Rankings (from 2011 to 2016)',
                    style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

        html.H2(id='titre_histo', children='World Ranking Universities Histogramm'),

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

        html.H2(id='titre_map', children = 'Universities World Map'),

        html.Label('Type'),

        dcc.RadioItems(
            id='map-value',
            options = [{'label': i, 'value': i} for i in col_map
                ],
                value=col_map[0],
                labelStyle={"display":'inline-block'}
        ),

        html.Label('Year'),

        dcc.Slider(
            id="year-map",
            min=2011,
            max=2016,
            marks={
                2011:{'label': '2011'},
                2012:{'label': '2012'},
                2013:{'label': '2013'},
                2014:{'label': '2014'},
                2015:{'label': '2015'},
                2016:{'label': '2016'}
            },
            value=2011,
        ),

        html.Iframe(id='map', srcDoc=open('map_beta.html','r').read(),width='100%',height='800'),
        
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
    if  year is None and type is None:
        raise PreventUpdate
    else:
        years_map=full_data["year"].unique()
        data_year={ year:full_data.query("year == @year") for year in years_map}

    return px.histogram(
        data_year[year],
        x=type,
        color='continent',
        color_discrete_map={ # replaces default color mapping by value
            "Oceania": "red",
            "Europe": "green",
            "Asia": "blue",
            "Africa": "goldenrod", 
            "Americas": "orange"
            },
        nbins=40)




@app.callback(  
        Output('year-slider', 'value'),
        [Input('interval', 'n_intervals')])

def on_tick(n_intervals):
    if n_intervals is None: return 0
    years=full_data["year"].unique()
    return years[(n_intervals+1)%len(years)]

@app.callback(
    Output('interval','disabled'),
    Input('Play','n_clicks'),
    Input('Pause', 'n_clicks')
)


def update_status(Play,Pause):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'Pause' in changed_id:
        return True
    elif 'Play' in changed_id:
        return False


@app.callback(
        Output(component_id='map', component_property='srcDoc'), # (1)
        [Input(component_id='map-value', component_property='value'),
        Input(component_id='year-map', component_property='value')] # (2)
    )

def update_map(input_value,input_year):
    if  input_value is None and input_year is None:
        raise PreventUpdate
    else:
        years_histo=df_map["year"].unique()
        df={ year:df_map.query("year == @year") for year in years_histo}

        if input_value == 'Number of Universities' :
            val_legend = 'Repartition of the Top Universities in the World'
        if input_value == 'Number of Students' :
            val_legend = 'Number of Students in Each Country'
        if input_value == 'Student / Staff Ratio' :
            val_legend = 'Student / Staff Ratio (in %)'        
        
        folium.Choropleth(
            geo_data=data_country,
            data=df[input_year],
            columns=["country", input_value],
            key_on="properties.ADMIN",
            fill_color="YlOrRd", 
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name=val_legend,
            reset=True,
            nan_fill_color='White'
        ).add_to(map)

    for key in map._children:
        if key.startswith("fill_color"):
            del(map._children[key])

    map.save(outfile='map_beta.html')

    return open('map_beta.html','r').read()

#
# RUN APP
#


"""
@app.callback(
    Output(component_id='titre', component_property='children'), # (1)
    [Input(component_id='type-dropdown', component_property='value')] # (2)
)
def update_title(input_value): # (3)
    return (f'University {input_value} rating')




"""

app.run_server(debug=True)


