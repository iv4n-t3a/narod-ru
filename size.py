import networkx as nx
import sqlite3
import os
import matplotlib.pyplot as plt

# open db
conn = sqlite3.connect('sites.db')
cur = conn.cursor()

cur.execute('SELECT root_id, child_id FROM children')
data = cur.fetchall()

graph = nx.Graph()

for a, b in data:
    graph.add_edge(a, b)

comps = nx.connected_components(graph)

state = {}

for i, comp in enumerate(comps):
    d = graph.subgraph(comp).size()
    if d in state: state[d] += 1
    else: state[d] = 1

state_list = []
state_heights = []

for i in state:
    while len(state_list) <= i:
        state_list.append(len(state_list))
        state_heights.append(0)
    state_heights[i] = state[i]

plt.plot(state_list, state_heights)
plt.show()