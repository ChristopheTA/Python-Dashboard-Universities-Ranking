# INTRODUCTION
Le projet ici que nous avons réalisé est l'étude des données concernant le classement mondial des 100 meilleures universités. 

Nous avons utilisé comme jeu de données les valeurs venant de l'institut [`Times Higher Education (THE)`](https://www.timeshighereducation.com/) étant l'une des plus connues et des plus influentes dans les mesures de données universitaires. 

Le dataset de départ comporte des notes des écoles sur plusieurs années concernant comme par exemple l'enseignement, les recherches effectuées ou encore le score total de l'université. D'autres données ont également été utiles pour un différent type d'étude géographique comme la répartition d'étudiants internationaux ou encore le rapport femme/homme. 

Toutes ces informations nous amènent à répondre à la problematique suivante : `Comment est l'état de la Haute Education dans le monde ?`


# INSTALLATION ET UTILISATION DES FICHIERS

## Installation de Git et récupération des fichiers

Vérifiez tout d'abord que vous avez installé [Git](https://git-scm.com/) pour la récupération des fichiers.

Nous allons maintenant cloner le projet dans le répertoire de votre choix. Pour cela, cliquez sur votre répertoire et faites clique-droit `Git Bash Here`.

Une fois Git Bash ouvert, nous allons cloner le répertoire en ligne où se trouve le projet. Cliquez sur le bouton `Clone or Download` et copiez l'adresse HTTPS du [répertoire](https://git.esiee.fr/duongh/python-pour-la-data-science.git).
Une fois copié, retournez dans Git Bash et tapez la commande `git clone` (adresse du répertoire) et cela vous donnera un accès de téléchargement au répertoire.
Finalement, tapez la commande `git pull` et vous aurez à votre disposition tous les fichiers du projet. 

## Comprendre les fichiers

Voici l'inventaire des fichiers présents dans notre projet :
- le fichier [`main.py`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/blob/master/main.py) qui sera la base de notre étude et l'ensemble des données affichés.
- le dossier [`Data_Projet`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/tree/master/Data_Projet) contenant le [dataset](https://www.kaggle.com/mylesoneill/world-university-rankings?=select=timesData.csv) (jeux de données) au format `csv`, un fichier [continents2](https://www.kaggle.com/andradaolteanu/country-mapping-iso-continent-region) ainsi qu'un fichier [`GeoJSON`](https://datahub.io/core/geo-countries#resource-countries) pour la représentation géographique.
- le fichier [`requirement.txt`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/blob/master/requirements.txt) contenant tous les packages nécessaires au bon fonctionnement du Dashboard.
- le fichier [`get_data.py`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/blob/master/get_data.py) vous donnant les fichiers à leurs sources si ils sont corrompus localement
- le fichier [`kaggle.json`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/blob/master/kaggle.json) contenant les authentifications d'un administrateur (ici l'un de nos identifiants confidentiels svp :) )
- le dossier [`assets`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/tree/master/assets) pour l'image de la page (représentant notre école :) ).


# USER'S GUIDE

## Installation des packages nécessaires

Vérifiez tout d'abord si vous disposez de la bonne version de Python. Pour cela:
- ouvrir l'invite de commandes de Windows (Windows+R, puis tapez cmd)
- dans l'invite de commandes tapez `python --version`
- vérifiez si la version est à jour, de préférence la version `3.9.7`

Certains packages seront également nécessaires à installer pour la bonne utilisation du dash si cela n'est pas déjà fait :
- ouvrir l'invite de commandes et se rendre dans le dossier du projet
- tapez la commande `python -m pip install -r requirements.txt`
- les packages sont désormais installés

Une fois les packages obtenus, pour afficher notre dashboard, il faudra donc exécuter sur l'invite de commandes le fichier `main.py` avec la commande `python main.py` avec en référence dans le même répertoire tous les dossiers nécessaires à l'exécution cités au-dessus. 

## Récupérer les données à la source

