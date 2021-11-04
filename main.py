"""
authors:
    Hoang-Duc DUONG : hoang-duc.duong@edu.esiee.fr
    Christophe TA : christophe.ta@edu.esiee.fr

"""
import json
import dash
import folium
import pandas as pd
import numpy as np
import plotly_express as px
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import callback_context
from dash import dash_table
from dash import dcc
from dash import html

if __name__ == '__main__':

    """
    Instanciation des fichiers à lire et test d'exception :

    Args:
        Fichiers dans le dossier Data_Projet/ avec précision des NaN values

    Returns:
        Lis le fichier passé en argument
        Sinon : Renvoie un message d'erreur
    """

    try:
        df1= pd.read_csv('Data_Projet/timesData.csv', na_values=["-",""])
    except:
        print("Data_Projet/timesData.csv not found")
        quit()

    try:
        df2= pd.read_csv('Data_Projet/continent.csv', na_values=["NaN",""])
    except:
        print("Data_Projet/continent.csv not found")
        quit()

    try:
        with open("Data_Projet/countries.geojson") as f:
            data_country=json.load(f)
    except:
        print('Data_Projet/countries.geojson not found')
        quit()

    """
    Modification des fichiers pour les adapter aux variables du projet

    Fonction rename():
        1st arg : Nom de variable de base
        2nd arg : Nom qui remplace la variable  
    
    Fonction merge() : assemble les deux fichiers passés en paramètre

    """

    df1 = df1.rename(columns = { "teaching" : "Teaching", "international" : "International", 
                            "research" : "Research", "citations" : "Citations", "income" : "Income",
                            "total_score" : "Total Score", "num_students" : "Number of Students",
                            "student_staff_ratio" : "Student / Staff Ratio",
                            "international_students" : "International Students", "female_male_ratio" : "Female / Male Ratio",
                            "world_rank" : "World Rank", "university_name" : "University's Name"})

    """
    Modification de certains noms de valeurs pour l'adapter au fichier GeoJSON

    """
    df1["country"]=df1['country'].str.replace('Hong Kong', 'Hong Kong S.A.R')
    df1["country"]=df1['country'].str.replace('Macau', 'Macao S.A.R')
    df1["country"]=df1['country'].str.replace('Serbia', 'Republic of Serbia ')
    df1["country"]=df1['country'].str.replace('Russian Federation', 'Russia')
    df1["country"]=df1['country'].str.replace('Republic of Ireland', 'Ireland')
    df1["country"]=df1['country'].str.replace('Unisted States of America', 'United States of America')
    df1["country"]=df1['country'].str.replace('Unted Kingdom', 'United Kingdom')

    df2= df2.rename(columns = {"name" : "country","region":"continent"}) # on renomme ici le 3ème fichier pour matcher la similitude avec le 1er fichier
    df2=df2[["country","continent"]] # on n'extrait que les colonnes utiles du fichier
    full_data=pd.merge(df2,df1)

    """
    Création de variables globales utilisées dans la suite du projet       
    """

    coords=(46.539758, 2.430331) #coordonnées de départ de la map du Dashboard : ESIEE Paris  
    map = folium.Map(location=coords,tiles='OpenStreetMap', zoom_start=1.5) #génération de la map du Dashboard
    map.save(outfile='map.html')

    full_data['World Rank']=full_data['World Rank'].str.replace("=",'').str.replace("-",".").astype("float64").apply(np.trunc)#modifie pour un format de classement
    df_tab=full_data[["World Rank","University's Name",'country','year','Total Score']]
    df_tab=df_tab.sort_values("World Rank").head(60)#on prend ici les 60 premières cases du tableau (5 pour le nom des colonnes + 5*10 pour les données)

    years_tab=df_tab["year"].unique()
    tab_year={ year:df_tab.query("year == @year") for year in years_tab} # instancie une sous-dataframe ayant en entrée l'année choisie
    year=2011

    """
    Instanciation des colonnes utilisées pour les données du diagramme, de l'histogramme et de la map

    """
    dfc = full_data.groupby(by = ["country"])["country"].count().to_frame("Number of Universities") #création d'une nouvelle colonne de données
    col=list(full_data.columns)
    col_histo=col[4:10]
    col_dfc=list(dfc.columns)
    col_map=col_dfc+col[10:14]
    first='Teaching'
    second='International'
    col_diagram=col[4:14]
    
    """
    Création d'une sous-dataframe exclusive à la map du Dashboard en fonction des valeurs transformées en dessous

    """

    df_map=full_data[["country","year"]].drop_duplicates() # sous-Dataframe sans duplicat pour avoir une dimension conforme
    count=full_data.groupby(by = ["country","year"])["country"].count().to_frame("count") # regroupe les pays en fonction des pays et de l'année
    list_count=list(count["count"]) # conversion des données en liste
    df_map['Number of Universities']=list_count # ajout dans la dataframe 
    
    full_data["Number of Students"]=full_data["Number of Students"].str.replace(',','.').astype("float64") # Adapte la valeur en format de nombre
    num_students=full_data.groupby(by = ["country","year"])['Number of Students'].sum().to_frame("Number of Students")
    list_students=list(num_students["Number of Students"])
    df_map['Number of Students']=list_students

    full_data["Student / Staff Ratio"]=full_data['Student / Staff Ratio'].astype("float64")
    stu_sta_ratio=full_data.groupby(by = ["country","year"])['Student / Staff Ratio'].mean().to_frame("Student / Staff Ratio")
    list_stu_sta=list(stu_sta_ratio["Student / Staff Ratio"])
    df_map['Student / Staff Ratio']=list_stu_sta

    full_data["Female / Male Ratio"]=full_data["Female / Male Ratio"].str.replace(" : ",".").astype("float64").apply(np.trunc)# Valeur du ratio avant le point 
    female_male_ratio=full_data.groupby(by = ["country","year"])['Female / Male Ratio'].mean().to_frame("Female / Male Ratio")
    list_fml=list(female_male_ratio["Female / Male Ratio"])
    df_map['Female / Male Ratio']=list_fml

    full_data['International Students']=full_data['International Students'].str.replace("%","").astype('float64')
    inter_stu=full_data.groupby(by = ["country","year"])['International Students'].mean().to_frame("International Students")
    list_inter=list(inter_stu["International Students"])
    df_map['International Students']=list_inter

    """
    Initialisation de la page du Dashboard

    """

    app = dash.Dash(__name__) 

    app.layout = html.Div(children=[
        html.H1(id = "titre", children='World University Rankings (from 2011 to 2016)',
                    style={'textAlign': 'center', 'color': '#7FDBFF'}), # Titre principal de la page

        html.Img(src=app.get_asset_url('ESIEE.png'),width='20%',height='80'),

        dcc.Tabs([

            dcc.Tab(label='Diagram and Ranking', children=[

                html.H2(id='titre_diagram', children=f'World Ranking Universities Diagramm ({second} depending on {first})'),

                html.Div(children=[
                    html.Label("X",style=dict(width='5%')),

                    dcc.Dropdown(
                        id="type_x-dropdown",
                        options=[ {'label': i, 'value': i} for i in col_diagram
                            ],
                        value=col_diagram[0],
                        style=dict(width='50%')
                    ), # Liste déroulante des valeurs d'abscisse du diagramme

                    html.Label("Y",style=dict(width='5%')),         
                
                    dcc.Dropdown(
                        id="type_y-dropdown",
                        options=[ {'label': i, 'value': i} for i in col_diagram
                            ],
                        value=col_diagram[1],
                        style=dict(width='50%')
                    ), # Liste déroulante des valeurs d'ordonnée du diagramme
                ],style=dict(display='flex')),

                dcc.Slider(
                        id="year-diagram",
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
                ), # Années des données du diagramme et du tableau

                html.Div(children=[

                    dcc.Graph(
                        id='diagram',
                        style=dict(width='50%')
                    ), # (6)

                    dash_table.DataTable(
                        id='table',
                        data=tab_year[year].to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in df_tab.columns.drop(['year'])],
                        style_cell={
                            'height': 'auto',
                            # all three widths are needed
                            'minWidth': '200px', 'width': '200px', 'maxWidth': '200px',
                            'whiteSpace': 'normal'
                        }
                    ), # Tableau du Top 10
                ],style=dict(display='flex')),   
            ]),

            dcc.Tab(label='Histogram', children=[    


                html.H2(id='titre_histo', children=f'World Ranking Universities Histogramm ({first} Rating)'), # 1ère partie du Dashboard : données de l'histogramme

                html.Label("Type"),

                html.Div(children=[
                    dcc.Dropdown(
                        id="type-dropdown",
                        options=[ {'label': i, 'value': i} for i in col_histo
                            ],
                        value=col_histo[0],
                        style=dict(width='50%')
                    ), # Liste déroulante des valeurs de l'histogramme

                    html.Label('Year'),
                    
                    dcc.Slider(
                        id="year-slider",
                        min=2011,
                        max=2016,
                        marks={
                            2011:{'label': '2011'},
                            2012:{'label': '2012'},
                            2013:{'label': '2013'},
                            2014:{'label': '2014'},
                            2015:{'label': '2015'},
                            2016:{'label': '2016'},
                        },
                        value=2011,
                    ), # Années des données de l'histogramme
                ]),
                
                dcc.Graph(
                    id='histo',
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
                html.Div(id='button'), # Bouton pour Play / Pause l'animation de l'histogramme 

                dcc.Interval(id='interval',
                    interval=2*1000, # in milliseconds
                    n_intervals=0,
                    #disabled=True
                ), # Création de l'interval de données pour l'animation de l'histogramme
            ]),

            dcc.Tab(label='World Map', children=[

                html.H2(id='titre_map', children = 'Universities World Map'), # 2nd partie du Dashboard : données de la World Map 

                html.Label('Type'),

                html.Div(children=[
                    dcc.RadioItems(
                        id='map-value',
                        options = [{'label': i, 'value': i} for i in col_map
                            ],
                            value=col_map[0],
                            labelStyle={"display":'inline-block'},
                            style=dict(width='50%')
                    ), # Choix des valeurs possibles sur la map

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
                    ), # Années des données de la map
                ]),

                html.Iframe(id='map', srcDoc=open('map.html','r').read(),width='100%',height='500'), # Generation de la map par lecture d'un fichier map.html,
                                                                                                    # initialement compilé pour l'affichage      
                ])
            ])
        ]
    )

