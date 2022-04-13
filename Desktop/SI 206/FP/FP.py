import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest


def read_cache(filename):
    try:
        file = open(filename, 'r')
        data = json.loads(file.read())
        file.close()
        return data
    except:
        return {}

def write_cache(filename, cache_dic):
    written_cache_file = open(filename, 'w')
    json_cache_dict = json.dumps(cache_dic)
    written_cache_file.write(json_cache_dict)
    written_cache_file.close()

def get_ids(query):
    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    p = {"q" : query}
    res = requests.get(search_url, params = p)
    data = json.loads(res.text)
    #print(json.dumps(data, indent = 4))
    object_ids = data['objectIDs']
    return object_ids

def get_object_info(query):
    object_data_for_cache = []
    object_ids = get_ids(query)
    for id in object_ids:
        object_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(id)
        res = requests.get(object_url)
        data = json.loads(res.text)
        object_data_for_cache.append(data)
    

#print(get_ids("disease"))
get_object_info("disease")

# def get_data_with_caching():
#     cache_dic = read_cache(CACHE_FNAME)
#     if request_url in cache_dic:
#         print(f"Using cache for {term}")
#         return cache_dic[request_url]
#     else:
#         print(f"Fetching data for {term}")
#         try:
#             res = requests.get(request_url) 
#             data = json.loads(res.text)
#         except:
#             return "Exception"
#         if data['resultCount'] != 1:
#             print("Request not set correctly")
#             return None
#         else:
#             cache_dic[request_url] = data['results'][0]
#             write_cache(CACHE_FNAME, cache_dic) 
#             return data['results'][0]