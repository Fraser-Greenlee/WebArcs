

function moreStatichtml() {
	if (userid == '0') {
		return `
			<ol>
				<li>Signup to access extra features.</li>
			</ol>
		`;
	} else {
		return `
			<ol>
				<li onclick="connectsite('twitter')"><img src="static/images/sites/twitter.png">Connect</li>
				<li onclick="connectsite('opml')">Upload OPML File</li>
				<li onclick="logout()">Logout</li>
			</ol>
		`;
	}
}
