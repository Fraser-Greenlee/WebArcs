
import web

db = web.database(dbn='postgres', db='main', user='postgres', pw='fh3478hf38oh0ofh8fh7hre', host='130.211.97.197', port='5432')
q = db.query("SELECT email from users")
for r in q:
	requests.post(
			"https://api.mailgun.net/v3/mg.webarcs.com/messages",
			auth=("api", "key-fde98f1eb655d8778c7df6c20f24b438"),
			data={"from": "WebArcs <mailgun@mg.webarcs.com>",
				  "to": [r['email']],
				  "subject": "Redesign + App Beta",
				  "html": """
				  	<html>
						<body style="margin:0px; font-family:Tahoma, Geneva, sans-serif;">
							<div style="padding:24px; font-size:17px;">


								When you signed up the site was barely just 'finished'.<br />
								<br />
								Back when you signed up the site was just 'useable' and a mess (so thank you for doing that!).<br>
								<br>




								We've now got an iOS app beta out and we'll be sending out invites soon.<br>
								Also got the site properly working with a new style to it


								To confirm your email address click the link below.<br />
							</div>
						</body>
					</html>
				  """"}
	)



"""

<html>
<body style="margin:0px; font-family:Tahoma, Geneva, sans-serif;">
<h1>Hi there we got an iOS App Beta!</h1>

Email invites are coming soon and we're super excited to hear what you think of it.

Also..

<h1>Redesign</h1>

The site has a whole new look to it and way more content.

(Works best on mobile.)

<a href="http://webarcs.com">See it for yourself.</a>


<a style="color:gray" href="webarcs.com/link/scDDSv0yuAS">don't email me</a>
</body>
</html>

"""