Si les données dans le dossier ne fonctionnent pas, il est nécessaire de passer par l'exécution du fichier `get_data.py`. Ce fichier va chercher directement les informations sur les urls qu'on lui a fourni, ici des informations sur Kaggle et un fichier json. 
Pour récupérer les fichiers, il faut exécuter la commande `python get_data.py`, cette commande va renvoyer une erreur de type `OSError`, ce qui est tout à fait normal. Pour remédier à cela, placer le fichier `kaggle.json` dans le chemin d'accès indiqué. Si tout est bien exécuté, relancez les commandes et vous pourrez obtenir les fichiers attendus. 

## Fonctionnement du Dashboard

Une fois le fichier lancé, le terminal va fournir une adresse url local, ici `http://127.0.0.1:8050/`. Tapez cette adresse va nous renvoyer vers notre navigateur par défaut (de préférence Chrome ou Brave) et charger le dashboard. 

Une fois la page cherchée, vous pourrez apercevoir 3 onglets à parcourir nommés respectivement `Graph and World Ranking`, `Histogram` et `World Map` qui contiennent chacun différent type de graphique représentant notre dataset. 

Sur chacun de ces onglets, vous verrez une barre horizontale appelée `Year` qui permettra de changer l'année des données étudiées.

Dans le premier onglet, vous avez 2 représentations graphiques : un graphique sur les données de la dataset et un tableau représentant les 10 meilleures universités sur chaque année. Vous pouvez également préciser dans la barre de recherches si vous voulez étudier un pays en particulier. Si même lorsque vous cliquez sur un pays et que rien ne s'affiche, c'est que l'année en question n'a pas de données sur le pays et ses universités, faites glisser la barre chronologique pour en avoir (par exemple, l'Argentine ne possède que des données en 2016). 

Dans le deuxième onglet, nous avons utilisé les données de la première moitié des données du data set afin d'en faire un histogramme donnant une approche d'étude plus numérique. On aura donc à disposition sur l'histogramme les valeurs allant de 0 à 100, ainsi que leurs effectifs moyens. De plus comme l'onglet précédent, on peut préciser le pays étudié. 
Cet onglet dispose d'une animation constante faisant défiler les années de l'histogramme pour observer de manière constante la variance des résultats et les tendances qu'on peut y voir.  

Et enfin, le troisième onglet donnera une représentation géographique de la seconde partie des données plus 'qualitative', avec une palette de couleur du jaune au rouge en fonction l'intervalle des données. Comme vous pourrez le voir, il y a peu de pays affichés en données en premier lieu, car l'information de départ en 2011 ne contient pas toutes les universités car le classement varie et de nouvelles entrées et sorties de nouveaux pays se font chaque année. 


# DEVELOPPER'S GUIDE

## Structure du fichier principal et instanciation

Après avoir énumérer les étapes et fichiers nécessaires à l'initialisation de notre Dashboard, voyons maintenant la structure du fichier principal `main.py`.

Le fichier se décompose en 5 parties:
- l'initialisation des packages exécutables
- la lecture des fichiers contenant la dataset et autres fonctionnalités nécessaires
- l'initialisation des variables globales utilisées dans le Dashboard
- création du Dashboard avec les fonctionnalités de page HTML
- Rappel des fonctions et instanciation des fonctionnalités de la page

La lecture des fichiers est simple. On va 'essayer' de les ouvrir dans le dossier `Data_Projet` et si cela n'est pas possible, on renvoit un message avec le chemin d'accès en question et le fichier non-existant. 

S'en suit la création de la DataFrame. Nous avons dû renommer certains noms de colonnes pour pouvoir 'merge' les fichiers entre eux, ainsi que certains noms de cellule. On a appelé cette DataFrame `full_data`, qui contiendra toutes les informations de notre Dashboard, qu'on adaptera aux différents aspects de la page. 

Intéressons-nous maintenant à l'instanciation des variables. Il nous a tout d'abord fallu créer plusieurs sous-colonnes car chaque onglet étudie différentes colonnes. De la même facon, nous avons dû créer plusieurs sous-Dataframes nommées `df_tab` pour la DataFrame du tableau à classement et `df_map`, DataFrame contenant les données de la carte de l'onglet `World Map`. 

Pour `df_tab`, on a modifié le caractère classement pour avoir une valeur numérique et on a trié en fonction de ce-dernier. 

Concernant `df_map`, la structure de cette DataFrame est un peu différente du reste, il fallait appliquer pas mal d'opération pour pouvoir afficher une donnée sur la carte en fonction de l'année et du type choisie. On a tout d'abord extrait les colonnes `country, year` et supprimer les duplicats.
En fonction du type et du calcul voulu, on applique la fonction `groupby()` et on insère ces valeurs dans une colonne de la sous-Dataframe. 

## Page HTML du Dashboard

Maintenant que l'initialisation du `back-end` du Dashboard est créé, il nous faut la partie `front-end` de la page. 
Nous avons utilisé la structure classique d'un fichier HTML en travaillant les fonctions `Div()`, les titres `H1() H2()` et des labels, mais l'information qui sera affiché vient des fonctionalités du package `dash-core-components`, où on pourra retrouver pas mal de widgets comme une liste déroulante, un slider d'année, une représentation de tableau `DataTable` et des représentation de graphes, qui seront définis dans la partie suivante en utilisant l'id du widget.

## Callback et affichage des données

Une fois l'esthétique de la page faite, il faut maintenant la remplir d'information. Dash dispose d'une fonctionnalité pemettrant de rappeler les élements de la page et de leur fournir des informations en fonction des valeurs qu'on donnera en entrée. 

Nous allons nous intéresser au premier et troisième onglet qui ont un nombre conséquent `d'input_values` pour gérer les affichages graphiques.

Comme on l'a vu dans le User's Guide, le premier onglet contient un graphe et un tableau de classement. Le graphe comme on a pu le tester, a une possibilité de 3 entries possibles: l'abscisse, l'ordonnée et l'année, tandis que le tableau n'en a qu'une seule: l'année. 

On va donc callback l'id de la liste déroulante de x et y, ainsi que les sliders de l'année et pays. 
On utilise la méthode query pour définir une data_year qui va sélectionner les données en fonction de l'année et on prend les input_values pour tracer le graphe. On pourra préciser le pays en filtrant la dataframe. Les variables et fonctions du tableau étant déjà faites en global, on a plus qu'a retourner sa valeur en précisant l'année en input_value et en affichant seulement les 10 premières lignes triées pour en faire un Top 10. 

Le troisième onglet va utiliser le package folium, notamment le style Choropleth pour représenter les pays sur la carte. Ce que l'on modifier sur la page est l'année choisie et le type choisie, qui seront les input_value dans le callback avec la Map comme output.
On répète le même processus, on va query l'année dans la sous-dataframe et notre jeu de données est prêt. 

Pour tracer les pays sur la map, on a besoin de l'aide d'un fichier GeoJSON nommé `data_country` contenant l'ensemble des coordonnées et de leur contour. Il faut rechercher dans ce fichier l'expression en question similaire à notre colonne 'country' pour matcher les contours, ces données se trouvant dans le chemin `properties.ADMIN`. En y ajoutant les autres paramètres notamment la gamme de couleurs d'intensité des valeurs, on retourne ces informations dans un fichier `map.html`, qui sera lancé par la fonction Iframe de la page HTML.

## Exploration et pistes de recherches

Nous avons plusieurs pistes d'amélioration pour notre code.
Dans un premier temps, nous pensons qu'il serait intéressant de pouvoir se focaliser sur les États-Unis, pays qui rassemble les meilleures universités du monde. On pourrait alors voir la répartition de ces universités entre chaque état, et observer les divergences dans le pays lui-même.
Nous pensons aussi qu'utiliser les autres datasets des autres instituts serait pertinent. On pourrait par exemple fusionner les datasets pour obtenir plus de données d'universités, ou alors comparer ces datasets pour distinguer les différences dans les critères de notation.

# RAPPORT D'ANALYSE

Analysons et interprétons les données dans leur ensemble pour répondre à la problématique. On sait que d'après les données que nous voyons et de manière générale, les universités Américaines monopolisent le classement comme on peut le voir au niveau du tableau Top 10 au fil des années (jusqu'en 2016).