@app.callback(
        [Output(component_id='diagram', component_property='figure'), 
        Output(component_id='titre_diagram', component_property='children')],
        Output(component_id='table',component_property='data'),
        [Input(component_id='type_x-dropdown', component_property='value'),
        Input(component_id='type_y-dropdown', component_property='value'),
        Input(component_id='year-diagram', component_property='value'),] 
    ) # Appel des données de l'histogramme et des valeurs qui le modifient : l'année et le type de valeurs
    
def update_diagram(x, y,year):
    """
    Retourne le diagramme en fonction des arguments en paramètre

    Args:
        x : valeur choisie en abscisse
        y : valeur choisie en ordonnée
        year : l'année des données choisies

    Returns:
        Le diagramme de "y" en fonction de "x"
        Le tableau des 10 Meilleures Universités en fonction de l'année
    
    """

    if  x is None and y is None:
        raise PreventUpdate # Si rien n'a été sélectionné, on n'actualise pas l'histogramme
    
    years_diagramm=full_data["year"].unique()
    data_year={ year:full_data.query("year == @year") for year in years_diagramm} # instancie une sous-dataframe ayant en entrée l'année choisie

    return px.scatter(
        data_year[year], # Histogramme de l'année choisie
        x=x, # type de données voulues en abscisse
        y=y,
        color='continent',
        color_discrete_map={ # attribue des couleurs fixes au continent
            "Oceania": "red",
            "Europe": "green",
            "Asia": "blue",
            "Africa": "goldenrod", 
            "Americas": "orange"
        }), (f'World Ranking Universities Diagramm ({y} depending on {x})'),tab_year[year].to_dict('records')



