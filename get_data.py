from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import requests


url = "https://datahub.io/core/geo-countries/r/countries.geojson"
r = requests.get(url, allow_redirects=True)
open('Data_Projet/countries.geojson', 'wb').write(r.content)


api = KaggleApi()
api.authenticate()

api.dataset_download_files('andradaolteanu/country-mapping-iso-continent-region', path='./')

with zipfile.ZipFile('country-mapping-iso-continent-region.zip', 'r') as zipref:
    zipref.extractall('Data_Projet/')

api.dataset_download_files('mylesoneill/world-university-rankings', path='./')

with zipfile.ZipFile('world-university-rankings.zip', 'r') as zipref:
    zipref.extractall('Data_Projet/')

