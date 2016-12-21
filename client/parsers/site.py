# -*- coding: utf-8 -*-

set_posts_per_load  = 10

import web

from m.webinput import webinput
from m.processTemplate import getTemp, make, convert

postTemp = getTemp('post')

def run(s,g):
	d = webinput(s,g,{'id':'fid','more':'fid'})
	if type(d) == str:
		return d

	if 'id' not in d:
		return '<end/>no id'
	id = d['id']

	if 'more' in d:
		offset = " OFFSET "+str(set_posts_per_load*int(d['more']))
	else:
		offset = ''
	ret = ''
	retcount = 0
	sql = "SELECT links.*, hub.name hubname, hub.url huburl FROM links, hub WHERE links.pageId="+id+" AND hub.id=links.pageId ORDER BY links.id DESC "+offset+" LIMIT "+str(set_posts_per_load)
	q = g['db'].query(sql)
	for row in q:
		ret += make(postTemp, row, {})
		retcount += 1

	if retcount < set_posts_per_load:
		return '<end/>' + ret
	else:
		return ret
