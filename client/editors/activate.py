import web

from m.inputfilter import num, fstring

def run(s,g):
	if 'mp' not in g['i'] or 'id' not in g['i']:
		return 'You seem to be missing details, please try another link.'
	id = num(g['i']['id'])
	mp = fstring(g['i']['mp'])
	if g['db'].query("SELECT COUNT(*) AS c FROM useroptions WHERE id="+id+" AND code="+mp+"")[0]['c'] == 1:
		g['db'].update('users', where="id="+id, activated=True)
		return 'done'
	else:
		return 'incorrect details sent'
