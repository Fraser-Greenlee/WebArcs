
start = [
	'globals'
]

end = [
	'onload'
]

from os import listdir

def filterscripts(scripts):
	nscr = []
	jn = start+end+['jquery-2.2.4.min']
	for scr in scripts:
		if scr[0] != '.' and scr[-3:] == '.js' and scr[:-3] not in jn:
			nscr.append(scr[:-3])
	return nscr

scripts = filterscripts(listdir('static/js'))

js = ""
for script in start+scripts+end:
	f = open('static/js/'+script+'.js','r')
	js += """

//!!!! """+script+""".js

"""+f.read()+"""

"""
	f.close()

main = open('static/jscombined/main.js','w')
main.write(js)
main.close()
