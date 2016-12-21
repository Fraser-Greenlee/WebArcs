
import web
import re
import string
import random
import requests

from m.webinput import webinput
from m.inputfilter import filip

def run(s,g):
	d = webinput(s,g,{'*setup':['loggedIn',False,'needall'],'e':'filmail','p':'filsetpass'})
	if type(d) == str:
		if 'e' not in d:
			return 'incorrect email address'
		elif 'p' not in d:
			return 'incorrect password'
		return d

	e = d['e']
	p = d['p']

	ech = checkmail(g['db'],e)

	if ech != True:
		return ech
	elif p == '':
		return 'missingP'

	if p == False:
		return 'password not allowed'

	ip = filip(web.ctx.env.get('ip', ''))

	try:
		uid = g['db'].insert('users', email=e, password=p, ip=ip, lasthistorycheck=0, signup=web.SQLLiteral("NOW()"), lastlogin=web.SQLLiteral("NOW()"), notescheck=web.SQLLiteral("NOW()"))
	except Exception, e:
		return e

	cp = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
	web.setcookie("cookiePass", cp, expires=30*24*60*60,  secure=False)


	mailp = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
	s.userid = uid
	g['db'].insert('useroptions', id=uid, code=mailp)

	requests.post(
		"https://api.mailgun.net/v3/mg.webarcs.com/messages",
		auth=("api", "key-fde98f1eb655d8778c7df6c20f24b438"),
		data={
			"from": "WebArcs <mailgun@mg.webarcs.com>",
			"to": [e],
			"subject": "Reset password",
			"html": '''<html>
							<body style="margin:0px; font-family:Tahoma, Geneva, sans-serif;">
								<div style="padding:10px; background:#2B9BFD; font-size:24px; color:#FFFFFF;">WebArcs confirm email</div>\
								<div style="padding:24px; font-size:17px;">
									Hi thanks for signing up to WebArcs.<br />
									We're super excited to see what you think of our new view of the internet.<br />
									To confirm your email address click the link below.<br />
									<br />
									<a href="http://webarcs.com/f/editors/activate?mp='''+mailp+'''&e='''+e+'''">Confirm my address.</a>
								</div>
							</body>
						</html>'''
			}
	)
	return True

def checkmail(db,e):
	if db.query("SELECT COUNT(*) AS c FROM users WHERE email='"+e+"'")[0]['c'] == 0:
		return True
	else:
		return 'already stored'
