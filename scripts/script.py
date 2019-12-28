import pycountry
import pickle

d = pickle.load(open('countries_sentiment.p', 'rb'))
new_d = {}
for k, v in sorted(d.items()):
    new_d[pycountry.countries.get(name=k).alpha_3] = v
pickle.dump(new_d, open("sent-alpha_3.p", "wb" ))