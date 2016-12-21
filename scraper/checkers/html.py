
from lxml import html
from lxml.cssselect import CSSSelector
from lxml import etree
parser = etree.XMLParser(recover=True)
import requests
import re

from m.dbconx import db
from m.inputfilter import escapehtml, fsurl
from m.filters import filterTitle, filterLink

TESTING = False

def innerText(nodelist):
	if len(nodelist) == 0:
		return ''
	else:
		return re.sub('<.*?>', '', etree.tostring(nodelist[0])).replace('\n', '').strip()

def getAttr(nodelist,atr):
	if len(nodelist) == 0:
		return ''
	else:
		return nodelist[0].get(atr)

def twitterurl(node):
	return 'https://twitter.com/distefam/status/'+node.get('data-item-id')

def getposts(row):
	vals = ""
	try:
		page = requests.get(row['url'], headers={'User-Agent': 'spider'})
		db.query('UPDATE refreshrate set datelastchecked=now() WHERE arcid='+str(row['id']))
		tree = html.fromstring(page.content)

		feed = tree.cssselect(row['feed'])

		for entry in feed:
			if row['link'][0] == '*':
				url = fsurl(globals()[row['link'][1:]](entry))
			else:
				url = fsurl(getAttr(entry.cssselect(row['link']),'href'))
			url = filterLink(db,url)

			title = filterTitle(innerText(entry.cssselect(row['title'])))
			snipet = escapehtml(innerText(entry.cssselect(row['snipet'])))
			img = fsurl(getAttr(entry.cssselect(row['img']),'src'))

			if title != '' and url != '':
				vals += "("+str(row['id'])+",'"+url+"','"+title+"','"+snipet+"','"+img+"'), "
	except:
		if TESTING:
			raise

	if vals != '':
		if TESTING:
			print "INSERT INTO linkstobeindexed (arcid,url,title,snipet,imgsrc) VALUES "+vals[:-2]
		else:
			db.query("INSERT INTO linkstobeindexed (arcid,url,title,snipet,imgsrc) VALUES "+vals[:-2])

	return vals.count('(')
