import requests
import lxml.html as lh
import pandas as pd
import pdb
import numpy as np


url='https://en.wikipedia.org/wiki/Global_Peace_Index'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//*[@id="mw-content-text"]/div/div[4]/table/tbody/tr')

tbl = np.array(['name', 'rank', 'score'])

for tr in tr_elements:
    tbl = np.vstack((tbl,[tr[i].text_content().strip() for i in range(0, 3)]))

df = pd.DataFrame(tbl)
new_header = df.iloc[0]
df = df[2:] 
df.columns = new_header
df = df.set_index('rank')
print(df)