# -*- coding: utf-8 -*-

set_post_count = 8

import web

from m.processTemplate import getTemp, make
from m.inputfilter import num

from m.webinput import webinput


postTemp = getTemp('post')

def run(s,g):
	d = webinput(s,g,{'*setup':['needall'],'id':'fid'})
	if type(d) == str:
		return d
	linkid = d['id']

	relatedpostcount = 0
	posts = ''

	extra = {'frominfo':'frominfo'}

	q = g['db'].query("""
		SELECT links.*, hub.name hubname, hub.url huburl
		FROM links, linkstokeywords, hub
		WHERE links.id<>"""+linkid+""" AND hub.id=links.pageid AND links.id=linkstokeywords.linkid AND linkstokeywords.keywordsid IN (
			SELECT linkstokeywords.keywordsid
			FROM linkstokeywords
			WHERE linkstokeywords.linkid="""+linkid+"""
		)
		GROUP BY links.id, hub.id
		ORDER BY COUNT(*) DESC
		LIMIT """+str(set_post_count))
	for row in q:
		posts += make(postTemp, row, extra)
		relatedpostcount += 1

	if relatedpostcount >= set_post_count:
		return posts
	else:
		q = g['db'].query("SELECT posts.*, hub.name hubname, hub.url huburl from hub, links posts, links sameas where posts.pageid=sameas.pageid and sameas.id="+linkid+" and posts.id<>"+linkid+" and hub.id=posts.pageid ORDER BY posts.id DESC LIMIT "+str(set_post_count-relatedpostcount))
		for row in q:
			posts += make(postTemp, row, extra)

	return posts
