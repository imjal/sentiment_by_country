import requests
import pdb
import json
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pycountry
import pickle
import datetime

def print_sentiment_scores(sentence):
    print("{:-<40} {}".format(sentence, str(sentence)))
    print("\n")

def agg_title_descrip(a, b):
    if a is None: 
        a = ''
    elif b is None:
        b = ''
    return a + b

def get_country_sentiment(name, delta_days, sent_dict, lst_no_news):
    analyser = SentimentIntensityAnalyzer()
    url = ('https://newsapi.org/v2/everything?'
        f'q={name}&'
        f'from={str(datetime.date.today() - datetime.timedelta(days=delta_days))}&'
        'domains=bbc.com,usatoday.com,newsweek.com,buzzfeed.com,latimes.com,npr.org,washingtonpost.com,nytimes.com,cnn.com,news.yahoo.com,foxnews.com,reuters.com,politico.com,nbcnews.com,cbsnews.com,abcnews.go.com,chicagotribune.com&'
        'sortBy=relevancy&'
        'apiKey=309c2a965914436b8882b8deb6cde164')

    response = requests.get(url)
    d = response.json()
    scores = []
    try:
        if len(d['articles']) < 5:
            print(f'{name} has less than 5 articles in the last {delta_days} days')
            lst_no_news+=[name]
            return
        for x in d['articles']:
            sentence = agg_title_descrip(x['title'], x['description'])
            snt = analyser.polarity_scores(sentence)
            scores += [snt['compound']]
        sent_dict[name] = np.array(scores).mean()
        print(f"{name} has a score of {sent_dict[name]}")
    except KeyError: 
        print(f"Key Error for {name}.")
        pickle.dump(sent_dict, open("countries_sentiment.p", "wb" ))


if __name__ == "__main__":
    test = False
    try:
        d = {}
        countries = [country.name for country in pycountry.countries]
        lst_no_news = pickle.load(open('no_news_countries.p', 'rb'))
        country_lst = list(set(countries).difference(set(lst_no_news)))
        pdb.set_trace()
        delta_days = 28
        for country in country_lst if not test else country_lst[0:1]:
            get_country_sentiment(country, delta_days, d, lst_no_news)
        new_d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        print(d)
        pickle.dump(new_d, open("countries_sentiment.p", "wb" ))
        pickle.dump(lst_no_news, open("no_news_countries.p", "wb" ))
    except:
        pickle.dump(new_d, open("countries_sentiment.p", "wb" ))

     