
def tblcount(self,table,**args):
	whrs = ""
	for col,val in args.iteritems():
		if col.lower() != 'limit':
			valtype = type(val)
			if valtype == str:
				whrs += col+"='"+val+"' AND "
			else:
				whrs += col+"="+str(val)+" AND "
	if whrs != "":
		whrs = " WHERE "+whrs[:-4]

	if 'limit' in args:
		lim = " LIMIT "+str(args['limit'])
	else:
		lim = ""

	return self.query("SELECT count(*) as c from "+ table + whrs + lim )[0]['c']


def remove(self,table,**args):
	whrs = ""
	for col,val in args.iteritems():
		if col.lower() != 'limit':
			valtype = type(val)
			if valtype == str:
				whrs += col+"='"+val+"' AND "
			else:
				whrs += col+"="+str(val)+" AND "
	if whrs != "":
		whrs = " WHERE "+whrs[:-4]
	if 'limit' in args:
		lim = " LIMIT "+str(args['limit'])
	else:
		lim = ""
	return self.query("DELETE FROM " + table + whrs + lim)


def insertlist(self,table,diclist):
	if len(diclist) == 0:
		return False
	cols = diclist[0].keys()
	cstr = ''
	for c in cols:
		cstr += c+','
	cstr = cstr[:-1]
	sql = "INSERT INTO "+table+" ("+cstr+") VALUES "
	for dic in diclist:
		sql += "("
		for col in cols:
			if col not in dic:
				raise Exception("All rows should have same columns. Broke with key="+str(col)+" on row "+str(dic)+".")
			if type(dic[col]) is str or type(dic[col]) is unicode:
				sql += "'"+unicode(dic[col])+"', "
			else:
				sql += unicode(dic[col])+", "
		sql = sql[:-2]+"), "
	sql = sql[:-2]
	return self.query(sql)
