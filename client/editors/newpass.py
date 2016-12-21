
import web
import hashlib

from m.inputfilter import fid, filsetpass, filpass

def run(s,g):
	if s.get('userid',0):
		return 'loggedIn'

	if 'p' not in g['i'] or 'key' not in g['i'] or 'id' not in g['i']:
		return 'data not sent'

	key = filpass(g['i']['key'])
	p = filsetpass(g['i']['p'])
	id = fid(g['i']['id'])
	if p in ['',False]:
		return 'bad password'
	if key in ['',False] or id == '':
		return 'data not sent'

	print id, key, p

	if g['db'].query("SELECT count(*) from forgotpass where id="+id+" and key='"+key+"'")[0]['count'] > 0:
		g['db'].query("UPDATE users set password='"+p+"' where id="+id)
		g['db'].query("DELETE from forgotpass where id="+id)
	else:
		return 'bad password'

	return 'v'
