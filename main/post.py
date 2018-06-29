class Post:
	"""docstring for Post"""
	def __init__(self,imageUrl,title,url,price,desc,location):
		self.imageUrl = imageUrl
		self.title = title
		self.url = url
		self.price = price
		self.desc = desc
		self.location = location
	def __repr__(self):
		return str(self.__dict__)

class FullPost:
	"""docstring for FullPost"""
	def __init__(self,imageUrls,title,url,price,desc,location,time,person):
		self.imageUrls = imageUrls
		self.title = title
		self.url = url
		self.price = price
		self.desc = desc
		self.location = location
		self.time = time
		self.person = person
	def __repr__(self):
		return str(self.__dict__)

		