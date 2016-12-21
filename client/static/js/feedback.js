/*jshint multistr: true */

function getfeedback() {
	if (userid === "") {
		hovermsq("\
			<h1>Hi there we'd love to hear what you think WebArcs.</h1>\
			<p>\
				WebArcs is super new and it will be shaped by your feedback.<br>\
				You can get in touch by signing up and comming back here.\
			</p>\
		");
	} else {
		hovermsq("\
			<h1>Hi there we'd love to hear what you think of WebArcs.</h1>\
			<p>\
				We'll be sending you an email for feedback soon but until then you can message us on twitter <a href='https://twitter.com/FraserGreenlee' target='_blank'>@WebArcs</a>\
			</p>\
		");
	}
}
