from flask import Flask, render_template
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

def index():
    geo_str = 'data/geo_json_gpi.json'

    m = folium.Map(location=[48, -102], zoom_start=3)

    d = pickle.load(open('data/sent-alpha_3.p', 'rb'))
    df =  pd.DataFrame.from_dict(d, orient = 'index')
    df = df.reset_index()
    df = df.rename(columns={"index": "name", 0: "sentiment"})
    dict_sentiment = df.set_index('name')['sentiment']

    colormap = linear.YlGn_09.scale(df.sentiment.min(), df.sentiment.max())
    peace_colormap = linear.PuRd_08.scale(0, 4)
    align_colormap = linear.RdBu_10.scale(0, 6)
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

    def peace_color_scale_fun(feature):
        if feature['properties']['iso_a3'] is None:
            return nan_fill_color
        if feature['properties']['gpi_score'] == 'N/A':
            return nan_fill_color
        return peace_colormap(feature['properties']['gpi_score'])

    def align(gpi_score, sentiment):
        return (gpi_score - sentiment)**2

    def alignment_peace_sentiment(feature):
        if feature['properties']['iso_a3'] is None:
            return nan_fill_color
        elif feature['properties']['iso_a3'] not in dict_sentiment: 
            return nan_fill_color
        if feature['properties']['gpi_score'] == 'N/A':
            return nan_fill_color
        return align_colormap(align(feature['properties']['gpi_score'], dict_sentiment[feature['properties']['iso_a3']]))
    
    folium.GeoJson(
        data=geo_str,
        style_function=lambda feature: {
            'fillColor': alignment_peace_sentiment(feature),
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
        ), 
        show=True,
        name = "Similarity of Global Peace Index"
    ).add_to(m)
    align_colormap.caption = 'Alignment of Sentiment and Peace Index'
    align_colormap.add_to(m)

    folium.GeoJson(
        data=geo_str,
        style_function=lambda feature: {
            'fillColor': peace_color_scale_fun(feature),
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
        ),
        overlay=True,
        show=False,
        name = "Global Peace Index"
    ).add_to(m)
    peace_colormap.caption = 'Global Peace Index'
    peace_colormap.add_to(m)
    
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
        ), 
        overlay=True,
        show=False,
        name = "News Sentiment"
    ).add_to(m)
    folium.LayerControl().add_to(m)
    colormap.caption = 'Sentiment Color Scale'
    colormap.add_to(m)

    m.save('templates/map.html')

@app.route('/')
def run_app():
    index()
    return render_template('home.html')
    
if __name__ == "__main__":
    app.run(debug=True)