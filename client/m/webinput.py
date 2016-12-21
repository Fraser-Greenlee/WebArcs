
import web

from m import inputfilter

'''
info

'*setup' [
	print = print error messages,
	needall = return error message on missing any input,
	loggedin = return error if not logged in,
]
# ^ all are default true define false as, 'param',False


'param':filter/False
	(False means no filter)
'''

def nothave(d,params):
	for p in params:
		if p not in d or d[p] in ['',False]:
			return True
	return False

def leniantlist(k,l):
	pos = l.index(k)
	if pos == len(l)-1:
		return True
	elif type(l[pos+1]) == bool:
		return l[pos+1]
	else:
		return True

def webinput(s,g,params):

	prnting = False
	needall = False
	if '*setup' in params:
		setup = params['*setup']

		if 'print' in setup:
			prnting = leniantlist('print',setup)

		if 'loggedin' in setup:
			if leniantlist('loggedin', setup):
				if s.get('userid',0) == 0:
					return '<end/>must be logged in'
			else:
				if s.get('userid',0) != 0:
					return '<end/>must not be logged in'

		if 'needall' in setup:
			if leniantlist('needall', setup):
				needall = True

		del params['*setup']

	d = {}
	for param in params:
		if param not in g['i']:
			if needall:
				if prnting:
					print 'bad data', param, 'not in', g['i']
				return '<end/>bad data'
			else:
				continue

		if params[param] == False:
			d[param] = g['i'][param]
		else:
			# call inputfilter from string
			val = getattr(inputfilter,params[param])(g['i'][param])
			if val in [False,'']:
				if needall:
					if prnting:
						print 'bad input ', param, '=', g['i'][param], ' filtered to', d[param]
					return '<end/>bad data'
			else:
				d[param] = val

	return d
