
import web

from m.webinput import webinput
from m.processTemplate import getTemp, make

postTemp = getTemp('post')
feedpostsbarTemp = getTemp('feedpostsbar')



def makefeed(rows):
	posts = ''
	postbarposts = ''
	currpageid = -1
	lastro = {}
	for row in rows:
		if currpageid != row['pageid']:
			if postbarposts != '':
				posts += make( feedpostsbarTemp, lastro, {'posts':postbarposts, 'subscribe':'Subscribe'} )
			postbarposts = ''
			currpageid = row['pageid']
		postbarposts += make( postTemp, row, {} )
		lastro = row
	return posts + make( feedpostsbarTemp, lastro, {'posts':postbarposts, 'subscribe':'Subscribe'} )


def run(s,g):
	rows = g['db'].query("""
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
			    hub.contenttype='news' AND links.pageid=hub.id AND links.foundpublisheddate > now() - INTERVAL '2 DAY'
			ORDER BY
			    links.id DESC
		    ) x
		WHERE
		    row_number < 11
		ORDER BY CASE
    				WHEN id=49 THEN 1
    				WHEN id=18 THEN 2
    				WHEN id=22 THEN 3
    			END ASC, max(id) OVER (PARTITION  by pageid) DESC, id DESC
	""")

	return makefeed(rows)
