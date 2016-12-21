
import web
from random import randint

from m.dbconx import db
from checkers import html
from checkers import rss

TESTING = False

def setrefreshrate(lc,sincelastfound,cyclevalue,arcid):
	qadd = ''

	print arcid, lc, sincelastfound, cyclevalue

	if lc > 0:
		qadd = ", datelastfound=now()"
		cyclvaluenew = int(sincelastfound/5.0)
	else:#						(1+19)/20
		cyclvaluenew = int(( sincelastfound/4.0 + 19*cyclevalue )/20.0)

	if cyclvaluenew < 3:
		cyclvaluenew = 3
	elif cyclvaluenew > cyclevalue*(5/4.0):
		cyclvaluenew = int(cyclevalue*(5/4.0))

	if TESTING == False:
		db.query('UPDATE refreshrate SET cyclevalue='+str(cyclvaluenew)+qadd+' WHERE arcid='+str(arcid))
	else:
		print 'UPDATE refreshrate SET cyclevalue='+str(cyclvaluenew)+qadd+' WHERE arcid='+str(arcid)



def run():
	db.query("UPDATE refreshrate SET midcheck=0 where datelastchecked < (now() - INTERVAL '20 MINUTE') and midcheck<>2")

	if TESTING:
		print 'start!'
		q = db.query("""
				SELECT
					htmlrecipe.*, datelastchecked, EXTRACT(EPOCH FROM (now() - datelastfound))/60 AS sincelastfound, hub.checktype, hub.url, hub.rssurl, hub.name, hub.id, cycleUnits, cycleValue, minrefreshmins, EXTRACT(EPOCH FROM (now() - datelastchecked))/60 /cycleValue AS score
				FROM
					refreshrate, hub LEFT JOIN htmlrecipe ON htmlrecipe.typeid=hub.checktype AND hub.checktype>1
				WHERE
					hub.id=49 AND refreshrate.arcid=hub.id
				ORDER BY
					score DESC
			""")
	else:
		q = db.query("""
				SELECT
					*
				FROM
					(
						SELECT
							htmlrecipe.*, datelastchecked, EXTRACT(EPOCH FROM (now() - datelastfound))/60 AS sincelastfound, hub.checktype, hub.url, hub.rssurl, hub.name, hub.id, cycleUnits, cycleValue, minrefreshmins, EXTRACT(EPOCH FROM (now() - datelastchecked))/60 /cycleValue AS score
						FROM
							refreshrate, hub LEFT JOIN htmlrecipe ON htmlrecipe.typeid=hub.checktype AND hub.checktype>1
						WHERE
							hub.id=refreshrate.arcid AND dateLastChecked < (CURRENT_TIMESTAMP - INTERVAL '1' MINUTE * minrefreshmins) and refreshrate.midcheck=0
						ORDER BY
							score DESC
						LIMIT 80
					) x
				WHERE
					sincelastfound > cycleValue
			""")

	q = list(q)

	if len(q) == 0:
		print 'no rows'
		if TESTING == False:
			db.query("UPDATE refreshrate SET midcheck=0 where datelastchecked < (now() - INTERVAL '20 MINUTE') and midcheck<>2")
		return False


	hubidlst = "("+str([row['id'] for row in q])[1:-1]+")"

	if TESTING == False:
		db.query("UPDATE refreshrate set midcheck=1 where midcheck<>2 and refreshrate.arcid IN "+hubidlst)

	for row in q:
		lc = False

		try:
			if row['checktype'] > 1:
				lc = html.getposts(row)
			else:
				lc = rss.getposts(row)
		except:
			continue

		if lc is False:
			continue

		setrefreshrate(lc, row['sincelastfound'], row['cyclevalue'], row['id'])

	if TESTING == False:
		db.query("UPDATE refreshrate set midcheck=0 where midcheck<>2 and refreshrate.arcid IN "+hubidlst)
		if randint(0,10) == 1:
			clearposts(db)
	return ''

def clearposts(db):
	q = list(db.query("SELECT * FROM (SELECT id, pageid, ROW_NUMBER() OVER (PARTITION by pageid) AS nt FROM links) x WHERE nt > 300"))
	if len(q) > 0:
		idlst = "("+str([x['id'] for x in q])[1:-1]+")"
		print 'idlst', idlst
		db.query("DELETE from linkstokeywords where linkid IN "+idlst)
		db.query("DELETE from history where linkid IN "+idlst)
		db.query("DELETE from responces where linkid IN "+idlst)
		db.query("DELETE from favourites where linkid IN "+idlst)
		db.query("DELETE from links where id IN "+idlst)
