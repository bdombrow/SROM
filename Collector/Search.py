#!/usr/bin/python

import time
import requests
import json
from abc import ABCMeta, abstractmethod

class BaseSearch:
	__metaclass__ = ABCMeta

	@abstractmethod
	def configure(self, info):
		pass

	@abstractmethod
	def getCounts(self, searchTerm):
		pass
		
	@abstractmethod
	def getID(self):
		pass

class GoogleSearch(BaseSearch):
	def __init__(self):
		pass
		
	def configure(self, info):
		self._ID = info['site_id']
		self._baseURL = info['url']
	
	def getCounts(self, searchTerm):
		url = self._baseURL.replace('SEARCHTERM', searchTerm)
		time.sleep(1) # Google has a 1 query/second limit	
		r = requests.get(url)
		r = r.text
		r = json.loads(r)
		return r[u'responseData'][u'cursor'][u'estimatedResultCount']
		
	def getID(self):
		return self._ID

class GoogleCustomSearch(BaseSearch):
	def __init__(self):
		pass
		
	def configure(self, info):
		self._ID = info['site_id']
		self._key = info['api_key']
		self._siteKey = info['site_key']
		self._baseURL = info['url']
		self._baseURL = self._baseURL.replace('APIKEY', self._key)
		self._baseURL = self._baseURL.replace('SITEKEY', self._siteKey)
		#pass
	
	def getCounts(self, searchTerm):
		url = self._baseURL.replace('SEARCHTERM', searchTerm)
		time.sleep(1) # Google has as 1 query/user/second limit
		r = requests.get(url).text
		r = json.loads(r)
		return r['searchInformation']['totalResults']
		
	def getID(self):
		return self._ID

class BingSearch(BaseSearch):
	def __init__(self):		
		pass
		
	def configure(self, info):
		self._ID = info['site_id']
		self._key = info['api_key']
		self._baseURL = info['url']
	
	def getCounts(self, searchTerm):
		url = self._baseURL.replace('SEARCHTERM', searchTerm)
		r = requests.get(url, auth=(self._key, self._key)).text
		r = json.loads(r)
		return r[u'd'][u'results'][0][u'WebTotal']

	def getID(self):
		return self._ID