#!/usr/local/bin/python

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag 

conn = sqlite3.connect('holoviews.docset/Contents/Resources/docSet.dsidx')
cur = conn.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'holoviews.docset/Contents/Resources/Documents/Reference_Manual'

directory = os.fsencode(docpath)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    page = open(os.path.join(docpath,filename)).read()
    soup = BeautifulSoup(page)
    for tag in soup.find_all('dt'):
        if not tag.attrs:
            continue
        name_ = list(tag.find('code', 'descname').stripped_strings)[0]
        type_ = tag.parent['class'][0].title()
        path_ = 'Reference_Manual/' + tag.find('a', 'headerlink')['href']
        cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES ('{}','{}','{}')".format(name_, type_, path_))
        print('type: {}, name: {}, path: {}'.format(type_, name_, path_))

conn.commit()
conn.close()
