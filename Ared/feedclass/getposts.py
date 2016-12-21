
from lxml import html
import re

from m.filters import filterTitle, filterLink, filterComments
from m.inputfilter import furl

xhtml = {'xhtml':'http://www.w3.org/2005/Atom'}

def getposts(feed,db):
	if feed.stored is False or feed.stored is None:
		return scrapeposts(feed,db)
	else:
		return list(db.query("SELECT * from links where pageid="+str(feed.id)))

def tweetText(nodelist):
	if len(nodelist) == 0:
		return ''
	else:
		txt = ''
		txt += unicode(nodelist[0].text)
		children = list(nodelist[0])
		for child in children:
			if 'u-hidden' not in child.get('class'):
				txt += re.sub('<.*?>', '', html.tostring(child)).replace('\n', '').strip()
			else:
				txt += ' '+re.sub('<.*?>', '', html.tostring(child)).replace('\n', '').strip()
		return txt

def getAttr(nodelist,atr):
	if len(nodelist) == 0:
		return ''
	else:
		return nodelist[0].get(atr)

def scrapeposts(feed,db):
	posts = []
	linklist = getlinks(feed.checktype, feed.tree)
	for link in linklist:
		d = linkdata(feed,link,db)
		if d is not False:
			posts.append(d)
	return posts

def getlinks(rsstype,tree):
	if rsstype == 1:
		return tree.xpath('//item')
	elif rsstype == 0:
		return tree.xpath('//xhtml:entry', namespaces=xhtml)
	else:
		return tree.cssselect('li.stream-item')


def linkdata(feed,link,db):
	data = {
		'title': getTitle(feed,link),
		'url': getUrl(feed,link,db),
		'comments': getComments(feed,link),
		'imgsrc': getImgsrc(feed,link),
		'snipet':'',
		'arcid':feed.id
	}
	if data['title'] in [False,''] or data['url'] in [False,'']:
		return False
	return data

def getTitle(feed,link):
	if feed.checktype == 2:
		return filterTitle(tweetText(link.cssselect('.js-tweet-text')))
	else:
		list = link.xpath('title') if feed.checktype == 1 else link.xpath('xhtml:title', namespaces=xhtml)
		if len(list) == 0:
			return False
		return filterTitle(list[0].text)

def getUrl(feed,link,db):
	if feed.checktype == 2:
		return furl('https://twitter.com/distefam/status/'+link.get('data-item-id'))
	else:
		list = link.xpath('link') if feed.checktype == 1 else link.xpath('xhtml:link', namespaces=xhtml)
		if len(list) == 0:
			return False
		if db is False:
			return filterLink(list[0].text if feed.checktype == 1 else list[0].get('href'))
		else:
			return filterLink(list[0].text if feed.checktype == 1 else list[0].get('href'), hasdb=db)

def getComments(feed,link):
	if feed.checktype == 1:
		list = link.xpath('comments')
		if len(list) > 0:
			return filterComments(list[0].text)
	return False

def getImgsrc(feed,link):
	if feed.checktype == 2:
		return furl(getAttr(link.cssselect('.AdaptiveMedia img'),'src'))
	else:
		rawstr = html.tostring(link)
		find = re.findall('.*(http.*?\.jpg|http.*?\.gif|http.*?\.png)',rawstr)
		if len(find) > 0:
			return furl(find[0])
		else:
			return False
