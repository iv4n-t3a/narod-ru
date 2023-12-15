import networkx as nx
import sqlite3
import igraph as ig
import os

# open db
conn = sqlite3.connect('sites.db')
cur = conn.cursor()

cur.execute('SELECT url FROM sites')
data = cur.fetchall()

for url in data:
    print(url)
