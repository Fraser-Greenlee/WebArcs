
import web

web.config.debug = False

urls = (
	'/(.*)', 'refresh'
)

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = MyApplication(urls, globals())

class refresh:
	def POST(self, path):
		checkforposts()
	def GET(self,path):
		checkforposts()

def checkforposts():
		from feedclass.feedclass import Feed
		db = web.database(dbn='postgres', db='main', user='postgres', pw='fh3478hf38oh0ofh8fh7hre', host='130.211.97.197', port='5432')
		import types
		from m.sqltools import tblcount, remove, insertlist
		db.count = types.MethodType(tblcount,db)
		db.remove = types.MethodType(remove,db)
		db.insertlist = types.MethodType(insertlist,db)
		q = db.query("SELECT name from Asubs order by lastcheck ASC")
		for r in q:
			name = r['name']
			print name
			db.query("UPDATE asubs set lastcheck=now() where name='"+name+"'")
			f = Feed('https://www.reddit.com/r/'+name+'/.rss')
			f.getposts()
			f.db = db
			f.saveposts()

if __name__ == "__main__":
	app.run(port=8080)
