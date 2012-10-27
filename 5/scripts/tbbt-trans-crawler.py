# -*- coding: utf-8 -*- 
import urllib2
import re
from bs4 import BeautifulSoup, Tag, NavigableString

def get_trans(url):
#page1 = urllib2.urlopen("http://bigbangtrans.wordpress.com/series-6-episode-01-the-date-night-variable/")
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page)
	trans = []
	entry = soup("div", { "class" : "entrytext" })
	speeches = entry[0].findAll('p')
	for item in speeches:
		raw = repr(item)
		speech = re.sub(r'</?\w+[^>]*>','',raw)
		speech = speech.replace('’', '\'').replace('…', '...').replace('“', '"').replace('”', '"')
		trans.append(speech)
	return trans


page = urllib2.urlopen("http://bigbangtrans.wordpress.com")
soup = BeautifulSoup(page)
for item in soup("li", { "class" : "page_item" }):
	a = item.findAll('a')[0]
	name = a.contents[0].encode('utf8')
	url = a['href']
	obj = re.search(r'Series\s(\d)\sEpisode\s(\d+)', name)
	if obj:
		series = int(obj.group(1))
		episode = int(obj.group(2))
		if series == 6 and episode == 3:
			trans = get_trans(url)
			filename = 's%02de%02d' % (series, episode)
			filename += '.txt'
			print filename
			f = open(r'../storage/tbbtsubfile/' + filename, 'w')
			print url
			f.write('\n'.join(trans))
			f.flush()
			f.close()
