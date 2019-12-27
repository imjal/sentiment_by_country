import requests
import lxml.html as lh
import pandas as pd
import pdb
import numpy as np
import pycountry
import json


url='https://en.wikipedia.org/wiki/Global_Peace_Index'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//*[@id="mw-content-text"]/div/div[4]/table/tbody/tr')

tbl = np.array(['name', 'rank', 'score'])

for tr in tr_elements:
    tbl = np.vstack((tbl,[tr[i].text_content().strip() for i in range(0, 3)]))

for i in range(1, len(tbl)):
    try:
        x = pycountry.countries.search_fuzzy(tbl[i][0])[0]
    except LookupError:
        if len(tbl[i][0].split()) == 1:
            x = pycountry.countries.search_fuzzy(tbl[i][0][:-1])[0]
        else:
            x = pycountry.countries.search_fuzzy(tbl[i][0].split()[1])[0]
    tbl[i][0] = x.alpha_3

d_name = {tbl[i][0]: list(tbl[i][1:]) for i in range(1, len(tbl))}

geo_str = 'shp/custom.geo.json'
j = json.load(open(geo_str, "rb"))

for i in range(len(j['features'])):
    key = j['features'][i]['properties']['iso_a3']
    if key in d_name: # query for the country code
        j['features'][i]['properties']['gpi_score'] = d_name[key][1]
        j['features'][i]['properties']['gpi_rank'] = d_name[key][0]
    else:
        j['features'][i]['properties']['gpi_score'] = 'N/A'
        j['features'][i]['properties']['gpi_rank'] = 'N/A'
json.dump(j, open('geo_json_gpi.json', 'w'))
