import xml.etree.ElementTree as ET
from xml.dom import minidom
class Group:
	"""docstring for Group"""
	def __init__(self,id):
		self.id = id
		self.url = 'https://www.facebook.com/groups/' + id
		self.posts = []
	def toXml(self):
		posts = ET.Element('posts')
		for p in self.posts:
			print(p.__repr__())
			post = ET.SubElement(posts, 'post')
			if p.title is not None:
				post.set('title',p.title)
			else:
				post.set('title','')
			if p.url is not None:
				post.set('url',p.url)
			else:
				post.set('url','')
			if p.price is not None:
				post.set('price',p.price)
			else:
				post.set('price','')
			if p.desc is not None:
				post.set('desc',p.desc)
			else:
				post.set('desc','')
			if p.location is not None:
				post.set('location',p.location)
			else:
				post.set('location','')
			time  = ET.SubElement(post,'time')
			if p.time[0] is not None:
				time.set('timeT',p.time[0])
			else:
				time.set('timeT','')
			if p.time[1] is not None:
				time.set('timeU',p.time[1])
			else:
				time.set('timeU','')
			person = ET.SubElement(post,'person')
			if p.person.name is not None:
				person.set('name',p.person.name)
			else:
				person.set('name','')
			if p.person.url is not None:
				person.set('url',p.person.url)
			else:
				person.set('url','')
			images = ET.SubElement(post,'imagesUrls')
			for image in p.imageUrls:
				url = ET.SubElement(images,'image')
				if image is not None:
					url.set('src',image)
				else:
					url.set('src','')
		print(posts)
		if posts is not None:
			mydata = ET.tostring(posts)
			xmlfile = open("posts.xml","w","utf-8")
			xmlfile.write(mydata)
	def toDb(self):
		md = minidom.parse('posts.xml')
		posts = md.getElementsByTagName('post')
		for i in posts:
			print(i.attributes['title'].value)
			#chlidnodes we have time -> 0, person -> 1, imagesUrls -> 2 
			print(i.childNodes[0].attributes['timeT'].value)
	def __repr__(self):
		return str(self.__dict__)