import sqlite3
import matplotlib.pyplot as plt

ALPHABET = 'abcdefghijklmnopqrstuvwxyzйцукенгшщзхъфывапролджэячсмитьбю'

bad_words = 'html http'.split()

def get_words_list(text : str):
    text = text.lower()
    words = ['']
    for i in text:
        if i in ALPHABET: words[-1] += i
        elif words[-1] != '': words.append('')
    return words

def get_words_state(words : list, avalible_state):
    state = avalible_state
    for i in words:
        if i in state: state[i] += 1
        else: state[i] = 1
    return state

def filter_words(words : list):
    new_words = []
    for w in words:
        if len(w) <= 3 or w in bad_words: continue
        new_words.append(w)
    return new_words

# can require optimisation
def get_most_popular_words(state : map, words_required : int):
    state_list = [[word, state[word]] for word in state]
    state_list.sort(key= lambda x : -x[1])
    res = []
    for count, item in enumerate(state_list):
        if count > words_required: return res
        res.append(item)
    return res

# open db
conn = sqlite3.connect('sites.db')
cur = conn.cursor()

cur.execute("SELECT plain_text FROM pages")
pages = cur.fetchall()

state = {}

for text in pages:
    words = get_words_list(text)
    words = filter_words(words)
    state = get_words_state(words, state)

most_popular = get_most_popular_words(state, 12)

plt.bar([i[0] for i in most_popular], height=[i[1] for i in most_popular])
plt.show()
