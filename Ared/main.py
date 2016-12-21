import web
import importlib
from urllib import quote_plus

web.config.debug = False

urls = (
	'/feed(.*)', 'feed',
	'/(.*)', 'home'
)

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = MyApplication(urls, globals())

class home:
	def GET(self,path):
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

					    <title>RED</title>
					    <meta name="description" content="A new way to browse reddit.">

					    <script src="static/js/jquery-2.2.4.min.js"></script>
					    <script src="static/jscombined/main.js"></script>

						<link rel="apple-touch-icon" href="static/images/appicons/touch-icon-iphone.png">
						<link rel="apple-touch-icon" sizes="120x120" href="static/images/appicons/touch-icon-iphone-retina.png">

						<meta name="apple-itunes-app" content="app-id=1134949612">

						<meta itemprop="image" content="http://webarcs.com/static/images/WebArcsSquare/front.png">

					</head>
					<body>
				        <div id="head">
				        	<span onclick="viewFeed()" id="feedbut" class="selected">Feed</span><span onclick="viewSubs()" id="subsbut">Subs</span>
				        </div>
						<div id="body">
							<div id="Feed" class="open"></div>
							<div id="Subs"></div>
						</div>
					</body>
				</html>
				"""

class feed:
	def POST(self, path):
		from m.template import Template
		feedbarTemp = Template('feedbarposts')
		postTemp = Template('post')
		db = web.database(dbn='postgres', db='main', user='postgres', pw='fh3478hf38oh0ofh8fh7hre', host='130.211.97.197', port='5432')
		q = db.query("""
			SELECT
			    *
			FROM
			    (
				SELECT
				    row_number() OVER (PARTITION by aredditposts.sub ORDER BY aredditposts.id DESC),
				    aredditposts.*,
				    max(aredditposts.id) OVER (PARTITION by aredditposts.sub) AS mxid
				FROM
				    aredditposts, asubs
				WHERE
				    aredditposts.sub=asubs.name
				ORDER BY
				    aredditposts.id DESC
			    ) x
			WHERE
	    		ROW_NUMBER < 11
			""")
		res = ''
		currentsub = ''
		for r in q:
			if currentsub != r['sub']:
				if currentsub != '':
					res += feedbarTemp.process({'name':currentsub}, posts=posts)
				currentsub = r['sub']
				posts = ''
			posts += postTemp.process(r)
		res += feedbarTemp.process({'name':currentsub}, posts=posts)

		return res



if __name__ == "__main__":
	app.run(port=8080)
