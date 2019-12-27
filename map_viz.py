from flask import Flask
import folium 
import pandas as pd
import numpy as np
import pickle
import pycountry
import json
from folium.map import *
from folium import plugins
from branca.colormap import linear

app = Flask(__name__)


@app.route('/')
def index():
    geo_str = 'geo_json_gpi.json'

    m = folium.Map(location=[48, -102], zoom_start=3)

    d = pickle.load(open('sent-alpha_3.p', 'rb'))
    df =  pd.DataFrame.from_dict(d, orient = 'index')
    df = df.reset_index()
    df = df.rename(columns={"index": "name", 0: "sentiment"})

    folium.Choropleth(
        geo_data=geo_str,
        name='choropleth',
        data=df,
        columns=['name', 'sentiment'],
        key_on='feature.properties.iso_a3',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Sentiment of News',
        highlight=True
    ).add_to(m)
    folium.LayerControl().add_to(m)

    Marker(location=[45.5, -122.3], popup='Portland, OR').add_to(m)

    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)