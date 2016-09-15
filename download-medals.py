#!/usr/bin/python
import os
import urllib2
import sqlite3
import urllib
from bs4 import BeautifulSoup

wiki = urllib2.urlopen('https://en.wikipedia.org/wiki/Awards_and_decorations_of_the_United_States_Armed_Forces');

soup = BeautifulSoup(wiki.read(), 'html.parser')

image_tags = soup.table.find_all('img')

titles = []
images = []
links = []

if not os.path.exists('images'):
	os.makedirs('images')

opener = urllib.URLopener()
for image_tag in image_tags:
	schema = image_tag['src'].replace('/thumb','').split('/')
	schema.pop()
	content = image_tag.parent.findNext('a')
	title = content.text
	link = content['href']
        image = 'https:'+ '/'.join(schema)
	titles.append(title)
	links.append(link)
	filename = image.split('/')[-1]
	opener.retrieve(image,'images/' + filename)
	images.append(filename)
	
conn = sqlite3.connect('ribbons.sqlite')
c = conn.cursor()

is_same_size = len(titles) == len(images) == len(links)
if is_same_size:
	for x in range(0,len(images)):
		c.execute('insert into ribbons(name,description,image) values(?,?,?)',[titles[x],links[x],images[x]])

c.execute('select count(id) from ribbons')

status_message = 'Download Successful!!'
if len(titles) != c.fetchone()[0]:
	status_message = 'Download Unsuccessful!!'
print status_message        

conn.commit()
conn.close()
