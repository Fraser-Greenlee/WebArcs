# -*- coding: utf-8 -*-

colToProp = {
	'snipet':['og:description','og:title','twitter:title'],
	'imgsrc':['og:image']
}

import web
from lxml import etree
from io import StringIO
import requests
import re
import time
import sys
from random import randint
from nltk.stem.porter import *
stemmer = PorterStemmer()

from m.dbconx import db
from m.inputfilter import escapehtml, furl
from m.scrapertools import cutStr
from m.stopwords import stopwords

def linkError(ex,linenum,row):
	ex = escapehtml(str(ex))[:255]
	print ex

	if 'url' in row:
		url = row['url']
	else:
		url = 'no url'

	db.query("INSERT INTO errorindexinglink (linenumber,exception,url) VALUES ('"+str(linenum)+"','"+ex+"','"+url+"')")
	db.query("DELETE from linkstobeindexed where id="+str(row['id']))

def strDict(d):
	for k in d:
		if isinstance(d[k], str) == False and isinstance(d[k], unicode) == False:
			if d[k] == None or d[k] == False:
				d[k] = "''"
			else:
				d[k] = str(d[k])
		else:
			d[k] = "'"+d[k]+"'"
	return d

def validkwd(wd):
	return len(wd) <= 32 and len(wd) > 1

def domain(url):
	nohttp = url[ url.index('://')+3: ]
	if '/' in nohttp:
		return nohttp[ 0:nohttp.index('/') ]
	else:
		return nohttp

def convert(rowt):
	for s in [('arcid','pageid'),('dateadded','postdate')]:
		rowt[s[1]] = rowt[s[0]]
		del rowt[s[0]]
	rowt['title'] = rowt['title'].encode("utf-8")
	return rowt

def filt(val, atr, typ, db):
	print val, atr, typ
	if val is None or val == []:
		print 'none'
		return ''
	if atr == '$text':
		val = val[0].text
	else:
		val = val[0].attrib[atr]
	if val in [None,'',False]:
		print 'val none'
		return ''
	if typ == 'snipet':
		val = cutStr(escapehtml(val), 255)
	elif typ == 'imgsrc':
		val = furl(val).strip()
		if val is False or len(val) > 255 or db.query("SELECT count(*) FROM links WHERE imgsrc='"+val+"'")[0]['count'] > 0:
			return ''
	return val.strip()

def run():
	q = db.query("""
		SELECT
			hub.domain, linkstobeindexed.id, dateadded, arcid, linkstobeindexed.url, title, snipet, imgsrc, indexing, comments
		FROM
			linkstobeindexed, hub
		WHERE
			indexing=FALSE AND arcid=hub.id
		ORDER BY
			id ASC
		LIMIT
			48
	""")
	# duplicate in memory
	q = list(q)
	if len(q) == 0:
		# restart inexing posts left for over 10mins
		if randint(0,4) == 4:
			db.query("""UPDATE
							linkstobeindexed
						SET
							indexing=FALSE
						WHERE
							id IN (
								SELECT id FROM (
									SELECT id, EXTRACT(EPOCH FROM (now() - dateadded))/60 AS addeddiff FROM linkstobeindexed
								) x WHERE addeddiff > 600
							)""")
		return ''

	whrs = ''
	for row in q:
		whrs += 'id='+str(row['id'])+' OR '
	db.query('UPDATE linkstobeindexed set indexing=true where '+whrs[:-4])
	endq = 'UPDATE linkstobeindexed set indexing=false where '+whrs[:-4]


	try:
		for row in q:
			ogrow = dict((k,v) for k,v in row.items())
			# pause so not blocked by reddit
			time.sleep(5)

			row = convert(row)
			text = requests.get(row['url'], headers={'User-Agent': 'spider'})

			if text.headers['content-type'].lower().replace(' ','').split(';')[0] != 'text/html':
				print text.headers['content-type']
				db.query("INSERT INTO error (href,hreforigin,pageid) VALUES ('"+row['url']+"','content-type:"+text.headers['content-type']+"',"+str(row['pageid'])+")")
				db.query("DELETE from linkstobeindexed where id="+str(row['id']))
				continue

			# <!--?xml version="1.0" encoding="UTF-8"?-->

			text = re.sub(r"\?xml(.*)\?", "", text.text)
			try:
				text.decode('utf-8')
			except UnicodeError:
				text = text.encode("utf-8")

			head = etree.HTML(text)

			for t in ['imgsrc','snipet']:
				# no images from Hacker News or soundcloud feeds
				if row['pageid'] == 49 and t == 'imgsrc':
					continue
				for key in colToProp[t]:
					row[t] = filt(head.xpath('//meta[@property="'+key+'"][@content]'), 'content', t, db)
					if row[t] != '':
						break

			if row['snipet'] == '':
				row['snipet'] = filt(head.xpath('//description'), '$text', 'snipet', db)
				if row['snipet'] == '':
					row['snipet'] = domain(row['url'])
					if row['snipet'] in	[row['domain'],'www.'+row['domain']]:
						row['snipet'] = ''

			toBeIndexedId = row['id']
			del row['id']

			lastLinkId = db.insert(
				'links',
				pageid = row['pageid'],
				url = row['url'],
				title = row['title'],
				snipet = row['snipet'],
				imgsrc = row['imgsrc'],
				postdate = row['postdate'],
				comments = row['comments']
			)
			print 'insert', row
			db.query("DELETE FROM linkstobeindexed WHERE id='"+str(toBeIndexedId)+"'")

			# get non-stop words from each title
			linksToKwdsVals = ''
			#	|remove duplicates|
			kwds = sorted(set(list(set([stemmer.stem(plural) for plural in re.sub("[^a-z0-9 ]", ' ',  re.sub('&.*?;','',row['title']).lower()).replace('  ',' ').split(' ')]) - stopwords)))

			i = 0
			toDel = []
			whrs = ''
			for kwd in kwds:
				if validkwd(kwd):
					whrs = whrs + "string='"+kwd+"' OR "
				else:
					toDel.append(kwd)
				i = i + 1
			for d in toDel:
				del kwds[kwds.index(d)]

			q = db.query("SELECT id, string FROM keywords WHERE " + whrs[:-4])
			for row in q:
				if row['string'] in kwds:
					del kwds[kwds.index(row['string'])]
					linksToKwdsVals = linksToKwdsVals + "("+str(lastLinkId)+","+str(row['id'])+",90),"

			if linksToKwdsVals != '':
				db.query("INSERT INTO linkstokeywords (linkid,keywordsid,score) VALUES "+linksToKwdsVals[:-1])

			l = 6
			for newKwd in kwds:
				if l == 0:
					break
				newKwdId = db.insert('keywords', string=newKwd)
				db.insert('linkstokeywords', linkid=lastLinkId, keywordsid=newKwdId, score=90)
				l = l - 1
	except Exception as ex:
		db.query(endq)
		linkError(ex,str(sys.exc_info()[2].tb_lineno),ogrow)

	db.query(endq)
	return ''
