# INTRODUCTION
Le projet ici que nous avons réalisé est l'étude des données concernant le classement mondial des 100 meilleures universités. 

Le dataset de départ comporte des sous notations de l'école sur plusieurs années concernant comme par exemple l'éducation, les recherches effectuées ou encore le score total de l'université. D'autres données ont également été utiles pour un différent type d'étude géographique comme la répartition d'étudiants internationaux ou encore le rapport femme/homme en moyenne dans chaque pays. 

# INSTALLATION ET UTILISATION DES FICHIERS

## Installation de Git et récupération des fichiers

Verifiez tout d'abord que vous avez installé [Git](https://git-scm.com/) pour la récupération des fichiers

Nous allons maintenant cloner le projet dans le répertoire de votre choix. Pour cela, cliquez sur votre répertoire et faîtes clique-droit `Git Bash Here`

IMAGE

Une fois Git Bash ouvert, nous allons cloner le répertoire en ligne où se trouve le projet. Cliquez sur le bouton `Clone or Download` et copiez l'adresse HTTPS du [répertoire](https://git.esiee.fr/duongh/python-pour-la-data-science.git).
Une fois copié, retournez dans Git Bash et tapez la commande `git clone` https://git.esiee.fr/duongh/python-pour-la-data-science.git et cela vous donnera un accès de téléchargement au répertoire.
Finalement, tapez la commande `git pull` et vous aurez à votre disposition tous les fichiers du projet. 


## Comprendre les fichiers