@app.callback(
        [Output(component_id='histo', component_property='figure'), 
        Output(component_id='titre_histo', component_property='children')],
        [Input(component_id='year-slider', component_property='value'),
        Input(component_id='type-dropdown', component_property='value')] 
    ) # Appel des données de l'histogramme et des valeurs qui le modifient : l'année et le type de valeurs
    
def update_histo(year, type):
    """
    Retourne l'histogramme' en fonction des arguments en paramètre

    Args:
        year : l'année choisi dans le slider animé
        type : la valeur étudiée choisie

    Returns:
        L'histogramme de données "year" en fonction de "type"
    
    """

    if  year is None and type is None:
        raise PreventUpdate # Si rien n'a été sélectionné, on n'actualise pas l'histogramme
    
    years_map=full_data["year"].unique()
    data_year={ year:full_data.query("year == @year") for year in years_map} # instancie une sous-dataframe ayant en entrée l'année choisie

    return px.histogram(
        data_year[year], # Histogramme de l'année choisie
        x=type, # type de données voulues en abscisse
        nbins=40), (f'World Ranking Universities Histogramm ({type} Rating)')

@app.callback(  
        Output('year-slider', 'value'),
        [Input('interval', 'n_intervals')]) # appel des variables pour l'animation de l'histogramme

