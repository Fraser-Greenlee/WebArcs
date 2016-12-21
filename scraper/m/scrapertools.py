# -*- coding: utf-8 -*-

def cutStr(st, lim):
	if len(st) > lim:
		return st[:lim-3]+'...'
	else:
		return st
