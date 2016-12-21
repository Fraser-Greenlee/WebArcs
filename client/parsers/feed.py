
import web
from string import Template

from m.webinput import webinput
from m.processTemplate import getTemp, make

postTemp = getTemp('post')
feedpostsbarTemp = getTemp('feedpostsbar')
contenttypeTemp = getTemp('contenttypebox')

def run(s,g):
	d = webinput(s,g,{'*setup':['loggedin'], 'filter':'fcontenttypes','more':'fid'})
	if type(d) == str:
		return d

	if 'more' in d:
		offby = str(int(d['more'])*12)
		lessthandate = "AND links.foundpublisheddate < now() - INTERVAL '"+str(int(d['more'])-1)+" DAY'"
	else:
		offby = 12
		lessthandate = ''
		lastseenid = g['db'].query("SELECT lasthistorycheck from users where id="+str(s.userid))[0]['lasthistorycheck']

	if 'filter' in d:
		posts = list(g['db'].query(Template("""
			SELECT
			    count(*) OVER (PARTITION by pageid), *
			FROM (
				SELECT
				    *
				FROM
				    (
					SELECT
					    row_number() OVER (PARTITION by links.pageid ORDER BY links.id DESC),
					    links.*,
					    hub.id hubid, hub.name hubname, hub.url huburl, domain, hub.contenttype
					FROM
					    links, subscriptions, hub
					WHERE
					    hub.contenttype='"""+d['filter']+"""' AND links.pageid=subscriptions.fid AND subscriptions.uid="""+str(s.userid)+""" AND hub.id=subscriptions.fid AND links.foundpublisheddate > now() - INTERVAL '$offby HOUR' $lessthandate
					ORDER BY
					    links.id DESC
				    ) x
				WHERE
				    ROW_NUMBER < 11
			) y
			ORDER BY max(id) OVER (PARTITION by pageid) desc, id desc
		""").substitute(offby=offby,lessthandate=lessthandate)))
	else:
		if 'more' not in d:
			posts = list(g['db'].query("""
				SELECT
				    *, count(*) OVER (PARTITION by pageid)
				FROM (
					SELECT
					    *, DENSE_RANK() OVER (PARTITION by contenttype ORDER BY mxid DESC) AS crc
					FROM
					    (
						SELECT
						    row_number() OVER (PARTITION by links.pageid ORDER BY links.id DESC),
						    links.*,
						    max(links.id) OVER (PARTITION by links.pageid) AS mxid,
						    hub.id hubid, hub.name hubname, hub.url huburl, domain, hub.contenttype
						FROM
						    links, subscriptions, hub
						WHERE
						    links.pageid=subscriptions.fid AND subscriptions.uid="""+str(s.userid)+""" AND hub.id=subscriptions.fid AND links.foundpublisheddate > now() - INTERVAL '12 HOUR' AND links.id > """+str(lastseenid)+"""
						ORDER BY
						    links.id DESC
					    ) x
					WHERE
					    ROW_NUMBER < 11
				) y
				WHERE
				    crc < 11
				ORDER BY
				    max(mxid) OVER (PARTITION by contenttype) DESC, mxid desc, id desc
			""")) + [False] + list(g['db'].query("""
				SELECT
				    *, count(*) OVER (PARTITION by pageid)
				FROM (
					SELECT
					    *, DENSE_RANK() OVER (PARTITION by contenttype ORDER BY mxid DESC) AS crc
					FROM
					    (
						SELECT
						    row_number() OVER (PARTITION by links.pageid ORDER BY links.id DESC),
						    links.*,
						    max(links.id) OVER (PARTITION by links.pageid) AS mxid,
						    hub.id hubid, hub.name hubname, hub.url huburl, domain, hub.contenttype
						FROM
						    links, subscriptions, hub
						WHERE
						    links.pageid=subscriptions.fid AND subscriptions.uid="""+str(s.userid)+""" AND hub.id=subscriptions.fid AND links.foundpublisheddate > now() - INTERVAL '1 DAY' AND links.id < """+str(lastseenid)+"""
						ORDER BY
						    links.id DESC
					    ) x
					WHERE
					    ROW_NUMBER < 11
				) y
				WHERE
				    crc < 11
				ORDER BY
				    max(mxid) OVER (PARTITION by contenttype) DESC, mxid desc, id desc
			"""))
		else:
			posts = list(g['db'].query(Template("""
				SELECT
				    *, count(*) OVER (PARTITION by pageid)
				FROM (
					SELECT
					    *, DENSE_RANK() OVER (PARTITION by contenttype ORDER BY mxid DESC) AS crc
					FROM
					    (
						SELECT
						    row_number() OVER (PARTITION by links.pageid ORDER BY links.id DESC),
						    links.*,
						    max(links.id) OVER (PARTITION by links.pageid) AS mxid,
						    hub.id hubid, hub.name hubname, hub.url huburl, domain, hub.contenttype
						FROM
						    links, subscriptions, hub
						WHERE
						    links.pageid=subscriptions.fid AND subscriptions.uid="""+str(s.userid)+""" AND hub.id=subscriptions.fid AND links.foundpublisheddate > now() - INTERVAL '$offby DAY' $lessthandate
						ORDER BY
						    links.id DESC
					    ) x
					WHERE
					    ROW_NUMBER < 11
				) y
				WHERE
				    crc < 11
				ORDER BY
				    max(mxid) OVER (PARTITION by contenttype) DESC, mxid desc, id desc
			""").substitute(offby=offby,lessthandate=lessthandate)))


	if 'more' not in d and 'filter' not in d and len(posts) != 0 and posts[0] != False:
		g['db'].query("UPDATE users set lasthistorycheck="+str(posts[0]['id'])+" WHERE id="+str(s.userid))

	if 'more' not in d and posts == [False]:
		return """
		<div class="msgbox">
			<h1>Welcome to <b>WebArcs</b></h1>
			<p>Browse all your favourite sites without clutter.</p>
			<p>Tap the Subscribe button to add sites to your feed.</p>
			<p class="linkholder"><a onclick="getstarted()">Get Started</a></p>
		</div>
		<end/>
		"""
	else:
		return makefeed(posts)

