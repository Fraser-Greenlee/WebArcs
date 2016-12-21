# -*- coding: utf-8 -*-

set_bar_max = '17'

import web

from m.webinput import webinput
from m.processTemplate import getTemp, make
from m.fixVals import fixVals

feedbarTemp = getTemp('feedbar')

def run(s,g):
	d = webinput(s,g,{'*setup':['loggedin'],'more':'fid'})
	if type(d) == str:
		return d

	if 'more' in d:
		return ''

	ret = ''
	q = g['db'].query("""
			SELECT
				hub.*
			FROM
				hub, subscriptions
			WHERE
				subscriptions.uid="""+str(s.userid)+""" AND subscriptions.fid=hub.id
			ORDER BY
				hub.name ASC
		""")
	for row in q:
		ret += make( feedbarTemp, fixVals(row), {'subscribe':'Subscribed'} )
	return '<end/>'+ret
