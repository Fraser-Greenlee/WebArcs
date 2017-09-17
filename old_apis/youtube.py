
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
	pg = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&key=AIzaSyDhlnLQNBSy0tZ_S532jizptCCAPaJsNyc&q='+search).content
	results = []
	bloglist = json.loads(pg)["items"]
	for blog in bloglist:
		results = addurl(results,blog['snippet'])
	return results

def addurl(r,dic):
	print dic

	url = furl('https://www.youtube.com/feeds/videos.xml?channel_id='+dic['channelId'])
	if url == False:
		return r

	name = escapehtml(dic['channelTitle'])
	if name == '':
		return r

	icon = furl(dic['thumbnails']['medium']['url'])
	if icon == False:
		icon = ''

	r.append({
		'url': url+'.rss',
		'name': name,
		'icon': icon
	})
	return r
