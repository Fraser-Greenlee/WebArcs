
import web
from string import Template

from m.webinput import webinput
from m.processTemplate import getTemp, make
from m.allcontenttypes import contenttypes

postTemp = getTemp('post')
feedpostsbarTemp = getTemp('feedpostsbar')
contenttypeTemp = getTemp('contenttypebox')

def run(s,g):
	d = webinput(s,g,{'filter':'fcontenttypes','more':'fid'})
	if type(d) == str:
		return d

	if 'more' in d:
		more = d['more']
	else:
		more = '1'

	if s.get('userid',0) != 0:
		notinsubtable = "links.pageid NOT IN (SELECT fid from subscriptions where subscriptions.uid="+str(s.userid)+") AND "
	else:
		notinsubtable = ""

	if 'filter' in d:
		posts = g['db'].query(Template("""
				SELECT
				    *
				FROM
				    (
					SELECT
					    row_number() OVER (PARTITION by links.pageid ORDER BY links.id DESC),
					    links.*,
					    hub.id hubid, hub.name hubname, hub.url huburl, domain
					FROM
					    links, hub
					WHERE
					    $notinsubtable hub.contenttype='$contenttype' AND links.pageid=hub.id AND """+ ("links.foundpublisheddate > now() - INTERVAL '1 DAY'" if more == '1' else "links.foundpublisheddate > now() - INTERVAL '"+more+" DAY' AND links.foundpublisheddate < now() - INTERVAL '"+str(int(more)-1)+" DAY'") +"""
					ORDER BY
					    links.id DESC
				    ) x
				WHERE
				    ROW_NUMBER < 11
				ORDER BY max(id) OVER (PARTITION  by pageid) DESC, id DESC
		""").substitute(notinsubtable=notinsubtable, more=more, contenttype=d['filter']))
		return makefilterfeed(d['filter'], posts)
	else:
		posts = g['db'].query(Template("""
			SELECT
			    *
			FROM (
				SELECT
				    DENSE_RANK() OVER (PARTITION by contenttype ORDER BY maxid DESC) AS ctypc, *
				FROM
				    (
					SELECT
					    max(links.id) OVER (PARTITION by pageid) AS maxid,
					    row_number() OVER (PARTITION by links.pageid ORDER BY links.id DESC),
					    links.*,
					    hub.id hubid, hub.name hubname, hub.url huburl, domain, hub.contenttype
					FROM
					    links, hub
					WHERE
					    $notinsubtable links.pageid=hub.id
					ORDER BY
					    links.id DESC
				    ) x
				WHERE
					"""+ ('ROW_NUMBER < 11' if more=='1' else 'ROW_NUMBER < '+str(11*int(more))+' AND ROW_NUMBER > '+str(11*(int(more)+1))) +"""
			) y
			WHERE
			    ctypc < 4
			ORDER BY max(id) over (PARTITION by contenttype) DESC, maxid, id DESC
		""").substitute(notinsubtable=notinsubtable))
		return makefeed(posts)

def makefeed(rows):
	if len(rows) < 1:
		return '<end/>'

	html = ''
	contentposts = ''
	postbarposts = ''
	currpageid = -1
	currtyp = ''
	lastro = {}

	for ro in rows:
		if currpageid != ro['pageid']:
			if postbarposts != '':
				contentposts += make( feedpostsbarTemp, lastro, {'posts':postbarposts, 'subscribe':'Subscribe'} )
			postbarposts = ''
			currpageid = ro['pageid']

		if currtyp != ro['contenttype']:
			if contentposts != '':
				html += make( contenttypeTemp, {'posts':contentposts,'contenttype':currtyp,'crc':10}, {} )
			contentposts = ''
			currtyp = ro['contenttype']

		postbarposts += make( postTemp, ro, {} )
		lastro = ro

	return html + make( contenttypeTemp, { 'posts':(contentposts + make(feedpostsbarTemp, ro, {'posts':postbarposts, 'subscribe':'Subscribe'})), 'contenttype':currtyp,'crc':10}, {} )


def makefilterfeed(contenttype,rows):
	if len(rows) < 1:
		return '<end/>'

	contentposts = ''
	postbarposts = ''
	currpageid = -1
	lastro = {}

	for ro in rows:
		if currpageid != ro['pageid']:
			if postbarposts != '':
				contentposts += make( feedpostsbarTemp, lastro, {'posts':postbarposts, 'subscribe':'Subscribe'} )
			postbarposts = ''
			currpageid = ro['pageid']
		postbarposts += make( postTemp, ro, {} )
		lastro = ro
	contentposts += make( feedpostsbarTemp, lastro, {'posts':postbarposts, 'subscribe':'Subscribe'} )

	return make( contenttypeTemp, {'posts':contentposts,'contenttype':contenttype}, {} )
