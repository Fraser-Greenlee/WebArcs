
import web
from m.processTemplate import getTemp, make, convert

filerTemp = getTemp('filtersite')

def run(s,g):
	ret = ''
	q = g['db'].query("SELECT * FROM (SELECT DISTINCT ON (domain) domain, name, inline, COUNT COUNT FROM (SELECT subscriptions.inline, hub.name, hub.domain, COUNT(*) OVER (PARTITION by hub.domain) FROM hub, subscriptions WHERE hub.id=subscriptions.fid AND subscriptions.uid="+str(s.userid)+") x WHERE inline=TRUE OR COUNT > 1) y ORDER BY inline desc, COUNT desc")
	for ro in q:
		if ro['inline'] == False:
			ro['name'] = ro['domain'][:ro['domain'].rfind('.')]
		ret += make(filerTemp, ro, {})
	return ret
