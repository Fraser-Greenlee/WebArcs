
from urlparse import urlparse
import requests
from lxml import html
from lxml.cssselect import CSSSelector
import re

from m.inputfilter import furl, escapehtml
from m.processTemplate import getTemp, process

searchTemp = getTemp('searchpostsbar')

def innerHTML(e):
	return (e.text or '') + ''.join([html.tostring(child) for child in e.iterchildren()])

def run(s,g):
	if 'q' not in g['i'] or g['i']['q'] == '':
		return 'bad data'

	results = searchdict(g['i']['q'])

	ret = ''
	for res in results:
		ret += process(searchTemp, res, add=True)
	return ret

def searchdict(search):
	pg = requests.get('https://duckduckgo.com/html/?q='+search, headers={'User-Agent': 'WebArcs'}).content
	results = []
	bloglist = html.fromstring(pg).cssselect('.result')
	i = 0
	for blog in bloglist:
		results = addurl(i,results,blog)
		i += 1

	return rearange(results)


platforms = ['youtube.com','twitter.com','reddit.com','tumblr.com']
def rearange(r):
	sourcelist = []
	nr = []
	for row in r:
		if urlparse(row['huburl']).netloc.replace('www.','') in platforms:
			row['platform'] = True
			sourcelist.append(row)
		else:
			nr.append(row)
	return sourcelist + nr[:3]


def addurl(i,r,e):
	link = e.cssselect('a.result__url')[0]
	url = furl(link.get('href'))
	if url == False:
		return r

	name = innerHTML(e.cssselect('.result__a')[0])

	r.append({
		'huburl': url.replace("'","").replace('"',''),
		'hubname': re.sub('<.*?>','',name.replace("'","").replace('"','')),
		'hubid': i,
		'subscribe': 'Subscribe',
		'platform': False
	})
	return r
