import re
import validators
from bs4 import BeautifulSoup

escapehtmltable = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
	"...":"&amp;#8230;",
	"$":"&#36;",
	'%':'&#37;',
	';':'&#59;'
}

def escapehtml(text):
	if text == '':
		return ''

	unescapedlst = re.split('&.*?;',text)
	escapedlst = re.findall('(&.*?;)',text)
	esclstLEN = len(escapedlst)
	ret = ''

	if text[0] == '&':
		ret = escapedlst[0]
		del escapedlst[0]

	for i in range(len(unescapedlst)):
		ret += "".join(escapehtmltable.get(c,c) for c in unescapedlst[i])
		if esclstLEN > i:
			ret += escapedlst[i]

	return ret

def filmail(mail):
	mail = re.sub("[^a-z0-9@!#$%&'*+-/=?^_`{|}~.]", '', mail)[:255]
	if not validators.email(mail):
		return False
	else:
		return mail

def furl(url):
	if url[:2] == '//':
		url = 'http:'+url
	if not validators.url(url):
		return False
	else:
		return url

def fsurl(url):
	if url[:2] == '//':
		url = 'http:'+url
	if not validators.url(url):
		return ''
	else:
		return url

def num(s):
	return int(re.sub("[^0-9]", '', s))

def fstring(s):
	return re.sub("[^a-z0-9]", '', s)
