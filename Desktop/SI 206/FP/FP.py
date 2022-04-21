import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import numpy as np

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
        
def calculations_and_visualizations(cur, conn, file): 
    cur.execute('''SELECT met_objects.object_enddate, met_objects.is_highlight FROM met_objects JOIN object_ids 
    ON met_objects.object_id = object_ids.id WHERE met_objects.is_highlight = ?''', (1,))
    conn.commit()
    lst = cur.fetchall()
    highlight_counts = {}
    count = 0
    total = 0
    for tup in lst:
        year = tup[0]
        total += year
        count += 1
        highlight_counts[year] = highlight_counts.get(year, 0) + 1
    avg = int(total/count)
    years = list(highlight_counts.keys())
    counts = list(highlight_counts.values())
    f = open(file, "w")
    f.write("The average year with the most highlighted 'activism' pieces was " + str(avg) + "\n")
    f.write("The total number of highlighted 'activism' items in this sample of 100 'activism' items was " + str(count))

    #plt.pie(counts, labels = years)
    # plt.bar(years, counts, color = "lightblue", width = 0.3)
    x1 = np.array(years)
    y1 = np.array(counts)
    plt.scatter(x1, y1)
    plt.xlabel("Year")
    plt.ylabel("Number of Highlighted Pieces")
    plt.title("Highlighted Pieces By Year at the Met")
    plt.show()
    #average year of when most activist pieces were created in a sample of 100 items at the met
    #count of highlights and which years had the most highlighted pieces 
    #make one more based on my data for EC

def main():
    db_filename = 'art.db'
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    add_to_database(cur, conn, "activism",'art.db', 0, 25)
    add_to_database(cur, conn, "activism",'art.db', 25, 50)
    add_to_database(cur, conn, "activism",'art.db', 50, 75)
    add_to_database(cur, conn, "activism",'art.db', 75, 100)
    calculations_and_visualizations(cur, conn, 'calculations.txt')



if __name__ == "__main__":
    main()
    
