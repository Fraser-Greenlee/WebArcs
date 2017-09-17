
from urlparse import urlparse
from lxml import etree, html
parser = etree.XMLParser(strip_cdata=False)

from m.inputfilter import escapehtml

def cutstr(st,ln):
	if len(st) > ln:
		return st[:ln-3]+'...'
	else:
		return st

def dbdata(rssurl,db):
	data = db.query("SELECT * from hub where rssurl='"+rssurl+"'")[0]
	data['tree'] = None
	if data['url'][:20] == 'https://twitter.com/' or data['url'][:23] == 'https://www.reddit.com/':
		data['viewtype'] = 'contentview'
	else:
		data['viewtype'] = ''
	return data

def getdata(content,doctype):
	data = {}

	if doctype == 'rss':
		if '?>' in content[:100]:
			if content[:100].strip().replace(' ','')[:5] == '<?xml':
				content = content[content.index('?>')+2:]

		tree = etree.XML(content, parser)

		data['tree'] = tree
		data['checktype'] = int(len(tree.xpath('//item')) > 0)
		if data['checktype'] == 1:
			data['name'] = tree.xpath('//channel/title')[0].text
			data['url'] = tree.xpath('//channel/link')[0].text
		else:
			data['name'] = tree.xpath('//xhtml:title', namespaces={'xhtml':'http://www.w3.org/2005/Atom'})[0].text
			data['url'] = tree.xpath('//xhtml:link[@rel="alternate"]', namespaces={'xhtml':'http://www.w3.org/2005/Atom'})[0].attrib['href']

	elif doctype == 'html':
		tree = html.fromstring(content)
		data['tree'] = tree

		title = tree.cssselect('title')[0].text
		data['name'] = title[title.index('(@')+1:title.index(')')]
		data['url'] = 'https://twitter.com/'+data['name']
		data['checktype'] = 2

	if data['url'][:20] == 'https://twitter.com/' or data['url'][:23] == 'https://www.reddit.com/':
		data['viewtype'] = 'contentview'
	else:
		data['viewtype'] = ''

	data['name'] = cutstr(escapehtml(data['name']),50)

	data['hidden'] = False
	data['postdate'] = None
	data['siteid'] = 'not done yet'
	data['id'] = False

	return data
