import sqlite3
from urllib.parse import urlparse
import whois
import matplotlib.pyplot as plt

# open db
conn = sqlite3.connect('sites.db')
cur = conn.cursor()

cur.execute("SELECT url FROM pages")
pages = cur.fetchall()

state = {}
checked = set()

for url in pages:
    domain = urlparse(url[0]).netloc
    domain = '.'.join(domain.split('.')[-3:])
    if domain in checked: continue
    print(domain)
    checked.add(domain)
    year = str(whois.whois(url[0])["creation_date"])
    if year in state: state[year] += 1
    else: state[year] = 1

plt.bar(list(state), height=[state[i] for i in state])
plt.show()
