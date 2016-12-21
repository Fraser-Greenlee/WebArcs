
from application_only_auth import Client


client = Client("fRg1zVQg1GybnPzLtOOgRXzwv", "7rQbXkIMALJhjugqV6tfowWbf6lsRMpmTKW2ubllBX6y2cxhhn")

client.request('https://api.twitter.com/1.1/users/search.json?q=cat')

# ------------------


from application_only_auth import Client
from m.webinput import webinput
import random

def run(s,g):
	d = webinput(s,g,{'*setup':['loggedin','needall','print'],'name':'fstring'})
	if type(d) == str:
		return d

	name = d['name']

	client = Client("fVtL0r3tml6sRSJFtlfJfedbm", "629Gj3VjKJ9ih9dAj2bROm4nlrCWrhUojQqZqmLCttg9hmsrQk")

	friends = client.request('https://api.twitter.com/1.1/friends/list.json?cursor=-1&screen_name='+name+'&skip_status=true&include_user_entities=false')[u'users']
	print friends[0]
	for friend in friends:
		if g['db'].query("select count(*) from hub where rssurl='https://twitrss.me/twitter_user_to_rss/?user="+friend[u'screen_name']+"'")[0]['count'] == 0:
			id = g['db'].insert('hub', name=friend[u'name'],url="https://twitter.com/"+friend[u'screen_name'],rssurl="https://twitrss.me/twitter_user_to_rss/?user="+friend[u'screen_name'],rsstype=True,domain="twitter.com",hueangle=random.randint(0,359))
			g['db'].insert('refreshrate', arcid=id)
			g['db'].insert('subscriptions', uid=s.userid, fid=id)
	return 'v'


######


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
