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
    dict_sentiment = df.set_index('name')['sentiment']

    colormap = linear.YlGn_09.scale(df.sentiment.min(), df.sentiment.max())
    fill_opacity=0.7
    line_opacity=0.2
    line_weight=1
    nan_fill_color='black'
    nan_fill_opacity=None

    def highlight_function(x):
        return {
            'weight': line_weight + 2,
            'fillOpacity': fill_opacity + .2
        }

    def color_scale_fun(feature):
        if feature['properties']['iso_a3'] is None:
            return nan_fill_color
        elif feature['properties']['iso_a3'] not in dict_sentiment: 
            return nan_fill_color
        return colormap(dict_sentiment[feature['properties']['iso_a3']])

    folium.GeoJson(
        data=geo_str,
        style_function=lambda feature: {
            'fillColor': color_scale_fun(feature),
            'color': 'black',
            'weight': 1,
            'dashArray': '5, 5',
            'fillOpacity': 0.9,
        },
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['name','gpi_score', 'gpi_rank'],
            aliases=['Country', 'Global Peace Index Score', 'Global Peace Index Rank'],
            localize=True,
            style=('background-color: grey; color: white; font-family: courier new; font-size: 24px; padding: 10px;')
        )
    ).add_to(m)
    folium.LayerControl().add_to(m)
    colormap.caption = 'Sentiment Color Scale'
    colormap.add_to(m)

    m

    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)