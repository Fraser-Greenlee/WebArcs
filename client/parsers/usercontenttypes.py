
import web
from m.processTemplate import getTemp, make, convert

filerTemp = getTemp('contenttype')

def run(s,g):
	ret = ''
	if s.get('userid',0) == 0:
		q = g['db'].query("""
			SELECT contenttype, count(*)
			FROM hub
			GROUP BY contenttype
			ORDER BY count(*) DESC
		""")
	else:
		q = g['db'].query("""
			SELECT contenttype, count(*)
			FROM subscriptions, hub
			WHERE hub.id=subscriptions.fid AND subscriptions.uid="""+str(s.userid)+"""
			GROUP BY contenttype
			ORDER BY count(*) DESC
		""")
	for ro in q:
		if ro['contenttype'] == '':
			ro['contenttype'] = 'other'
		
		if ro['contenttype'] == 'news':
			ret = make(filerTemp, ro, {}) + ret
		else:
			ret += make(filerTemp, ro, {})
	return ret
