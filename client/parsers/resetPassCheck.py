import web

from m.inputfilter import filmail, fstring
from m.accounts.validForPassReset import validForPassReset

def run(s,g):
	if 'e' not in g['i'] or 'c' not in g['i']:
		return False
	return validForPassReset(g['db'], filmail(g['i']['e']), fstring(g['i']['c']))
