/*jshint multistr: true */

function searchStatichtml() {
	searchTimeOut = setTimeout(function() {
		$("#searchinput").focus();
	}, 600);
	return `
	<div id="searchform" class="empty">
		<input id="searchinput" placeholder="Enter feed name." type="text" oninput="searchHandler()" autocomplete="off" tabindex="1" value="" autocapitalize="off" autocorrect="off"><div id="searchcross" onclick="clearsearch()"></div><div id="searchenter" onclick="search()"></div>
	</div>
	<div id="searchresults"></div>
	`;
}

function search() {
	searchQuery($("#searchinput")[0].value);
}

$( window ).keypress(function(event) {
    if (event.which == 47) {
        $("#searchinput").focus();
    }
});

var lastq = "",
	searchTimeOut;

function searchHandler() {
	clearTimeout(searchTimeOut);
	var q = $("#searchinput")[0].value;
	if (q === "") {
		clearsearch();
		return false;
	}
	$("#searchform").removeClass('empty');
	searchTimeOut = setTimeout(function() {
		var q = $("#searchinput")[0].value;
		if (q != lastq) {
			searchQuery(q);
		}
		lastq = q;
	}, 950);
}

function searchQuery(q) {
	$("#searchresults").html(loadingicon);
	$.ajax({
		type: 'POST',
		url: 'f/generalweb/search',
		async: true,
		data: {'q':q},
		success:
			function (returnedData) {
				$("#searchresults").html(returnedData);
				$(".feedpostsbar[data-loadposts='True']").each(function(i,e) {
					loadposts(e.id,e.getAttribute('data-url'));
				});
			}
	});
}

function loadposts(id,url) {
	$('.feedpostsbar#'+id+' .postsbar').html(loadingicon);
	$.ajax({
		type: 'POST',
		url: 'f/generalweb/posts',
		async: true,
		data: {'url':url},
		success:
			function (returnedData) {
				if (returnedData == 'False') {
					$('.feedpostsbar#'+id).remove();
				} else {
					data = JSON.parse(returnedData);
					$(".feedpostsbar#"+id+" .nameholder").html('<img src="http://www.google.com/s2/favicons?domain_url='+data.url+'">'+data.name);
					$('.feedpostsbar#'+id+' .postsbar').html(data.posts);
					if (data.viewtype !== '') {
						$('.feedpostsbar#'+id).addClass(data.viewtype);
					}
					if (data.Subscribed) {
						$(".feedpostsbar#"+id+" .subscribe").removeClass('Subscribe');
						$(".feedpostsbar#"+id+" .subscribe").addClass('Subscribed');
						$(".feedpostsbar#"+id+" .subscribe").html('Subscribed');
					}
				}
			}
	});
}

function clearsearch() {
	$("#searchinput").val('');
	$("#searchform").addClass('empty');
	$("#searchresults").html('');
	$("#searchinput").focus();
}
