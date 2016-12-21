import web

def validForPassReset(db,uid,c):

	if set(uid,c).isdisjoint(['',False]):
		return False

	if db.query("SELECT count(*) AS count FROM useroptions WHERE id='"+uid+"' AND code='"+c+"'")[0]['count'] != 0:
		return True
	else:
		return False
