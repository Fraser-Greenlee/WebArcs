
import web
import requests
from urlparse import urlparse
from random import randint

from m.webinput import webinput

def run(s,g):
	d = webinput(s,g,{
			'*setup':['loggedin','print'],
			'id':'fid',
			'url':'furl'
		})
	if type(d) == str:
		return d

	if 'id' in d:

		data = list(g['db'].query("SELECT data from tempdatadump where id="+d['id']))

		if len(data) == 0:
			return 'bad data'

		data = data[0]['data'].split('<>')
		cols = {}
		i = 0
		for k in ['title','url','rssurl','rsstype']:
			cols[k] = data[i]
			i += 1

		if cols['rsstype']:
			cols['rsstype'] = 1
		else:
			cols['rsstype'] = 0

		fid = g['db'].insert('hub', name=cols['title'], url=cols['url'], hueangle=randint(0, 359), rssurl=cols['rssurl'], checktype=cols['rsstype'], domain=urlparse(cols['url']).netloc)
		g['db'].insert('refreshrate', arcid=fid)
		g['db'].insert('subscriptions', uid=s.userid, fid=fid)

		return 'v'

	elif 'url' in d:

		

	else:
		return 'bad data'
