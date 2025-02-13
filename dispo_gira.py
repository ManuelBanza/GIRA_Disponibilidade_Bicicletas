
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
import datetime
import time


# URL of the WFS data
url = "https://emel.city-platform.com/maps/wfs?REQUEST=GetFeature&typeNames=emel_gira_stations&outputFormat=application/json"

# Fetch the data
response = requests.get(url)
data = response.json()

# Convert features into a DataFrame
df = pd.json_normalize(data["features"])

# Extract latitude and longitude
df["longitude"] = df["geometry.coordinates"].apply(lambda x: x[0][0] if isinstance(x[0], list) else x[0])
df["latitude"] = df["geometry.coordinates"].apply(lambda x: x[0][1] if isinstance(x[0], list) else x[1])

# Remove unnecessary columns
df = df.drop(columns=["geometry.coordinates", "geometry.type", "type"])

# Rename columns to remove the "properties." prefix
df.columns = [col.replace("properties.", "") for col in df.columns]


# Exportar
from datetime import datetime
df.to_csv(datetime.now().strftime('data_sources/data_export/gira_disponibilidade_emel_opendata-%Y-%m-%d-%H-%M-%S.csv'), encoding='utf8', index=False)
