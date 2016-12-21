
import web
import random
from lxml import etree
parser = etree.XMLParser(strip_cdata=False)

def run(s,g):
	rssUrls = []
	if web.input(myfile={})['myfile'].value == '':
		return 'no file sent'
	tree = etree.XML(web.input(myfile={})['myfile'].value, parser)
	feeds = tree.xpath('//outline[@type="rss"]')
	for feed in feeds:
		print feed.attrib['title']
		if g['db'].query("select count(*) from hub where rssurl='"+feed.attrib['xmlUrl']+"'")[0]['count'] == 0:
			id = g['db'].insert('hub', name=feed.attrib['title'],rssurl=feed.attrib['xmlUrl'],url="",rsstype=True,hueangle=random.randint(0,359))
			g['db'].insert('refreshrate', arcid=id)
			g['db'].insert('subscriptions', uid=s.userid, fid=id)
	return 'v'