Intéressons-nous plus au valeur données par le Graphe sur différents critères. Est-ce que les meilleures écoles en général dominent vraiment sur tous les critères ? 

La réponse est à première vue non, puisque si par exemple on veut tracer le score total en fonction du pourcentage d'étudiants à l'international, on remarque que c'est plutôt les pays d'Europe qui ont certes un score total un peu moins élevé mais une répartition d'étudiants étrangers un peu plus égale pouvant aller jusqu'à 50 % d'étudiants étrangers contre maximum 35 % d'étudiants internationaux dans les universités américaines, ce qui montre bien que l'éducation aux Etats-Unis restent tout de même un privilège pas accessible à tout le monde. C'est pourquoi sur le critère `International`, l'Europe a en moyenne de meilleurs résultats.

Pour le reste des critères numériques à savoir l'enseignement, la recherche, les citations et les revenus, les universités d'Amérique du Nord ont de meilleurs résultats en moyenne, suivi de l'Europe, l'Asie, l'Océanie et l'Afrique, ce qui se voit en détail sur le tableau des 10 meilleures universités de chaque année, avec les Etats-Unis et le Royaume-Uni se partageant majoritairement les places.  

Bien que les nombres jouent en faveur des pays Anglosaxons, on peut voir que cela reste tout de même juste un échantillon du reste des universités. On peut voir sur la deuxième représentation graphique un histogramme des valeurs numériques en globalité et le résultat montre que chaque critère a une moyenne de scores importante entre 20 et 40 sur l'ensemble des universités, montrant bien la notation pointue des critères de l'institut THE. 

