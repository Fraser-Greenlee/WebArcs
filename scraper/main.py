import web
web.config.debug = True

urls = (
	'/(.*)', 'job'
)

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = MyApplication(urls, globals())

def get_a_job(path):
	if not path:
		return ''
	import os.path
	if(os.path.exists(path+'.py')):
		import importlib
		return importlib.import_module(path.replace('/','.')).run()

class job:
	def POST(self, path):
		return get_a_job(path)
	def GET(self, path):
		return get_a_job(path)

if __name__ == "__main__":
	app.run(port=8080)
