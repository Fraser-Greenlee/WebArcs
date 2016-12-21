
import web

from m.webinput import webinput

def run(s,g):
	if 'loginid' not in g['i'] or s.get('userid',0) != 0:
		return s.get('userid',0)

	d = webinput(s,g,{'*setup':['loggedin',False,'needall'],'loginid':'filpass'})
	if type(d) == str:
		return '0'

	if 'loginid' in d:
		uid = list(g['db'].query("SELECT id from users, phoneaccounts where phoneaccounts.pass='"+d['loginid']+"' and phoneaccounts.uid=users.id"))
		if len(uid) != 0:
			s.userid = int(uid[0]['id'])
			return str(s.userid)
		else:
			return 'loginphone'
	else:
		return '0'
