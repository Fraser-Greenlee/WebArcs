
String.prototype.capFirst = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

function replaceList(str,replist){
	var evenkeys = Array.apply(null, Array(replist.length/2)).map(function (_, i) {return i*2;});
	evenkeys.forEach(function(even) {
		str = str.replaceAll(replist[even], replist[even+1]);
	});
	return str;
}
