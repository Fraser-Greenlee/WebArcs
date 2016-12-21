
import web

from m.webinput import webinput

def run(s,g):
	d = webinput(s,g,{'*setup':['loggedin'],'id':'fid','url':'furl'})
	if type(d) == str or 'id' not in d and 'url' not in d:
		print d
		return False

	uid = str(s.userid)

	db = g['db']

	if 'id' in d:
		if db.count('subscriptions', uid=uid, fid=d['id']) == 0:
			db.insert('subscriptions', uid=uid, fid=d['id'])
			return 'subscribed'
		else:
			db.remove('subscriptions', uid=int(uid), fid=d['id'])
			return 'unsubscribed'

	elif 'url' in d:
		url = d['url']
		from feedclass.feedclass import Feed
		try:
			f = Feed(url,db)
		except Exception as e:
			print e
			return False

		if f.stored is False:
			f.save()
			print 'saved'
		f.subscribe(uid)
		print 'Subscribed'
		return 'subscribed'
