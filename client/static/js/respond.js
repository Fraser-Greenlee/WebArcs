
function respond(id,responce) {
	if ($("#"+responce+"hold"+id).hasClass('voted')) {
		$("#"+responce+"hold"+id).removeClass('voted');
	} else {
		$("#"+responce+"hold"+id).addClass('voted');
	}
	$.post(
		"f/editors/respond",
		{
			'id':id,
			'responce':responce
		},
		function (msg) {
			console.log('msg,');
			console.log(msg);
			if (msg == 'inserted') {
				if ($("#"+responce+"hold"+id).hasClass('voted') === false) {
					$("#"+responce+"hold"+id).addClass('voted');
				}
				if (['like','dislike'].indexOf(responce) > -1) {
					if (responce == 'like') {
						$("#likehold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())+1);
						if ($("#dislikehold"+id).hasClass('voted')) {
							$("#dislikehold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())-1);
							$("#dislikehold"+id).removeClass('voted');
						}
					} else {
						$("#dislikehold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())+1);
						if ($("#likehold"+id).hasClass('voted')) {
							$("#likehold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())-1);
							$("#likehold"+id).removeClass('voted');
						}
					}
				}
			} else {
				if ($("#"+responce+"hold"+id).hasClass('voted')) {
					$("#"+responce+"hold"+id).removeClass('voted');
				}
				if (['like','dislike'].indexOf(responce) > -1) {
					$("#"+responce+"hold"+id+" span").text(parseInt($("#"+responce+"hold"+id+" span").text())-1);
				}
			}
		}
	);
}

function opencomments(id) {
	if ($(".rid"+id+" #commentbox").hasClass("shut")) {
		$(".rid"+id+" #commentbox").removeClass("shut");
	} else {
		$(".rid"+id+" #commentbox").addClass("shut");
	}
}

function share(url) {
	hovermsq('<span>'+url+'<span>');
}
