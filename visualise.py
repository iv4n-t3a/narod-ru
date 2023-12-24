import sqlite3
import igraph as ig
import tqdm
from transliterate import translit

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText

# open db
conn = sqlite3.connect('sites.db')
cur = conn.cursor()

cur.execute('SELECT url, site_name, id FROM sites')
data = cur.fetchall()

for url, site, site_id in tqdm.tqdm(data):
    edges = []
    used = set()
    queue = [site_id]
    while queue:
        cur.execute(f'SELECT root_id, child_id FROM children WHERE root_id = {queue[-1]}')
        new_edges = cur.fetchall()
        queue.pop(-1)
        for edge in new_edges:
            edges.append(edge)
            used.add(edge[0])
            if edge[1] in used: continue
            queue.append(edge[1])
            used.add(edge[1])

    graph = ig.Graph()
    used_nodes = set()

    for i in edges:
        if not i[0] in used_nodes: graph.add_vertex(str(i[0]))
        if not i[1] in used_nodes: graph.add_vertex(str(i[1]))
        used_nodes.add(i[0])
        used_nodes.add(i[1])

    if len(edges) == 0:
        continue

    graph.add_edges([[str(a), str(b)] for a, b in edges])

    ig.plot(graph, target=f'vis/{site_id}.pdf',
            vertex_size=3,
            vertex_color=['blue', 'red', 'green', 'yellow'],
            edge_width=[1, 3],
            edge_color=['black', 'grey'],
            )

    pdf_path = f'vis/{site_id}.pdf'
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    writer = PdfWriter()
    writer.add_page(page)

    annotation = FreeText(
            text=f'{url}\n{translit(site, "ru", reversed=True)}',
            rect=(0, 0, 300, 50),
            font="Arial",
            bold=True,
            italic=True,
            font_size="40pt",
            font_color="000000",
            border_color="000000",
            background_color="ffffff",
            )

    writer.add_annotation(page_number=0, annotation=annotation)

    # Write the annotated file to disk
    with open(f"vis/{site_id}-with_name.pdf", "wb") as fp:
        writer.write(fp)
