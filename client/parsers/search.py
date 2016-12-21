
import web

from m.webinput import webinput
from m.processTemplate import getTemp, make
from api.redditsearch import rsearch

hubsearch = getTemp('hubsearch')

def run(s,g):
	d = webinput(s,g,{'*setup':['needall'],'search':'fstring'})
	if type(d) == str:
		return d

	if s.get('userid',0) != 0:
		loggedin = True
		subs = []
		q = g['db'].query("SELECT fid from subscriptions where uid="+str(s.userid))
		for ro in q:
			subs.append(ro['fid'])
	else:
		loggedin = False

	q = d['search'].split()

	if len(q) == 1:
		urls = list(g['db'].query("SELECT * FROM (SELECT similarity('"+q[0]+"',url) sim, * FROM hub ORDER BY sim DESC LIMIT 10) x WHERE sim > 0.1"))
		if len(urls) == 0 or urls[0]['sim'] < 1:
			names = g['db'].query("SELECT * FROM (SELECT similarity('"+q[0]+"',name) sim, * FROM hub ORDER BY sim DESC LIMIT 10) x WHERE sim > 0.1")

		hubsims = {}
		hubdata = {}
		for hub in urls:
			hubdata[hub['id']] = hub
			if hub['sim'] in hubsims:
				hubsims[hub['sim']].append(hub['id'])
			else:
				hubsims[hub['sim']] = [hub['id']]
		for hub in names:
			if hub['id'] in hubdata:
				if len( hubsims[hubdata[hub['id']]['sim']] ) == 1:
					del hubsims[hubdata[hub['id']]['sim']]
				else:
					del hubsims[hubdata[hub['id']]['sim']][hubsims[hubdata[hub['id']]['sim']].index(hub['id'])]
				hubdata[hub['id']]['sim'] += hub['sim']
			else:
				hubdata[hub['id']] = hub
			if hubdata[hub['id']]['sim'] in hubsims:
				hubsims[hubdata[hub['id']]['sim']].append(hub['id'])
			else:
				hubsims[hubdata[hub['id']]['sim']] = [hub['id']]

		hubsims.keys().sort(reverse=True)

		subed = {'subscribe':'Subscribed'}
		sub = {'subscribe':'Subscribe'}
		ret = ''
		for sim in hubsims:
			for id in hubsims[sim]:
				if loggedin and id in subs:
					ret += make( hubsearch, hubdata[id], subed )
				else:
					ret += make( hubsearch, hubdata[id], sub )
		return rsearch(" ".join(q))+ret
