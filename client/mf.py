"""
requests.post(
		"https://api.mailgun.net/v3/mg.webarcs.com/messages",
		auth=("api", "key-fde98f1eb655d8778c7df6c20f24b438"),
		data={"from": "WebArcs <mailgun@mg.webarcs.com>",
			  "to": ["fraser.greenlee@mac.com"],
			  "subject": "Test",
			  "text": 'client'}
)
"""
