#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import urllib2
import re
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

def get_trans(url):
#page1 = urllib2.urlopen("http://bigbangtrans.wordpress.com/series-6-episode-01-the-date-night-variable/")
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, convertEntities=BeautifulSoup.HTML_ENTITIES)
	trans = []
	entry = soup("div", { "class" : "entrytext" })
	speeches = entry[0].findAll('p')
	for item in speeches:
		raw = repr(item) # unicode problem if using str(item)
		speech = re.sub(r'</?\w+[^>]*>','',raw)
		speech = speech.replace('’', '\'').replace('…', '...').replace('“', '"').replace('”', '"')
		trans.append(speech)
	return trans

def crawl_tbbt():
	page = urllib2.urlopen("http://bigbangtrans.wordpress.com")
	soup = BeautifulSoup(page, convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a', href=re.compile('^http://bigbangtrans.wordpress.com/series'))
	for item in items:
		name = item.contents[0]#.encode('utf8')
		url = item['href']
		obj = re.search(r'Series\s(\d)\sEpisode\s(\d+)', name)
		if obj:
			series = int(obj.group(1))
			episode = int(obj.group(2))
			if series == 6 and episode > 14:
				trans = get_trans(url)
				filename = 's%02de%02d' % (series, episode)
				filename += '.txt'
				print filename
				f = open(filename, 'w')
				print url
				f.write('\n'.join(trans))
				f.flush()
				f.close()


