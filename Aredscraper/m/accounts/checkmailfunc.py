import re

from m.inputfilter import filmail

def checkmail(db,e):
	e = filmail(e)
	if not e:
		return 'invalid address'
	if db.query("SELECT COUNT(*) AS c FROM users WHERE email='"+e+"'")[0]['c'] == 0:
		return True
	else:
		return 'already stored'

def checkmailTF(db,e):
	e = filmail(e)
	if not e:
		return True
	if db.query("SELECT COUNT(*) AS c FROM users WHERE email='"+e+"'")[0]['c'] == 0:
		return True
	else:
		return False
