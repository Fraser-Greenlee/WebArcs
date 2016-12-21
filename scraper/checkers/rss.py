# -*- coding: utf-8 -*-

# UPDATE refreshrate SET midcheck=0 WHERE datelastchecked < now() - INTERVAL '1 DAY'

testfilelinks = {
	18:'reddit-rss.txt',
	49:'hacker-news-rss.txt',
	14:'stratechary-rss.txt',
	5:'waitbutwhy-rss.txt',
	22:'paulg.txt'
}
TESTING = False

import web
from lxml import etree
parser = etree.XMLParser(recover=True)
import StringIO
import requests
import sys

from m.dbconx import db
from m.filters import filterTitle, filterLink, filterComments
from m.inputfilter import escapehtml

def getlinks(feed,checktype,feedid,db):
	values = ''
	alreadystoredC = 10
	itemsMax = 40
	for item in feed:
		link = ''
		comments = ''
		title = ''

		itemsMax -= 1
		if itemsMax == 0:
			break

		imax = 50
		for i in item:
			imax -= 1
			if imax == 0:
				break

			if '}' in i.tag:
				tag = i.tag[i.tag.index('}')+1:]
			else:
				tag = i.tag

			if tag == 'title':
				title = filterTitle(i.text)
				if len(title) > 180:
					print title
					raise Exception('Title too long!')
			elif tag == 'link':
				if checktype == 0:
					link = i.xpath('@href')
					if len(link) == 0:
						return False
					else:
						link = filterLink(link[0],db)
				else:
					link = filterLink(i.text,db)
			elif tag == 'comments' and checktype == 1:
				comments = filterComments(i.text)

		if  title == '' or link == '':
			alreadystoredC -= 1
			if alreadystoredC == 0:
				break
			else:
				continue

		# be sure to get links in order
		values = "("+unicode(feedid)+", '"+unicode(title)+"', '"+unicode(link)+"','"+unicode(comments)+"'), " + values

	print 'values:', values
	if values != '':
		if TESTING == False:
			print 'INSERT INTO...'
			db.query(u'INSERT INTO linkstobeindexed (arcid,title,url,comments) VALUES '+values[:-2])
		else:
			print u'INSERT INTO linkstobeindexed (arcid,title,url,comments) VALUES '+values[:-2]

	return values.count('(')

def getfeed(url,checktype,id,db):
	if TESTING:
		text = open('test-data/'+testfilelinks[id],'r').read()
	else:
		text = requests.get(url, headers={'User-Agent': 'spider'})
		db.query('UPDATE refreshrate set datelastchecked=now() WHERE arcid='+str(id))
		text = text.text
	try:
		text.decode('utf-8')
	except UnicodeError:
		text = text.encode("utf-8")

	if '?>' in text[:100]:
		if text[:100].strip().replace(' ','')[:5] == '<?xml':
			text = text[text.index('?>')+2:]

	feed = etree.parse(StringIO.StringIO(text), parser=etree.XMLParser(recover=True))
	if feed is None or feed.getroot() is None or feed.getroot().tag == 'html':
		errorupdate += " arcid="+str(id)+" OR "
		#print "continue: feed is None or feed.getroot() is None or feed.getroot().tag == 'html'"
		return False
	return etree.fromstring(text)

	return False


import dateutil.parser
def couldbeUpdated(feed,lastchecked):
	updated = feed.xpath('feed/updated')
	if len(updated) == 0:
		return True
	else:
		# ISO date converter
		updated = dateutil.parser.parse(updated.text).replace(tzinfo=None)
		return updated > lastchecked


def getposts(row):
	try:
		feed = getfeed(row['rssurl'],row['checktype'],row['id'],db)
		if feed is False:
			print 'feed is False'
			return False

		if couldbeUpdated(feed,row['datelastchecked']):
			if row['checktype'] == 1:
				feed = feed.xpath('//item')
			else:
				feed = feed.xpath('//xhtml:entry', namespaces={'xhtml':'http://www.w3.org/2005/Atom'})

			if feed is False:
				return False

			return getlinks(feed,row['checktype'],row['id'],db)

	except Exception as ex:
		if TESTING == False:
			db.query(u"INSERT INTO errorcheckrss (linenumber,exception,arcid) VALUES ('"+str(sys.exc_info()[2].tb_lineno)+"','"+escapehtml(str(ex))+"','"+str(row)+"')")
		else:
			raise Exception('error, '+str(ex))

	return False
