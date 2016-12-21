/*jshint multistr: true */

var addforms = {

	'twitter':'\
		<h2><img src="static/images/sites/twitter.png">Add your twitter follows.</h2>\
		<span>@<input type="text" placeholder="Your Username"></span>\
		<button onclick="addtwitter()">Submit</button><button class="cancel" onclick="closeauth()">Cancel</button>',

	'opml':'\
		<form method="POST" enctype="multipart/form-data" action="fs/api/xmlfeeds">\
			<h1>Upload OPML file.</h1>\
			<input type="file" name="myfile" />\
			<br/>\
			<input type="submit" />\
		</form>\
		<button class="cancel outside" onclick="closeauth()">Cancel</button>'
};

function connectsite(site) {
	if ($('#authform').length === 0) {
		$('#main').append('<div id="authform" class="'+site+'">'+addforms[site]+'</div>');
		shadeOn('closeauth');
	}
}

function closeauth() {
	$('#authform').remove();
	shadeOff();
}

function addtwitter() {
	if ($('#authform').length !== 0 && $('#authform input')[0].value !== "") {
		$.ajax({
	        type: 'POST',
	        url: 'f/api/twitter/getuserfriends',
	        async: true,
	        data: {'name':$('#authform input')[0].value},
	        success:
	            function (returnedData) {
	            	console.log(returnedData);
					$('#authform').remove();
	            }
	    });
	}
}

function addnewfeed(e) {
	$(e).addClass('loading');
	$.ajax({
        type: 'POST',
        url: 'f/addfeed/add',
        async: true,
        data: {'id':$(e).attr('data-id')},
        success:
            function (returnedData) {
				if (returnedData == 'v') {
					closesearch();
					notifyshow('Added to your feeds.');
					$(e).html('Added');
				} else {
					$(e).addClass('error');
					$(e).html(returnedData);
				}
            }
    });
}

function addurlfeed(e) {
	$(e).addClass('loading');
	$.ajax({
        type: 'POST',
        url: 'f/addfeed/add',
        async: true,
        data: {'url':$(e).attr('data-url')},
        success:
            function (returnedData) {
				if (returnedData == 'v') {
					closesearch();
					notifyshow('Added to your feeds.');
					$(e).html('Added');
				} else {
					$(e).addClass('error');
					$(e).html(returnedData);
				}
            }
    });
}