Une fois les fichiers récupérés, pas mal de dossiers vont apparaître. Seuls certains concernent la version finale du projet:
- le fichier [`main.py`](url_final) qui sera la base de notre étude et l'ensemble des données affichés
- le dossier `Data_Projet` contenant les [datasets](https://www.kaggle.com/mylesoneill/world-university-rankings) (jeux de données) utilisées au format `csv`, un fichier [continent](https://www.kaggle.com/andradaolteanu/country-mapping-iso-continent-region) ainsi qu'un fichier [`GeoJSON`](https://datahub.io/core/geo-countries#resource-countries) pour la représentation géographique
- le dossier `assets`pour l'image de la page (représentant notre école :) )


# USER'S GUIDE

## Installation des packages nécessaires

Verifiez tout d'abord si vous disposez de la bonne version de Python. Pour cela:
- ouvrir l'invite de commande cmd de Windows (Windows+R, puis tapez cmd)
- dans l'invite de commandes tapez la commande `python --version`
- vérifiez si la version est à jour, de préférence la version `3.9.7`

Certains packages seront également nécessaires à installer pour la bonne utilisation du dash si cela n'est pas déjà fait:
- les packages d'operation classiques Numpy et Pandas: `pip install numpy` `pip install pandas`
- le package Dash pour l'initialisation de la page: `pip install dash`
- les packages permettant de visualiser correctement les graphiques: `pip install folium` 

Une fois les packages obtenus, pour afficher notre dashboard, il faudra donc exécuter sur l'invite de commandes le fichier `main.py`avec la commande `python main.py` avec en référence dans le même répertoire tous les dossiers nécessaires à l'exécution cités au-dessus. 

## Fonctionnement du Dashboard

Une fois le fichier lancé, le terminal va fournir une adresse url local, ici `http://127.0.0.1:8050/`. Cliquez sur ce lien va nous renvoyer vers notre navigateur par défaut et charger le dashboard. 

Une fois la page cherchée, vous pourrez apercevoir 3 onglets à parcourir nommés respectivement `Diagram and World Ranking`, `Histogram` et `World Map` qui contiennent chacun différent type de graphique représentant notre dataset. 

Sur chacun de ces onglets, vous verrez une barre verticale appelée `Year`qui permettra de changer l'année des données étudiées pour plus de précision.

Dans le premier onglet, vous avez 2 représentations graphiques: un diagramme sur les données de la dataset et un tableau représentant les 10 Meilleures universités en fonction du rang sur chaque année. 

Dans le deuxième onglet, nous avons utilisé les données de la première moitié des données du data set afin d'en faire un histogramme donnant une approche d'étude plus numérique. On aura donc à disposition sur l'histogramme les valeurs allant de 0 à 100, ainsi que leurs effectifs moyens.
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

S'en suit la création de la DataFrame, nous avons du renommer certains noms de colonnes pour pouvoir 'merge' les fichiers entre eux, ainsi que certains noms de cellule. On a appelé cette DataFrame `full_data`, qui contiendra toutes les informations de notre Dashboard qui décortiquera pour les adapter aux différents aspects de la page. 


Interessons-nous maintenant à l'instanciation des variables. Il nous a tout d'abord fallu créer plusieurs sous-colonnes car chaque onglet étudie différentes colonnes. De la même facon, nous avons du créer plusieurs sous-Dataframes nommées `df_tab` pour la DataFrame du tableau à classement et `df_map`, DataFrame contenant les données de la carte de l'onglet `World Map`. 

Pour `df_tab`, on a modifié le caractère classement pour avoir une valeur numérique et on a trié en fonction de ce-dernier et d'en afficher les 60 premieres cases, 5 étant les noms des colonnes et 5 x 10 pour les 10 premières écoles.  

Concernant `df_map`, la structure de cette DataFrame est un peu différente du reste, il fallait appliquer pas mal d'opération pour pouvoir afficher une donnée sur la carte en fonction de l'année et du type choisie. On a tout d'abord extrait les colonnes `country, year` et supprimer les duplicats.
En fonction du type et du calcul voulu, on applique la fonction `groupby()` et on insère ces valeurs dans une colonne de la sous-Dataframe. 

## Page HTML du Dashboard

Maintenant que l'initialisation du `back-end` du Dashboard est créé, il nous faut la partie `front-end` de la page. 
Nous avons utilisé la structure classique d'un fichier HTML en travaillant les fonctions `Div()`, les titres `H1() H2()` et des labels, mais l'information qui sera affiché vient des fonctionalités du package `dash-core-components`, où on pourra retrouver pas mal de widgets comme une liste déroulante, un slider d'année, une représentation de tableau `DataTable` et des représentation de graphes, qui seront définis dans la partie suivante en utilisant l'id du widget.

## Callback et affichage des données

Une fois l'esthétique de la page faite, il faut maintenant la remplir d'information. Dash dispose d'une fonctionnalité pemettrant de rappeler les élements de la page et de leur fournir des informations en fonction des valeurs qu'on donnera en entrée. 

Nous allons nous interesser au premier et troisième onglet qui ont un nombre conséquent `d'input_values` pour gérer les affichages graphiques.

Comme on l'a vu dans le User's Guide, le premier onglet contient un diagramme et un tableau de classement. Le diagramme comme on a pu le tester, a une possibilité de 3 entries possibles: l'abscisse, l'ordonnée et l'année, tandis que le tableau n'en a qu'une seule: l'année. 

On va donc callback l'id de la liste déroulante de x et y, ainsi que le slider de l'année. 
On utilise la méthode query pour définir une data_year qui va sélectionner les données en fonction de l'année et on prend les input_values pour tracer le diagramme. Les variables et fonctions du tableau étant déjà faites en global, on a plus qu'a retourner sa valeur en précisant l'année en input_value. 

Le troisième onglet va utiliser le package folium, notamment le style Choropleth pour représenter les pays sur la carte. Ce que l'on modifier sur la page est l'année choisie et le type choisie, qui seront les input_value dans le callback avec la Map comme output.
On répète le même processus, on va query l'année dans la sous-dataframe et notre jeu de données est prêt. 

Pour tracer les pays sur la map, on a besoin de l'aide d'un fichier GeoJSON nommé `data_country` contenant l'ensemble des coordonnées et de leur contour. Il faut rechercher dans ce fichier l'expression en question similaire à notre colonne 'country' pour matcher les contours, ces données se trouvant dans le chemin `properties.ADMIN`. En y ajoutant les autres paramètres notamment la gamme de couleurs d'intensité des valeurs, on retourne ces informations dans un fichier `map.html`, qui sera lancé par la fonction Iframe de la page HTML.

# RAPPORT D'ANALYSE









 

