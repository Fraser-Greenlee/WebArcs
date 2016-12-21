
import web

from m.inputfilter import num

def run(s,g):
	if s.get('userid',0) == 0 or 'responce' not in g['i'] or g['i']['responce'] not in ['like','dislike','star'] or 'id' not in g['i']:
		return ''
	id = num(g['i']['id'])
	if id[0] in ['','0']:
		return ''

	q = g['db'].query("SELECT count(*) from responces where linkid="+g['i']['id']+" and userid="+str(s.userid)+" and responce='"+g['i']['responce']+"'")
	if q[0]['count'] == 0:
		g['db'].query("""
			INSERT INTO
				responces
				(linkid,userid,responce)
			values
				("""+id+""","""+str(s.userid)+""",'"""+g['i']['responce']+"""')
		""")
		g['db'].query("UPDATE links set "+g['i']['responce']+"c="+g['i']['responce']+"c+1 WHERE id="+g['i']['id'])
		return 'inserted'
	else:
		g['db'].query("DELETE from responces where linkid="+g['i']['id']+" and userid="+str(s.userid)+" and responce='"+g['i']['responce']+"'")
		g['db'].query("UPDATE links set "+g['i']['responce']+"c="+g['i']['responce']+"c-1 WHERE "+g['i']['responce']+"c>0 AND id="+g['i']['id'])
		return 'removed'