Analysons maintenant ces valeurs et cherchons si certaines d'entre elles sont liées en changeant les variables sur les axes du graphique et en observant si cela forme une régression. On constate que hormis entre la note de l'international et le taux d'elèves internationaux, et la note d'enseignement et le score total, très peu de données corellent entre elles, ce qui montre l'impact du taux d'enseignement dans la notation du score total de chaque université.    

Qu'en est-il de la représentation géographique et comment faire la relation avec les scores obtenus ? On constate que les nombres jouent en la faveur des Etats-Unis avec un nombre conséquent d'universités et de nombres d'étudiants dans le haut du classement. 

Si maintenant on s'intéresse aux valeurs de ratio, on constate que dans les pays où les universités sont bien classées ayant les plus hauts `Total Score`, ont un `Student / Staff Ratio` assez bas, ce qui signifie qu'un intervenant va gérer un nombre d'élève assez bas, ce qui peut expliquer une meilleure méthode et donc de meilleurs résultats. 

Le critère `International Students` comme vu précédemment présente des résultats assez homogènes au fil des années, avec en tête de valeurs la Russie et l'Australie aux alentours des 40 % en moyenne.   
Le dernier ratio `Female / Male Ratio` montre avec 'surprise' que la haute éducation a une forte tendance féminine en majorité sur tout le globe sur toutes les années. 

En conclusion, bien que la valeur du score total d'une université reflète en grande partie son niveau académique, il se peut que certains critères passent à la trappe alors qu'ils sont pertinents dans l'étude d'un classement. Certaines valeurs 'qualitatives' montrent que leur étude se doit d'être pertinente pour peut-être pouvoir proposer un différent type de classement. On comprend désormais mieux numériquement pourquoi certaines universités américaines, notamment celles de la `Ivy League` se distinguent mieux dans les sondages et médias par ce qu'elles représentent dans les scores en comparaison avec les autres universités.  








 

