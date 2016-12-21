import web
import re
from m.inputfilter import filmail
from m.accounts.checkmailfunc import checkmail

def run(s,g):
	if 'e' not in g['i'] or g['i']['e'] == '':
		return 'no email sent'
	return checkmail(g['db'], g['i']['e'])
