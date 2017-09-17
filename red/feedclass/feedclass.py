
from findurl import findurl
from getdata import getdata, dbdata
from getposts import getposts

class Feed:
	def __init__(self,url,*db):
		if len(db) > 0:
			self.db = db[0]
		else:
			self.db = False

		# get content   v(incase unicode)
		res = findurl(str(url),self.db)
		if res is False:
			raise Exception('No feed found.')
		self.rssurl = res['url']
		self.request = res['req']
		self.doctype = res['doctype']
		self.domain = res['domain']
		self.stored = res['stored']
		self.contenttype = res['contenttype']

		# get info
		if self.stored:
			data = dbdata(self.rssurl,self.db)
		else:
			data = getdata(self.request.content, self.doctype)

		self.checktype = data['checktype']
		self.id = data['id']
		self.name = data['name']
		self.url = data['url']
		self.hidden = data['hidden']
		self.siteid = data['siteid']
		self.postdate = data['postdate']
		self.tree = data['tree']
		self.viewtype = data['viewtype']
		self.posts = False

	def getposts(self):
		if self.posts is False:
			self.posts = getposts(self,self.db)
		return self.posts

	def save(self):
		if self.db is False:
			raise Exception('self.db is False')
		elif self.stored:
			raise Exception('feed is already stored')
		id = self.db.insert('hub', name=self.name, url=self.url, rssurl=self.rssurl, checktype=self.checktype, domain=self.domain)
		self.id = id
		self.saveposts()
		self.db.insert('refreshrate', arcid=id)
		self.stored = True
		return id

	def saveposts(self):
		if self.db is False:
			raise Exception('db is False')
		elif self.stored:
			raise Exception('feed is already stored')
		self.db.insertlist('linkstobeindexed',self.getposts())


	def subscribe(self,uid):
		if self.stored is False:
			raise Exception('feed is not saved')
		if self.id is False:
			raise Exception('feed has no id')
		if self.db is False:
			raise Exception('feed db is false')

		if self.db.count('subscriptions', uid=uid, fid=self.id) > 0:
			self.db.remove('subscriptions', uid=uid, fid=self.id, limit=1)
			return 'unsubscribed'
		else:
			self.db.insert('subscriptions', uid=uid, fid=self.id)
			return 'subscribed'
