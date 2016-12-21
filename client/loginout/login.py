
import web

from m.webinput import webinput
from m.inputfilter import setpass

def run(s,g):
	d = webinput(s,g,{'*setup':['loggedin',False],'loginid':'filpass','e':'filmail','p':'filsetpass'})
	if type(d) == str:
		return d

	if 'loginid' in d:
		uid = list(g['db'].query("SELECT id from users, phoneaccounts where phoneaccounts.pass='"+d['loginid']+"' and phoneaccounts.uid=users.id"))
		if len(uid) != 0:
			s.userid = int(uid[0]['id'])
			return str(s.userid)

	if ('e' in d and 'p' in d) == False:
		return 'bad data'

	if g['db'].query("SELECT COUNT(*) AS c FROM users WHERE email='"+d['e']+"' AND password='"+d['p']+"'")[0]['c'] < 1:
		return 'incorrect details'
	s.userid = g['db'].query("SELECT id FROM users WHERE email='"+d['e']+"' AND password='"+d['p']+"' LIMIT 1")[0]['id']

	if 'loginid' in d:
		g['db'].query("DELETE from phoneaccounts where uid="+str(s.userid))
		g['db'].query("INSERT INTO phoneaccounts (uid,pass) VALUES ("+str(s.userid)+",'"+d['loginid']+"')")

	return str(s.userid)
