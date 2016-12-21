
function pageback() {
	if ($('#relpages #relpage:not(.closed)').length > 1) {
		$('#relpages #relpage:not(.closed)').last().addClass('closed');
		$('#relforward').attr('class','on');
		$('#related').scrollTop(0);
		if ($('#relpages #relpage:not(.closed)').length < 2) {
			$('#relback').attr('class','off');
		}
	}
}
function pageforward() {
	if ($('#relpages #relpage.closed').length > 0) {
		$('#relpages #relpage.closed').last().removeClass('closed');
		$('#relback').attr('class','on');
		$('#related').scrollTop(0);
		if ($('#relpages #relpage.closed').length === 0) {
			$('#relforward').attr('class','off');
		}
	}
}
