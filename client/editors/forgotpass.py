
import web
import random
import string
import requests

from m.inputfilter import filmail

def makekey():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))

def run(s,g):

	if s.get('userid',0):
		return 'loggedIn'

	if 'e' not in g['i'] or g['i']['e'] == '':
		return 'bad input'

	e =	filmail(g['i']['e'])
	if e == '':
		return 'invalid address'
	elif db.count('users',email=e) == 0:
		return 'email not stored'

	id = str(q[0]['id'])

	key = makekey()

	g['db'].insert('forgotpass', id=id, key=key)

	requests.post(
		"https://api.mailgun.net/v3/mg.webarcs.com/messages",
		auth=("api", "key-fde98f1eb655d8778c7df6c20f24b438"),
		data= {
			"from": "WebArcs <mailgun@mg.webarcs.com>",
			"to": [e],
			"subject": "Reset password",
			"html": '''<html>
							<body style="margin:0px; font-family:Tahoma, Geneva, sans-serif;">
								<div style="padding:10px; background:#2B9BFD; font-size:24px; color:#FFFFFF;">WebArcs password reset</div>\
								<div style="padding:24px; font-size:17px;">
									We recieved a reset password request on your account.<br />
									<br />
									<a href="http://webarcs.com/?id='''+id+'''&resetpass='''+key+'''">Reset Password</a><br />
									<br />
									If you know your password ignore this message.
								</div>
							</body>
						</html>'''
		}
	)

	return 'v'