def on_tick(n_intervals):

    """
    Actualise l'animation de l'histogramme

    Args:
        n_intervals: la durée de l'intervalle entre les valeurs

    Returns:
        L'animation de l'histogramme de durée d'intervalle n_intervals
    
    """

    if n_intervals is None: return 0
    years=full_data["year"].unique()
    return years[(n_intervals+1)%len(years)] 

@app.callback(
    Output('interval','disabled'), # Variable du status de l'intervalle
    Input('Play','n_clicks'),
    Input('Pause', 'n_clicks') # Variables qui active / désactive l'animation 
)

def update_status(Play,Pause):

    """
    Active / Désactive l'animation de l'histogramme

    Args:
        Play : met en marche l'animation
        Pause : met en suspens l'animation 

    Returns:
        Status Marche / Arrêt de l'animation
    
    """

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if "Pause" in changed_id:
        return True # Modifie la valeur de la variable 'disabled' qui change le status de l'intervalle, de base false
    elif "Play" in changed_id:
        return False # Active l'animation

@app.callback(
        Output(component_id='map', component_property='srcDoc'), # Valeur de la projection de la map
        [Input(component_id='map-value', component_property='value'),
        Input(component_id='year-map', component_property='value')] # Variables qui modifient les données de la map
    )

def update_map(input_value,input_year):

    """
    Actualise la World Map en fonction du type et de l'année voulus

    Args:
        input_value : type de valeur de la Map
        input_year : année des données de la Map 

    Returns:
        World Map de 'type' en fonction de l'année 'year'
    
    """

    if  input_value is None and input_year is None:
        raise PreventUpdate # Si rien n'a été sélectionné, on n'actualise pas la Map
    
    years_map=df_map["year"].unique()
    df={ year:df_map.query("year == @year") for year in years_map} # instancie une sous-dataframe ayant en entrée l'année choisie

    if input_value == 'Number of Universities' :
        val_legend = 'Repartition of the Top Universities in the World (Count in Nb)'
    elif input_value == 'Number of Students' :
        val_legend = 'Number of Students in Each Country (x10e3)'
    elif input_value == 'Student / Staff Ratio' :
        val_legend = 'Student / Staff Ratio' 
    elif input_value == 'International Students' :
        val_legend = 'Portion of International Students in Each Country (in %)' 
    elif input_value == 'Female / Male Ratio' :
        val_legend = 'Female / Male in Ratio'    # en fonction du type choisie, on attribue une légende spécifique à la Map      


    map = folium.Map(location=coords,tiles='OpenStreetMap', zoom_start=1.5) #génération de la map du Dashboard

    folium.Choropleth(
        geo_data=data_country, # fichier JSON pour les contours géographiques
        data=df[input_year], # année choisie
        columns=["country", input_value], # en fonction des pays, on choisit le type de valeur voulu
        key_on="properties.ADMIN", # valeur du fichier JSON à tracer sur la map
        fill_color="YlOrRd", # couleur d'accentuation des valeurs
        fill_opacity=0.7,
        line_opacity=0.5, # opacité des couleurs sur les pays
        legend_name=val_legend, # légende définie au dessus
        reset=True,
        nan_fill_color='White' # pays en blanc si aucune valeur sur ce-dernier ne correspond 
    ).add_to(map) # ajout de ces paramètres à la map

    map.save(outfile='map.html') # conversion des données pour actualiser le fichier HTML

    return open('map.html','r').read() # actualisation de la variable modifiée dans le callback()

#
# RUN APP
#

app.run_server(debug=True)


