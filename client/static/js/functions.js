
function stopPropagation(e) {
	if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();
	e.preventDefault();
	return false;
}

function subscribe(inp,e) {
	if (e !== undefined) {
		if (!e) var e = window.event;
	    e.cancelBubble = true;
	    if (e.stopPropagation) e.stopPropagation();
		e.preventDefault();
	}

	if (userid == "0") {
		notifyshow('To Subscribe <button class="loglink" onclick="setpage(\'signup\')">Signup</button>');
	} else {

		console.log('Subscribe: '+inp);

		var urltype = inp[0] == 'h';
		if (urltype) {
			var data = {
					'url':inp
				};
		} else {
			var data = {
					'id':inp
				};
		}
		if (urltype) {
			id = $('*[data-url="'+inp+'"]')[0].id;
		} else {
			id = inp;
		}
		$("#sub_"+id).attr('class','subscribe loading');
		$.ajax({
			type: 'POST',
			url: 'f/editors/subscribe',
			async: true,
			data: data,
			success:
				function (returnedData) {
					subscribeRet(id,returnedData);
				}
		});
	}
	return false;
}
function subscribeRet(id,returnedData) {
	if (returnedData == 'subscribed') {
		$("#sub_"+id)
			.html("Subscribed")
			.attr('class','subscribe off Subscribed');
		$(".feedpostsbar#"+id).removeClass('unsubbed');
	} else if (returnedData == 'unsubscribed') {
		$("#sub_"+id)
			.html("Subscribe")
			.attr('class','subscribe Subscribe');
		$(".feedpostsbar#"+id).addClass('unsubbed');
	} else {
		console.log('error, '+returnedData);
	}
}

function notifyshow(msg) {
	$("#notification").html(msg);
	$("#notification").addClass('showing');
}
function notifyhide() {
	$('#notification').removeClass('showing');
}
