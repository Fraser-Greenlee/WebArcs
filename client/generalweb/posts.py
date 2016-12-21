
import json

from m.webinput import webinput
from feedclass.feedclass import Feed
from m.template import Template
from m.inputfilter import furl

postTemp = Template('post')

def run(s,g):
	if 'url' not in g['i'] or furl(g['i']['url']) is False:
		return False

	try:
		feed = Feed(g['i']['url'],g['db'])
	except Exception as e:
		print 'Exception', e
		return False

	feed.getposts()

	if s.get('userid',0) > 0 and feed.stored and g['db'].count('subscriptions',uid=s.userid,fid=feed.id) > 0:
		Subscribed = True
	else:
		Subscribed = False

	res = ''
	for post in feed.posts:
		res += postTemp.process(post,subscribe=('Subscribed' if Subscribed else 'Subscribe'),id='?url='+post['url'])
	return json.dumps({'name':feed.name,'url':feed.url,'posts':res,'stored':feed.stored,'Subscribed':Subscribed})
