import web
import importlib
from urllib import quote_plus

web.config.debug = False
testing = False

urls = (
	'/link/(.*)', 'link',
	'/fs/(.*)', 'filesend',
	'/f/(.*)', 'api',
	'/(.*)', 'home'
)

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = MyApplication(urls, globals())
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'userid':0})

class filesend:
	def POST(self, path):
		db = web.database(dbn='postgres', db='main', user='postgres', pw='fh3478hf38oh0ofh8fh7hre', host='130.211.97.197', port='5432')
		import types
		from m.sqltools import tblcount, remove, insertlist
		db.count = types.MethodType(tblcount,db)
		db.remove = types.MethodType(remove,db)
		db.insertlist = types.MethodType(insertlist,db)
		res = importlib.import_module(path.replace('/','.')).run(session, {'db':db,'i':web.input()})
		raise web.seeother('/?msg='+res)
	def GET(self, path):
		raise web.seeother('/')

class api:
	def POST(self, path):
		db = web.database(dbn='postgres', db='main', user='postgres', pw='fh3478hf38oh0ofh8fh7hre', host='130.211.97.197', port='5432')
		import types
		from m.sqltools import tblcount, remove, insertlist
		db.count = types.MethodType(tblcount,db)
		db.remove = types.MethodType(remove,db)
		db.insertlist = types.MethodType(insertlist,db)
		return importlib.import_module(path.replace('/','.')).run(session, {'db':db,'i':web.input()})
	def GET(self, path):
		raise web.seeother('/')

class link:
	def GET(self,sid):
		if 'url' in web.input():
			raise web.seeother(web.input()['url'])

		from m.inputfilter import fid
		id = fid(sid)
		if id is False:
			raise web.seeother('/')

		db = web.database(dbn='postgres', db='main', user='postgres', pw='fh3478hf38oh0ofh8fh7hre', host='130.211.97.197', port='5432')
		db.query("UPDATE links set clickc=clickc+1 where id="+id)

		if session.get('userid',0) != 0:
			urlrow = list(db.query("""
						SELECT
							links.url, history.id hid
						FROM
							links LEFT OUTER JOIN history ON links.id=history.id AND history.userid="""+str(session.userid)+"""
						WHERE
							links.id='"""+id+"""'
					  """))
			if len(urlrow) > 0 and urlrow[0]['hid'] is None:
				db.query("INSERT INTO history (userid,linkid) VALUES ("+str(session.userid)+",'"+id+"')")
				raise web.seeother(urlrow[0]['url'])
			else:
				raise web.seeother('/')
		else:
			urlrow = list(db.query("""
						SELECT
							url
						FROM
							links
						WHERE
							links.id='"""+id+"""'
					  """))

			if len(urlrow) > 0:
				raise web.seeother(urlrow[0]['url'])
			else:
				raise web.seeother('/')

class home:
	def GET(self, path):
		print path
		return """
				<!DOCTYPE html>
				<html>
					<head>
					    <link href='http://fonts.googleapis.com/css?family=Open+Sans:400,700,600' rel='stylesheet' type='text/css'>

					    <link rel="stylesheet" type="text/css" href="static/css/css.css" />
					    <link rel="stylesheet" type="text/css" href="static/css/excess.css" />
					    <link rel="stylesheet" type="text/css" href="static/css/mediaqs.css" />

					    <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
					    <link rel="icon" type="image/png" href="static/images/hubicon.png">

					    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=0">

					    <meta charset="UTF-8">

					    <title>WebArcs</title>
					    <meta name="description" content="A new way to subscribe to and discover websites!">

					    <script src="static/js/jquery-2.2.4.min.js"></script>
					    <script src="static/jscombined/main.js"></script>

						<link rel="apple-touch-icon" href="static/images/appicons/touch-icon-iphone.png">
						<link rel="apple-touch-icon" sizes="120x120" href="static/images/appicons/touch-icon-iphone-retina.png">

						<meta name="apple-itunes-app" content="app-id=1134949612">

						<meta itemprop="image" content="http://webarcs.com/static/images/WebArcsSquare/front.png">

					</head>
					<body>
					    <div id="shadecover" onclick="shadeOff(true)">
					    </div>
						<div id="holdoverscreen"></div>
					    <div id="notification" onclick="notifyhide()"></div>
					    <div id="main">
					        <div id="head">
					            <div id="shadecontainer">
					                <div id="logo">
					                    <span id="logoflower"></span>
					                    <span id="logotext"></span>
					                </div>
					                <div id="headoptions">
					                </div>
					            </div>
					        </div>
							<div id="toptabbar"></div>
							<div id="notifybar" onclick="hidenotify()"></div>
					        <div id="side" class="sideoff" style="display:none" onmouseover="stopbodyscrolling()" onmouseout="startbodyscrolling()">
					            <div id="related" class="relatedoff">
					                <div id="uibar">
					                    <img id="relback" class="off" onclick="pageback()" src="static/images/thinSideArrow.png"/>
					                    <img id="relforward" class="off" onclick="pageforward()" src="static/images/thinSideArrow.png"/>
					                    <img id="relclose" src="static/images/cross.png" onclick="sideOff()"/>
					                </div>
					                <div id="relpages"></div>
					            </div>
					        </div>
							<div id="filterseg" style="top: 44px;">
							</div>
							<div id="filshadow"></div>
					        <div id="pages" class=""></div>
					    </div>
					</body>
				</html>
				"""


if __name__ == "__main__":
	app.run(port=8080)
