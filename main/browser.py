import os
import random
import sys
import time
import unicodedata
from bs4 import BeautifulSoup
from post import Post
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from person import Person
from post import FullPost

class Browser:
	"""docstring for Browser"""
	delay = 15
	def __init__(self):
		self.browser = webdriver.Firefox()
		#self.browser = webdriver.PhantomJS()
	def navigate(self, url, wait_for, error):
		try:
			print('Navigating to: ' + url)
			self.browser.get(url)
			element_present = expected_conditions.presence_of_element_located((By.ID, wait_for))
			WebDriverWait(self.browser, self.delay).until(element_present)
		except TimeoutException:
			sys.exit(error)

	def navigateC(self, url, wait_for, error):
		try:
			print('Navigating to: ' + url)
			self.browser.get(url)
			element_present = expected_conditions.presence_of_element_located((By.CLASS_NAME, wait_for))
			WebDriverWait(self.browser, self.delay).until(element_present)
		except TimeoutException:
			sys.exit(error)

	def enter_login_details(self, email, password):
		try:
			print('Entering login details')
			email_field = self.browser.find_element_by_id('email')
			pass_field = self.browser.find_element_by_id('pass')
			email_field.send_keys(email)
			pass_field.send_keys(password)
			pass_field.submit()
			element_present = expected_conditions.presence_of_element_located((By.ID, 'userNavigationLabel'))
			WebDriverWait(self.browser, self.delay).until(element_present)
		except TimeoutException:
			pass
			#sys.exit('Login with your credentials unsuccessful')
	#to join a group
	def joinGroup(self,id):
		try:
			self.navigate(
				url='https://www.facebook.com/groups/' + id,
				wait_for='joinButton_'+id,
				error='is already joined'
			)
			print('Joining the group')
			element = self.browser.find_element_by_id("joinButton_"+id)
			element.click()
		except NoSuchElementException:
			print('already Joined!')
			return False
	#to get for sale posts from a group
	def getPosts(self,group):
		print('Getting posts')
		self.browser.get('https://www.facebook.com/groups/'+group.id+'/forsaleposts/')
		self.scroll()
		print('Getting page Source')
		htmlPage = self.browser.page_source
		soup = BeautifulSoup(htmlPage,'html.parser')
		posts = soup.findAll("div", { "class" : "_4-u3 _9zl" })
		try:
			for ps in posts:
				img = ps.find("img", { "class" : "scaledImageFitHeight img" })
				titles = ps.find("span", { "class" : "_9zp" })
				title = ''
				for i in titles:
					title = i.string
				a = ps.find("a")
				link = a.attrs['href']
				price = ''
				location = ''
				desc = ''
				priceTag  = ps.find("div", { "class" : "_sz6" })
				if priceTag:
					price = priceTag.string
				locationTag  = ps.find("div", { "class" : "_2gqu" })
				if locationTag:
					location = locationTag.string
				descTag = ps.find("div", { "class" : "_5rfl" })
				if descTag:
					desc = descTag.string
				post  = Post(img,title,link,price,desc,location)
				group.posts.append(post)
		except Exception:
			print 'Error in getting posts'
		print(group.posts[0])

	def getPostsv2(self,group):
		print('Getting posts')
		self.browser.get('https://www.facebook.com/groups/'+group.id)
		#self.scroll()
		print('Getting page Source')
		htmlPage = self.browser.page_source
		soup = BeautifulSoup(htmlPage,'html.parser')
		posts = soup.findAll("div", { "class" : "_1dwg _1w_m _q7o" })
		for ps in posts:
			check = ps.find("div", { "class" : "_l52" })
			if check is not None:
				images = []
				imgs = ps.find("div", { "class" : "_2a2q _65sr" })
				if imgs is not None:
					al = imgs.find('a')
					images = self.extractImgs(al)
				titles = ps.find("div", { "class" : "_l53" })
				title = ''
				for i in titles:
					if i.string != '\n':
						title = i.string
				lt = ps.find("span", { "class" : "fsm fwn fcg" })
				a = lt.find("a")
				#link to the post in group
				link = a.attrs['href']
				#title time ex : 28/06/2018 01:26
				timeTitle = a.abbr.attrs['title']
				#data time ex : 1530145607
				timeData = a.abbr.attrs['data-utime']
				#time list
				time = [timeTitle,timeData]
				price = ''
				location = ''
				desc = ''
				priceTag  = ps.find("div", { "class" : "_l57" })
				if priceTag is not None:
					price = priceTag.string
				locationTag  = ps.find("div", { "class" : "_l58" })
				if locationTag is not None:
					location = locationTag.string
				descTag = ps.find("div", { "class" : "_5pbx userContent _3576" })
				if descTag is not None:
					desc = descTag.p.string
				pTag = ps.find("span", { "class" : "fwb fcg" })
				person = Person(pTag.a.string,pTag.a.attrs['href'])
				post  = FullPost(images,title,link,price,desc,location,time,person)
				print(post.__repr__())
				group.posts.append(post)
	def updatePosts(self,group):
		pass

	def scroll(self):
		SCROLL_PAUSE_TIME = 10

		last_height = self.browser.execute_script("return document.body.scrollHeight")
		#self.browser.execute_script("var scroll = setInterval(function(){ window.scrollTo(0,document.body.scrollHeight); }, 2000);")
		while True:
			print('scrolling')
			print(last_height)
			self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(SCROLL_PAUSE_TIME)
			new_height = self.browser.execute_script("return document.body.scrollHeight")
			print(new_height)
			if new_height == last_height:
				print('Stop scrolling')
				break
				#self.browser.execute_script("clearInterval(scroll);")
			print('llllll')
			last_height = new_height
			print(last_height)

		
	def extractImgs(self,als):
		imagesUrls = []
		url = als.attrs['ajaxify']
		self.browser.get(url)
		#self.navigateC(url=url,wait_for="_5810 _580_ img",error="images class not found")
		page = self.browser.page_source
		imageSoup = BeautifulSoup(page,'html.parser')
		imageTag = imageSoup.findAll("img", { "class" : " _580_ img" })
		imagesTag = imageSoup.findAll("img", { "class" : "_5810 _580_ img"})
		if imageTag is not None:
			print('images :')
			print(imageTag)
			for o in imageTag:
				imagesUrls.append(o.attrs['src'])
		if imagesTag is not None:
			for i in imagesTag:
				print('images :')
				print(i)
				imagesUrls.append(i.attrs['src'])
				#imagesUrls.append(im.attrs['src'])
		return imagesUrls