def makefeed(rows):

	sets = {
		'page':'',
		'contenttype':{'id':'','html':''},
		'pageid':{'id':-1,'html':''}
	}

	# add false end entry for loop
	rows.append({'pageid':'','contenttype':'','count':False})

	for row in rows:
		if row is False:
			# reset feed
			if sets['pageid']['html'] != '':
				sets['contenttype']['html'] += make( feedpostsbarTemp, lastrow, {'posts':sets['pageid']['html'], 'subscribe':'Subscribed'} )

			if sets['contenttype']['html'] != '':
					sets['page'] += make( contenttypeTemp, lastrow, {'posts':sets['contenttype']['html']} )

			if sets['page'] != '':
				sets['page'] += '<div class="split"></div>'

			sets = {
				'page':sets['page'],
				'contenttype':{'id':'','html':''},
				'pageid':{'id':-1,'html':''}
			}
			continue

		if row['pageid'] == sets['pageid']['id']:
			sets['pageid']['html'] += make( postTemp, row, {'subscribe':'Subscribed'} )

		else:

			if sets['pageid']['html'] != '':
				sets['contenttype']['html'] += make( feedpostsbarTemp, lastrow, {'posts':sets['pageid']['html'], 'subscribe':'Subscribed'} )
				sets['pageid']['html'] = ''
			sets['pageid']['id'] = row['pageid']

			if row['contenttype'] != sets['contenttype']['id']:
				if sets['contenttype']['html'] != '':
					sets['page'] += make( contenttypeTemp, lastrow, {'posts':sets['contenttype']['html']} )
					sets['contenttype']['html'] = ''
				sets['contenttype']['id'] = row['contenttype']

			if row['count'] == 1:
				sets['contenttype']['html'] += make( postTemp, row, {'frominfo':'x','subscribe':'Subscribed'} )
			else:
				sets['pageid']['html'] = make( postTemp, row, {'subscribe':'Subscribed'} )

		lastrow = row

	if sets['page'] == '':
		return '<end/>'
	else:
		return sets['page']
