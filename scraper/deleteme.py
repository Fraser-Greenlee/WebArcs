# -*- coding: utf-8 -*-

# UPDATE refreshrate SET midcheck=0 WHERE datelastchecked < now() - INTERVAL '1 DAY'

TESTING = False
testfilelinks = {
	18:'reddit-rss.txt',
	49:'hacker-news-rss.txt',
	14:'stratechary-rss.txt',
	5:'waitbutwhy-rss.txt',
	22:'paulg.txt'
}

import web
from lxml import etree
parser = etree.XMLParser(recover=True)
import StringIO
import requests
import sys
from random import randint
import re
httpfinder = re.compile(r"(http://[^ ]+)")
httpsfinder = re.compile(r"(https://[^ ]+)")

from modules.inputfilter import escapehtml, furl

def rssError(ex,linenum,row):
	ex = escapehtml(unicode(ex))[:255]
	print ex
	if 'id' in row:
		arcid = unicode(row['id'])
	else:
		arcid = 'no id'
	db.query(u"INSERT INTO errorcheckrss (linenumber,exception,arcid) VALUES ('"+unicode(linenum)+"','"+ex+"','"+arcid+"')")

def htmllist(txt):
	xml = etree.fromstring('<html>'+txt+'</html>', parser)
	t = xml.text
	if type(t) is str:
		lst = [escapehtml(t)]
	else:
		lst = ['']
	for i in range(len(xml)):
		plaintxt = etree.tostring(xml[i])
		lst += [plaintxt[:plaintxt.index('>')+1], escapehtml(xml[i].text), plaintxt[plaintxt.index('</'):plaintxt.rfind('>')+1], escapehtml(re.sub('<.*>','',plaintxt)),]
	return lst

def cutescapedstr(st,maxln):
	if ';' in st[-(len(st) - maxln):]:
		while len(st) > maxln:
			if st[-1] == ';':
				st = st[:st.rfind('&')]
			elif ';' in st:
				st = st[:st.rfind(';')+1]+st[st.rfind(';')+1:][:-(len(st) - maxln)]
			else:
				return st[:-(len(st) - maxln)]
		return st
	else:
		return st[:-(len(st) - maxln)]

def cutlisttext(ls,ln):
	tocut = len(''.join(ls)) - ln
	#print ls, tocut
	if tocut <= 0:
		return ls
	for i in range(len(ls))[::-1]:
		if '<' in ls[i]:
			continue
		if tocut >= len(ls[i]):
			tocut -= len(ls[i])
			del ls[i]
			if tocut == 0:
				return ls
		else:
			ls[i] = cutescapedstr(ls[i], len(ls[i]) - tocut)
			return ls
	return ['']

def cuthtmlstr(txt,ln):
	ls = htmllist(txt)
	return ''.join(cutlisttext(ls, ln)).replace('<b></b>', '')

def findTitle(tag,feedname):
	title = escapehtml(tag.text.strip())
	#print 'title', title
	if 'http://' in title:
		title = httpfinder.sub(r'<b>\1</b>',title)
	if 'https://' in title:
		title = httpsfinder.sub(r'<b>\1</b>',title)

	if len(title) > 180:
		return cuthtmlstr(title, 177)+'...'[:180]
	else:
		return cuthtmlstr(title, 180)[:180]
