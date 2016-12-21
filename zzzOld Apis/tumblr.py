
import requests
from lxml import html
from lxml.cssselect import CSSSelector
import json

from m.inputfilter import furl, escapehtml
from m.processTemplate import getTemp, process

searchTemp = getTemp('hubsearch')

def run(s,g):
	if 'q' not in g['i'] or g['i']['q'] == '':
		return 'bad data'

	results = searchdict(g['i']['q'])

	ret = ''
	for res in results:
		ret += process(searchTemp, res, add=True)
	return ret

def searchdict(search):
	pg = requests.get('https://www.tumblr.com/search/'+search).content
	results = []
	bloglist = json.loads(html.fromstring(pg).cssselect('.tumblelogs_json')[0].get('data-search-tumblelogs-json'))
	for blog in bloglist:
		results = addurl(results,blog)
	return results

def addurl(r,dic):
	url = furl(dic['url'])
	if url == False:
		return r

	name = escapehtml(dic['title'])
	if name == '':
		return r

	icon = furl(dic['avatar_url'])
	if icon == False:
		icon = ''

	r.append({
		'url': url+'/rss',
		'name': name,
		'icon': icon
	})
	return r
