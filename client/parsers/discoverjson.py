# -*- coding: utf-8 -*-

import web
import json

from m.getposthtml import getposts
#from m.functions import fixvals

def fixVals(row,ks):
	for k in ks:
		row[k] = str(row[k])
	return row

def run(s,g):
	output = []
	l = '5'
	s = '''SELECT hub.id hubid, hub.name, hub.url, max(links.id) linksid
		FROM links, hub
		WHERE links.pageId=hub.id
		GROUP BY hub.id
		ORDER BY linksid DESC LIMIT '''+l
	q = g['db'].query(s)
	for row in q:
		row = fixVals(row,['hubid','linksid','hueangle'])
		qi = g['db'].query('SELECT id, url, title, snipet, imgsrc FROM links WHERE pageId='+row['hubid']+' ORDER BY links.id DESC LIMIT 5')
		for ri in qi:
			for k in ri:
				if ri[k] is None:
					ri[k] = ''
			ri['name'] = row['name']
			output.append(ri)

	return json.dumps(output)
