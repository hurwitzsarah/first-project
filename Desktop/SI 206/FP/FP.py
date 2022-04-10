import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

#def get_data(db_filename):
    # base_url_apple = "https://itunes.apple.com/search?"
    # params = {'term': 'jack johnson', 'media' : 'song', 'limit' : 20}
    # res = requests.get(base_url_apple, params)
    # data = json.loads(res.text)
    # return data

    # path = os.path.dirname(os.path.abspath(__file__))
    # conn = sqlite3.connect(path+'/'+db_filename)
    # cur = conn.cursor()


#def visualize_results(db_filename):
    # path = os.path.dirname(os.path.abspath(__file__))
    # conn = sqlite3.connect(path+'/'+db_filename)
    # cur = conn.cursor()

def call_api(artist):
    base_url_apple = "https://itunes.apple.com/search?"
    params = {'term': artist, 'mediaType' : 'song', 'limit' : 20, 'attribute' : 'allArtistTerm'}
    res = requests.get(base_url_apple, params)
    data = json.loads(res.text)
    json.dumps(data, indent = 4)
    song_list = []
    for dic in data['results']:
        title = dic['trackName']
        country = dic['country']
        song_list.append((title, country))
    return song_list

print(call_api('jack johnson'))
