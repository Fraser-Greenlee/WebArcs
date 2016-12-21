
from m.inputfilter import furl
from m.template import template
from addfeed.getdata import feedfromurl

postTemp = template('post')

def run(s,g):
	if 'url' not in g['i'] or furl(g['i']['url']) is False:
		return 'bad input'
	data = feedfromurl(g['db'], g['i']['url'], posts=True)
	print data
	return postHTML(data)

def postHTML(data):
	res = ''
	for row in data['posts']:
		res += postTemp.process(row)
	return res
