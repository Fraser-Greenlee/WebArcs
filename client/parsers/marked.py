# -*- coding: utf-8 -*-

set_posts_per_load  = 10

import web

from m.inputfilter import num

from m.webinput import webinput
from m.processTemplate import getTemp, make

postTemp = getTemp('post')

def run(s,g):
	d = webinput(s,g,{'*setup':['loggedin'],'type':'markedtype','more':'fid'})
	if type(d) == str:
		return '<end/>'+d

	if 'type' not in d:
		print 'No type sent'
		return '<end/> No type sent.'

	if 'more' in d:
		offset = " OFFSET "+str(set_posts_per_load*int(d['more']))
	else:
		offset = ""

	ret = ''
	retcount = 0

	if d['type'] == 'history':
		sql = """
				SELECT
					links.*, hub.name hubname, hub.url huburl
				FROM
					links, hub, history
				WHERE
					history.userid="""+str(s.userid)+""" AND links.id=history.linkid AND hub.id=links.pageid
				ORDER BY
					history.id DESC
				"""+offset+"""
				LIMIT
				    """+str(set_posts_per_load)
	else:
		sql = """
				SELECT
					links.*, hub.name hubname, hub.url huburl
				FROM
					links, responces, hub
				WHERE
					responces.userid="""+str(s.userid)+""" and responces.responce='"""+d['type']+"""' and links.id=responces.linkid AND hub.id=links.pageid
				ORDER BY
					responces.linkid DESC
				"""+offset+"""
				LIMIT """+str(set_posts_per_load)
	q = g['db'].query(sql)
	for row in q:
		ret += make(postTemp, row, {})
		retcount += 1

	if retcount < set_posts_per_load:
		return '<end/>' + ret
	else:
		return ret
