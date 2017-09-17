
import re
import validators
import hashlib

from m.allcontenttypes import contenttypes

def filmail(mail):
	mail = re.sub("[^a-z0-9@!#$%&'*+-/=?^_`{|}~.]", '', mail)[:255]
	if not validators.email(mail):
		return False
	else:
		return mail

urlregex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)
def furl(url):
	if url[:2] == '//':
		url = 'http:'+url
	if urlregex.match(url) is not None and len(url) < 256:
		return url
	else:
		return False

def setpass(inp):
	try:
		return hashlib.sha1("icTYCCYiOR6RX6CYCytdCTYdTYTdTYFkGHj-"+inp).hexdigest()
	except:
		return False

def filpass(pwd):
	return re.sub("[^a-z0-9@!#$%&'*+-/=?^_`{|}~.]g", '', pwd)[:255]

def filsetpass(pwd):
	return setpass(filpass(pwd))

def filip(ip):
	return re.sub("[^0-9.]", '', ip)[:255]

def num(s):
	return re.sub("[^0-9]", '', s)

def fid(s):
	id = num(s)
	if id == '' or id[0] == '0':
		return False
	else:
		return id

def fstring(s):
	return re.sub("[^A-Za-z0-9_]", '', s)

def fcontenttypes(s):
	if s in contenttypes:
		return s
	else:
		return False

escapehtmltable = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;",
	"...":"&amp;#8230;"
}
def escapehtml(text):
	return "".join(escapehtmltable.get(c,c) for c in text)

def markedtype(tp):
	if tp in ['like','dislike','star','history']:
		return tp
	else:
		return False

def hubname(s):
	return re.sub("[^A-Za-z0-9 &;]", '', s)

####### unused

unescapehtmltable = {
	"amp": "&",
	'quot': '"',
	"apos": "'",
	"gt": ">",
	"lt": "<",
	"amp;#8230": "..."
}
def unescapehtml(text):
	for k in unescapehtmltable:
		text = re.sub("&.*?"+k+".*?;", unescapehtmltable[k], text)
	return text
