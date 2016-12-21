# -*- coding: utf-8 -*-

import web

def run(s,g):
	if 'id' not in g['i']:
		return 'no feed selected'

	if 'more' in g['i']:
		offset = ' OFFSET '+str(int(set_post_max)*int(g['i']['more']))
	else:
		offset = ''

	ret = ''
	q = g['db'].query("SELECT links.* from links where links.pageid='"+g['i']['id']+"' order by id desc limit "+set_post_max+offset)
	for row in q:
		row = fixVals(row,[])
		ret += make( postTemp, merge_dicts(row, {'isSub':'isSub', 'fromstring':'x'}) )
	return ret
