import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_ids(cur, conn, query):
    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    p = {"q" : query}
    res = requests.get(search_url, params = p)
    data = json.loads(res.text)
    object_ids = data['objectIDs']
    cur.execute("CREATE TABLE IF NOT EXISTS object_ids (id INTEGER PRIMARY KEY, met_id INTEGER)")
    for i in range(len(object_ids)):
        cur.execute("INSERT OR IGNORE INTO object_ids (id,met_id) VALUES (?,?)",(i,object_ids[i]))
    conn.commit()
    return object_ids

def add_to_database(cur, conn, query, db_filename, start, end):
    cur.execute("CREATE TABLE IF NOT EXISTS met_objects (object_id INTEGER PRIMARY KEY, is_highlight TEXT, title TEXT, artist_name TEXT, object_enddate INTEGER, objectname TEXT, medium TEXT)")
    conn.commit()
    object_ids = get_ids(cur, conn, query)
    for id in object_ids[start:end]:
        try:
            object_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(id)
            res = requests.get(object_url)
            data = json.loads(res.text)
        except:
            return "Exception"
        for k, v in data.items():
            if v != '':
                object_id = int(data.get("objectID", 0))
                cur.execute("SELECT id FROM object_ids WHERE met_id = ?", (object_id,))
                id = int(cur.fetchone()[0])
                is_highlight = data.get("isHighlight", 0)
                title = data.get("title", 0)
                artist_name = data.get("artistDisplayName", 0)
                object_enddate = data.get("objectEndDate", 0)
                objectname = data.get("objectName", 0)
                medium = data.get("medium", 0)
                cur.execute('''INSERT or ignore INTO met_objects (object_id, title, artist_name, object_enddate, objectname, medium, is_highlight) 
                VALUES (?,?,?,?,?,?,?)''',(id, title, artist_name, object_enddate, objectname, medium, is_highlight))
                conn.commit()
        
def join_tables(cur, conn): #returns list of objects that were made after 1900 and are highlighted
    cur.execute('''SELECT met_objects.object_id, object_ids.met_id, met_objects.title, met_objects.artist_name, met_objects.object_enddate, met_objects.objectname, met_objects.medium, met_objects.is_highlight FROM met_objects JOIN object_ids 
    ON met_objects.object_id = object_ids.id WHERE met_objects.is_highlight = ? AND met_objects.object_enddate > ?''', (1, 1900))
    conn.commit()
    lst = cur.fetchall()
    count = 0
    for item in lst:
        count += 1
    return count

def main():
    db_filename = 'art_pieces.db'
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    add_to_database(cur, conn, "disease",'art_pieces.db', 0, 25)
    add_to_database(cur, conn, "disease",'art_pieces.db', 25, 50)
    add_to_database(cur, conn, "disease",'art_pieces.db', 50, 75)
    add_to_database(cur, conn, "disease",'art_pieces.db', 75, 100)
    join_tables(cur, conn)

if __name__ == "__main__":
    main()