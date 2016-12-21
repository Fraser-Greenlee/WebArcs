
import web
import requests
from urlparse import urlparse
from lxml import etree, html
parser = etree.XMLParser(strip_cdata=False)

from m.webinput import webinput
from m.inputfilter import furl, escapehtml
from m.scraperfilters import filterUrl, filterTitle, filterComments

def run(s,g):
	i = webinput(s,g,{
			'*setup':['loggedin','needall'],
			'url':'furl'
		})
	if type(i) == str:
		return i

	url = i['url']

	d = feedfromurl(db, url)

	if d == False:
		return 'bad data'
	d['rssurl'] = rssurl
	if 'url' not in d:
		d['url'] = htmlurl

	ret = ''
	for k in ['title','url','rssurl','rsstype']:
		ret += str(d[k])+'<>'
	ret = ret[:-2]

	id = g['db'].insert('tempdatadump', data=ret)

	return d['title']+'<>'+d['url']+'<>'+str(id)


def feedfromurl(db,url,**options):
	getposts = 'posts' in options and options['posts']

	pg = requests.get(url, headers={'User-Agent': 'spider'})

	ctyp = pg.headers['content-type']
	if 'html' not in ctyp and 'xml' not in ctyp:
		return 'bad data'

	special = specialcase(url,pg)
	if special is not False:
		pg = requests.get(special)
	else:
		if 'html' in ctyp:
			rssurl = findrsslink(pg.content)
			if rssurl is False:
				return 'no rss feed found'
			htmlurl = url
			pg = requests.get(rssurl, headers={'User-Agent': 'spider'})
		else:
			rssurl = url
			htmlurl = ''

	return rssdata( pg.content , getposts )


def specialcase(url,pg):
	domain = urlparse(url).netloc.replace('www.','')

	# check for html recipie
	if domain in ['twitter.com']:
		print 'twitter!'
		return False

	# missing rss link
	if domain == 'youtube.com':
		tree = html.fromstring(pg.content)
		ls = tree.cssselect('meta[itemprop="channelId"]')
		if len(ls) > 0:
			channelId = ls[0].get('content')
			url = 'https://www.youtube.com/feeds/videos.xml?channel_id='+channelId
		 	return url

	return False


def rssdata(text, getposts):
	data = {}
	if '?>' in text[:100]:
		if text[:100].strip().replace(' ','')[:5] == '<?xml':
			text = text[text.index('?>')+2:]

	tree = etree.XML(text, parser)

	try:
		if len(tree.xpath('//item')) > 0:
			data['rsstype'] = True
			data['title'] = tree.xpath('//channel/title')[0].text
			data['url'] = tree.xpath('//channel/link')[0].text
		elif len(tree.xpath('//xhtml:entry', namespaces={'xhtml':'http://www.w3.org/2005/Atom'})) > 0:
			data['rsstype'] = False
			data['title'] = tree.xpath('//xhtml:title', namespaces={'xhtml':'http://www.w3.org/2005/Atom'})[0].text
			data['url'] = tree.xpath('//xhtml:link[@rel="alternate"]', namespaces={'xhtml':'http://www.w3.org/2005/Atom'})[0].attrib['href']
		else:
			print 'no len'
			return False
	except Exception as e:
		print 'error', e

	data['url'] = furl(data['url'])
	data['title'] = escapehtml(data['title'])[:50]

	if data['url'] is False or data['title'] == '':
		return False

	if getposts == False:
		return data

	# get posts
	posts = []
	linklist = getlinks(data['rsstype'],tree)
	for link in linklist:
		posts.append(linkTOdict(data,link))

	data['posts'] = posts
	return data


def linkTOdict(data,link):
	title = ''
	url = ''
	comments = ''
	imgsrc = ''

	imax = 50
	for el in link:
		imax -= 1
		if imax == 0:
			break

		if '}' in el.tag:
			tag = el.tag[el.tag.index('}')+1:]
		else:
			tag = el.tag

		if tag == 'group' and imgsrc == '':
			print el
			thumbnailList = el.xpath('thumbnail@url')
			if len(thumbnailList) > 0:
				imgsrc = thumbnailList[0]

		if tag == 'title':
			title = filterTitle(el.text)
			if len(title) > 180:
				return False
		elif tag == 'link':
			if data['rsstype'] is False:
				hreflist = el.xpath('@href')
				if len(hreflist) == 0:
					return False
				else:
					url = filterUrl(hreflist[0])
			else:
				url = filterUrl(el.text)
		elif tag == 'comments' and data['rsstype']:
			comments = filterComments(el.text)

	if  title == '' or link == '':
		return False

	return {'id':-1,'title':title,'url':url,'imgsrc':imgsrc,'comments':comments}


def getlinks(rsstype,tree):
	if rsstype == 1:
		return tree.xpath('//item')
	else:
		return tree.xpath('//xhtml:entry', namespaces={'xhtml':'http://www.w3.org/2005/Atom'})


def findrsslink(text):
	tree = etree.HTML(text)
	links = tree.xpath('//link[@rel="alternate"][@href]') + tree.xpath('//a[@href]')
	for link in links:
		if 'href' in link.attrib:
			href = furl(link.attrib['href'])
			if href is not False:
				if wordsinstring(['rss','atom','feed'],[href,unicode(link.text)[:100]]):
					return href
	return False


def wordsinstring(words,strings):
	for string in strings:
		if string is not None:
			for word in words:
				if word in string:
					return True
	return False
