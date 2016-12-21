
import requests
import json

from m.inputfilter import furl, escapehtml
from m.processTemplate import getTemp, process

searchTemp = getTemp('hubsearch')

def run(s,g):
	if 'q' not in g['i'] or g['i']['q'] == '':
		return 'bad data'

	results = searchdict(g['i']['q'])

	print results

	ret = ''
	for res in results:
		ret += process(searchTemp, res, add=True)
	return ret

def searchdict(search):
	pg = requests.get('https://www.reddit.com/subreddits/search.json?q='+search, headers={'User-Agent': 'spider'}).content
	results = []
	bloglist = json.loads(pg)["data"]["children"]
	for blog in bloglist:
		results = addurl(results,blog['data'])
	return results

def addurl(r,dic):
	print dic

	url = furl('https://www.reddit.com'+dic['url'])
	if url == False:
		return r

	name = escapehtml(dic['display_name'])
	if name == '':
		return r

	icon = furl(dic['header_img']) if dic['header_img'] is not None else ''
	if icon == False:
		icon = ''

	r.append({
		'url': url+'.rss',
		'name': name,
		'icon': icon
	})
	return r
