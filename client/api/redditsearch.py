
import requests
import json

from m.processTemplate import getTemp, make

hubsearch = getTemp('hubsearch')

def rsearch(q):
	subreddits = json.loads(requests.get('https://www.reddit.com/subreddits/search.json?q='+q, headers={'User-Agent': 'spider'}).content)['data']['children']
	res = ''
	lim = 4
	for sub in subreddits:
		if 'title' not in sub['data'] or 'url' not in sub['data']:
			continue
		if lim < 1:
			break
		res += make(hubsearch, {
								'add':	'x',
								'name':	sub['data']['title'],
								'url':	'https://www.reddit.com'+sub['data']['url'],
								'rssurl':	'https://www.reddit.com'+sub['data']['url']+'.rss'
								}, {})
		lim -= 1
	if res == '':
		return ''
	return res+'<div class="breack"></div>'
