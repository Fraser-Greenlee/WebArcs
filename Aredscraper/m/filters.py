
from lxml import etree
parser = etree.XMLParser(recover=True)
import re

from m.inputfilter import escapehtml, furl

def cutlisttext(ls,ln):
	tocut = len(''.join(ls)) - ln
	#print ls, tocut
	if tocut <= 0:
		return ls
	for i in range(len(ls))[::-1]:
		if '</' in ls[i]:
			continue
		elif '<' in ls[i]:
			tocut -= (len(ls[i])*2 + 1)
			del ls[i]
			del ls[i]
			if tocut < 1:
				return ls
			continue
		elif '&' in ls[i]:
			tocut -= len(ls[i])
			del ls[i]
			if tocut < 1:
				return ls
			continue
		if tocut >= len(ls[i]):
			tocut -= len(ls[i])
			del ls[i]
			if tocut < 1:
				return ls
		else:
			ls[i] = ls[i][:-tocut]
			return ls
	return ['']

def esclist(text):
	if text == '':
		return ''
	txtlst = re.split('&.*?;',text)
	taglst = re.findall('(&.*?;)',text)
	ret = []
	if text[0] == '&':
		ret = [taglst[0]]
		del taglst[0]
	for i in range(len(txtlst)):
		ret.append(txtlst[i])
		if len(taglst) > i:
			ret.append(taglst[i])
	return ret

def htmllist(text):
	if text == '':
		return ''
	txtlst = re.split('<.*?>',text)
	taglst = re.findall('(<.*?>)',text)
	ret = []
	if text[0] == '<':
		ret = [taglst[0]]
		del taglst[0]
	for i in range(len(txtlst)):
		ret.append(txtlst[i])
		if len(taglst) > i:
			ret.append(taglst[i])
	nret = []
	for raw in ret:
		if raw != '':
			if raw[0] != '<':
				nret += esclist(raw)
			else:
				nret.append(raw)
	return nret

def filterTitle(title):
	title = escapehtml(title.strip())
	for startword in ['http://','https://','@','u/','#']:
		title = re.sub(r"("+startword+"[^ ]+)", r'<b>\1</b>', title)
	if len(title) > 180:
		return "".join(cutlisttext(htmllist(title), 177))+'...'[:180]
	else:
		return title

#############

def filterLink(link,**hasdb):
	link = furl(link)

	if link == False or len(link) > 255:
		return ''

	if 'db' in hasdb and hasdb['db'].query("""
			SELECT
				(SELECT COUNT(*) FROM links WHERE url='"""+link+"""' LIMIT 1)
				+ (SELECT COUNT(*) FROM linkstobeindexed WHERE url='"""+link+"""' LIMIT 1)
				+ (SELECT COUNT(*) FROM error WHERE href='"""+link+"""' LIMIT 1)
			 AS c
		 """)[0]['c'] > 0:
		return ''
	else:
		return link

#############

def filterComments(comments):
	comments = furl(comments)
	if comments == False or len(comments) > 255:
		return ''
	return comments
