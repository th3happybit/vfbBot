class Person:
	"""docstring for Person"""
	def __init__(self, name,url):
		self.name = name
		self.url = url

	def __repr__(self):
		return str(self.__dict__)