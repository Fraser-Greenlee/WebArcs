import hashlib

def setpass(inp):
	try:
		return hashlib.sha1("icTYCCYiOR6RX6CYCytdCTYdTYTdTYFkGHj-"+inp).hexdigest()
	except:
		return False