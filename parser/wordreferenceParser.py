#!/usr/bin/env python3
###############################
# Rodrigo Cabrera Pena
# parser de wordreference.com para obtener sinonimos y definicion
# 30/09/2013
###############################

import json
import lxml.html
import urllib.request as request
from urllib.parse   import quote
#from lxml.cssselector import CSSSelector

class UrlHandler:
	_baseUrl = "http://www.wordreference.com/"
	_def = "definicion/"
	_syn = "sinonimos/"
	url = ""
	def __init__(self, typ="def"):
		if typ is "def":
			self.url = self._baseUrl + self._def
		else:
			self.url = self._baseUrl + self._syn

	def getHTML(self, word):
		opener = request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/19.0')]
		req = opener.open(self.url + quote(word))
		#req = request.urlopen(self.url + word)
		encoding = req.headers.get_content_charset()
		htmlText = req.read().decode(encoding)
		htm = lxml.html.fromstring(htmlText)
		return htm

class ParseHTML:
	def parseSyn(self, html):
		syn = []
		tags = html.xpath("//div[@class='trans clickable']/ul")
		if len(tags) == 0:
			return syn
		for i in tags[0] :
			if i.tag == "li":
				for x in i.xpath(".//text()"):
					syn += x.split(",")  
		return syn

	def parseDef(self, html):
		defs = []
		for i in html.xpath("//ol[@class='entry']")[0]:
			defs += [x for x in i.xpath(".//text()") if x != ' ' and x != ""]
		return defs


def getSynonyms(palabra):
	u2 = UrlHandler("syn");
	p = ParseHTML()
	return p.parseSyn(u2.getHTML(palabra));

def getDefinitions(palabra):
	u = UrlHandler("def")
	p = ParseHTML()
	return p.parseDef(u.getHTML(palabra));

if __name__ == '__main__':
	u = UrlHandler("def")
	u2 = UrlHandler("syn")


	p = ParseHTML()
	print(p.parseDef(u.getHTML("motor")))
	print(p.parseSyn(u2.getHTML("servicio")))
	#print (u.getHTML("bola"))