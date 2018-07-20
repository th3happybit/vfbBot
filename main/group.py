import xml.etree.ElementTree as ET
from xml.dom import minidom
from post import FullPost
from person import Person
from os import listdir,remove
from os.path import isfile, join
class Group:
	"""docstring for Group"""
	update = False
	def __init__(self,id):
		self.id = id
		self.url = 'https://www.facebook.com/groups/' + id
		self.posts = []
	def toXml(self):
			posts = ET.Element('posts')
			self.posts.reverse()
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
				mydata = ET.tostring(posts, encoding="unicode")
				xmlfile = open("posts/"+str(self.id)+".xml","w", encoding="utf8")
				xmlfile.write(mydata)
				return True
	def init(self):
		try:
			md = minidom.parse('posts/'+self.id+'.xml')
			posts = md.getElementsByTagName('post')
			for i in posts:
				p = Person(name=i.childNodes[1].attributes['name'].value,url=i.childNodes[1].attributes['url'].value)
				post = FullPost(imageUrls='',title=i.attributes['title'].value,url=i.attributes['url'].value,price=i.attributes['price'].value,desc=i.attributes['desc'].value,location=i.attributes['location'].value,time=[i.childNodes[0].attributes['timeT'].value,i.childNodes[0].attributes['timeU'].value],person=p)
				self.posts.append(post)
			return True
		except FileNotFoundError:
			print('fine not found')
			return False
	def update(self,update):
		nposts = []
		oldposts = self.posts
		print(self.posts)
		oldlen = len(oldposts)
		newposts = update.posts
		breaker = False
		for op in oldposts:
			for np in newposts:
				if op.url == np.url:
					print('finding match stoping ...')
					breaker = True
					break
				else:

					print('adding ...')
					nposts.append(np)
			if breaker == True:
				break
		if len(nposts) == 0:
			print('no new posts')
			return False
		else:
			oldposts.reverse()
			nposts.reverse()
			for np in nposts:
				oldposts.append(np)
			if len(oldposts) > oldlen:
				self.posts = oldposts
			return True
	def delete(self):
		file = 'posts/'+self.id+'.xml'
		print(file)
		if isfile(file):
			remove(file)
			return True
		else:
			return False

	def __repr__(self):
		return str(self.__dict__)