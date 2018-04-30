#coding=utf-8
#update at 2018-4-20
from http.client import IncompleteRead
from mzitu.items import ImageItem
import scrapy
import numpy as np
import os

class mzituimages(scrapy.Spider):
	"""docstring for acgimages"""
	name = 'images'
	start_urls = [
		"http://www.mm131.com/xinggan/list_6_2.html"
	]
	page = 1
	count = 0
	MAX_CATCH_PAGES = 1000
	item = ImageItem()
	def parse(self,response):
		next_page = response.xpath('//div[@class="main"]//a/@href').re(r'http://www.mm131.com/xinggan/([0-9]+)\.html')
		used = []
		for page in next_page:
			if page not in used:
				used.append(page)
		print('find %d secound pages' % len(used))
		for number in used:
			url = "http://www.mm131.com/xinggan/%s.html" % number
			print('url = %s' % url)
			self.item['url'] = url
			yield scrapy.Request(url, callback = self.post_page)

		if self.page < self.MAX_CATCH_PAGES:
			self.page = self.page + 1
		next_url = "http://www.mm131.com/xinggan/list_6_%d.html" % self.page
		yield scrapy.Request(next_url, callback = self.parse)

	def post_page(self,response):
		images_url = response.xpath("//div[@class='content-pic']//img/@src").extract()
		print('find %d images' % len(images_url))
		print('image url = %s' % images_url)
		self.item['images'] = images_url
		return self.item
