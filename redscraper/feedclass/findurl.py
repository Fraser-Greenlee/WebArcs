
import requests
h = {'User-Agent': 'spider'}
from lxml import html
from urlparse import urlparse
import re
import time

from m.inputfilter import furl

def getdomain(url):
	return urlparse(url).netloc.replace('www.','')

def specialcase(url,req):
	domain = getdomain(url)

	# check for html recipie
	if domain == 'twitter.com':
		findlist = re.findall('https://twitter.com/.*?/',url+'/')
		if len(findlist) > 0:
			return {'url':findlist[0],'domain':'twitter.com','req':req,'doctype':'html'}

	# if from reddit
	elif domain == 'reddit.com':
		findlist = re.findall('https://www.reddit.com/r/.*?/',url+'/')
		if len(findlist) > 0:
			url = findlist[0]+'.rss'
			return url

	# missing rss link
	if 'text/html' in req.headers['content-type'] and domain == 'youtube.com':
		tree = html.fromstring(req.content)
		ls = tree.cssselect('meta[itemprop="channelId"]')
		if len(ls) > 0:
			channelId = ls[0].get('content')
			url = 'https://www.youtube.com/feeds/videos.xml?channel_id='+channelId
		 	return url

	return False


def findrsslink(url,content):
	tree = html.fromstring(content)
	links = tree.xpath('//link[@rel="alternate"][@href]') + tree.xpath('//a[@href]')
	for link in links:
		if 'href' in link.attrib:
			href = relativeurl(url,link.attrib['href'])
			href = furl(href)
			if href is not False:
				if wordsinstring(['rss','atom','feed'],[href,unicode(link.text)[:100]]):
					return href
	return False

def relativeurl(sourceurl,url):
	if url[:4] == 'http':
		return url
	elif url[:2] == '//':
		return sourceurl[:sourceurl.index(':')]+':'+url[url.index(':')+1:]
	else:
		sourceup = urlparse(sourceurl)
		if url[0] == '/':
			return sourceup.scheme+'://'+sourceup.netloc+'url'
		else:
			if url[2:] == '..':
				sourcepath = sourceup.path[1:].split('/')
				relpath = url.split('/')
				backcount = relpath.count('..')
				return sourceup.scheme+'://'+sourceup.netloc+'/'+ '/'.join(sourcepath[:-backcount]) +'/'+ '/'.join(relpath[backcount:])
			else:
				if sourceurl[-1] == '/':
					sourceurl = sourceurl[:-1]
				return sourceurl+'/'+url

def wordsinstring(words,strings):
	for string in strings:
		if string is not None:
			for word in words:
				if word in string:
					return True
	return False

def feedurl(url):
	req = requests.get(url, headers=h)
	#stop from being blocked
	time.sleep(1)
	#
	content_type = req.headers['content-type'].lower()
	if 'html' not in content_type and 'xml' not in content_type:
		raise Exception('bad data')
	special = specialcase(url,req)
	if special is not False:
		if type(special) == dict:
			return special
		else:
			url = special
			req = requests.get(url, headers=h)
			return {'url':url,'domain':getdomain(url),'req':req,'doctype':'rss'}
	else:
		if 'html' in content_type:
			url = findrsslink(url,req.content)
			if url is False:
				raise Exception('no rss feed found')
			else:
				feedreq = requests.get(url, headers=h)
				content_type = feedreq.headers['content-type'].lower()
				if 'xml' in content_type:
					return {'url':url,'domain':getdomain(url),'req':feedreq,'doctype':'rss'}
				else:
					return False
		else:
			return {'url':url,'domain':getdomain(url),'req':req,'doctype':'rss'}

def storedfeed(url,db):
	if db is False:
		return None
	else:
		return db.count('hub',rssurl=url) > 0

def getcontenttype(domain,db):
	if db is False:
		return None
	else:
		for row in db.query("SELECT contenttype from hub where domain='"+domain+"' order by id ASC limit 1"):
			return row['contenttype']
		return None

def findurl(url,db):
	data = feedurl(url)
	if data is False:
		return data
	data['contenttype'] = getcontenttype(data['domain'],db)
	data['stored'] = storedfeed(data['url'],db)
	return data
