
import re

from m.inputfilter import escapehtml

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

def cuthtmlstr(html,cut):
	html = escapehtml(html.strip())
	if len(html) > cut:
		return "".join(cutlisttext(htmllist(html), cut-3))+'...'
	else:
		return html
