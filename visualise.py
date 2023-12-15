import networkx as nx
import sqlite3
import igraph as ig
import os

# open db
conn = sqlite3.connect('sites.db')
cur = conn.cursor()

cur.execute('SELECT root_id, child_id FROM children')
data = cur.fetchall()

graph = nx.DiGraph()

for a, b in data:
    print(a, b)
    graph.add_edge(a, b)

comps = nx.weakly_connected_components(graph)

for i, comp in enumerate(comps):
    print(f"illustrating {i}")
    edges = graph.subgraph(comp).edges
    edges = [[str(a), str(b)] for a, b in edges]
    nodes = graph.subgraph(comp).nodes
    subgraph = ig.Graph()
    for j in nodes: subgraph.add_vertex(str(j))
    subgraph.add_edges(edges)

    ig.plot(subgraph, target=f'{i}.pdf',
            vertex_size=3,
            vertex_color=['blue', 'red', 'green', 'yellow'],
            edge_width=[1, 3],
            edge_color=['black', 'grey']
            )
