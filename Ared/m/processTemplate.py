
import re
import random

from m.fixVals import fixVals

convertData = {
	'hub':{'name':'hubname','url':'huburl','id':'pageid'}
}
def convert(k,r):
	for ch in convertData[k]:
		if ch in r:
			r[convertData[k][ch]] = r[ch]
			del r[ch]
	return r

def dicTohtml(temp,valdict):
	for k in valdict:
		if valdict[k] != '':
			temp = re.sub('{'+k+'}', unicode(valdict[k]), temp, flags=re.MULTILINE | re.DOTALL)
	return temp

def getTemp(name):
	keyval = []
	haskey = []
	temp = open('templates/'+name+'.html','r').read()
	questions = re.findall('{{(.*?)} \[(.*?)\]}', temp, flags=re.MULTILINE | re.DOTALL)
	replacelist = re.findall('{{.*?\[.*?\]}', temp, flags=re.MULTILINE | re.DOTALL)
	i = {'global':0,'haskey':0,'keyval':0}
	for q in questions:
		q = list(q)
		q[0] = q[0].split()
		if len(q[0]) == 1:
			haskey.append([q[0][0],q[1]])
			temp = temp.replace(replacelist[i['global']],'{haskey'+str(i['haskey'])+'}')
			i['haskey'] += 1
		else:
			keyval.append([ q[0][0] , q[0][2].split(',') , q[1] ])
			temp = temp.replace(replacelist[i['global']],'{keyval'+str(i['keyval'])+'}')
			i['keyval'] += 1
		i['global'] += 1
	return {'keyval':keyval,'haskey':haskey,'temp':temp}


def process(temp, values, **extra):
	values = fixVals(values)
	extraextra = {}
	i = 0
	for keyval in temp['keyval']:
		if keyval[0] in values and str(values[keyval[0]]) in keyval[1] or keyval[0] in extra and str(extra[keyval[0]]) in keyval[1]:
			extraextra['keyval'+str(i)] = keyval[2]
		i += 1
	i = 0
	for haskey in temp['haskey']:
		if haskey[0] in values and values[haskey[0]] not in  ['',None] or haskey[0] in extra and extra[haskey[0]] not in  ['',None]:
			extraextra['haskey'+str(i)] = haskey[1]
		i += 1
	output = temp['temp']
	for valdict in [extraextra,values,extra]:
		output = dicTohtml(output,valdict)
	return re.sub('{[A-Za-z0-9 ]*?}', '', output, flags=re.MULTILINE | re.DOTALL)


###

def make(temp, values, extra):
	values = fixVals(values)
	extraextra = {}
	i = 0
	for keyval in temp['keyval']:
		if keyval[0] in values and str(values[keyval[0]]) in keyval[1] or keyval[0] in extra and str(extra[keyval[0]]) in keyval[1]:
			extraextra['keyval'+str(i)] = keyval[2]
		i += 1
	i = 0
	for haskey in temp['haskey']:
		if haskey[0] in values and values[haskey[0]] not in  ['',None] or haskey[0] in extra and extra[haskey[0]] not in  ['',None]:
			extraextra['haskey'+str(i)] = haskey[1]
		i += 1
	output = temp['temp']
	for valdict in [extraextra,values,extra]:
		output = dicTohtml(output,valdict)
	return re.sub('{[A-Za-z0-9 ]*?}', '', output, flags=re.MULTILINE | re.DOTALL)
