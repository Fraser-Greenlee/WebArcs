
from application_only_auth import Client
from m.webinput import webinput
import random

def run(s,g):
	d = webinput(s,g,{'*setup':['loggedin','needall','print'],'name':'fstring'})
	if type(d) == str:
		return d

	name = d['name']

	client = Client("fVtL0r3tml6sRSJFtlfJfedbm", "629Gj3VjKJ9ih9dAj2bROm4nlrCWrhUojQqZqmLCttg9hmsrQk")

	friends = client.request('https://api.twitter.com/1.1/friends/list.json?cursor=-1&screen_name='+name+'&skip_status=true&include_user_entities=false')[u'users']
	print friends[0]
	for friend in friends:
		if g['db'].query("select count(*) from hub where rssurl='https://twitrss.me/twitter_user_to_rss/?user="+friend[u'screen_name']+"'")[0]['count'] == 0:
			id = g['db'].insert('hub', name=friend[u'name'],url="https://twitter.com/"+friend[u'screen_name'],rssurl="https://twitrss.me/twitter_user_to_rss/?user="+friend[u'screen_name'],rsstype=True,domain="twitter.com",hueangle=random.randint(0,359))
			g['db'].insert('refreshrate', arcid=id)
			g['db'].insert('subscriptions', uid=s.userid, fid=id)
	return 'v'
