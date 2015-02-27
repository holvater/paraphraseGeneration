#!/usr/bin/env python3
###############################
# Rodrigo Cabrera Pena
# parser de es.wiktionary.org para obtener sinonimos, hiperonimos y definicion
# 18/09/2013
###############################

import json
import lxml.html
import urllib.request as request
from urllib.parse import quote


class UrlHandler:
	_baseUrl = "http://es.wiktionary.org/w/api.php?"
	url = ""

	def __init__(self, action="parse", prop="text", format="json"):
		self.url = self._baseUrl + "&action=" + action + "&prop=" + prop + "&format=" + format + "&page="

	def getJSON(self, titles):
		req = request.urlopen(self.url + quote(titles))
		encoding = req.headers.get_content_charset()
		jsonText = json.loads( req.read().decode(encoding) )
		return jsonText

	def getExtracts(self, titles):
		extracts = []
		result = self.getJSON(titles)
		if "parse" in result:
			extracts.append(" ".join(result["parse"]["text"]["*"].splitlines()))
		return extracts

class Acepcion:
	def __init__(self, pos):
		self.pos = pos
		self.definiciones = []
		self.inflecciones = {}
		self.inflecciones["ms"] = None
		self.inflecciones["mp"] = None
		self.inflecciones["fs"] = None
		self.inflecciones["fp"] = None

	def printit(self):
		print (self.pos)
		for d in self.definiciones:
			print ("----")
			d.printit()
		print("............")
		print("ms -> ", self.inflecciones["ms"])
		print("mp -> ", self.inflecciones["mp"])
		print("fs -> ", self.inflecciones["fs"])
		print("fp -> ", self.inflecciones["fp"])

class Definicion:
	def __init__(self, definicion, syn=[], hyp=[], hip=[]):
		self.definicion = definicion
		self.syn = syn
		self.hyp = hyp
		self.hip = hip

	def printit(self):
		print (self.definicion)
		print ("Sinónimos: ", self.syn)	
		print ("Hiperónimos: ", self.hyp)	
		print ("Hipónimos: ", self.hip)	

class ParseExtract:
	""" 
	formato del html del api
	p
	h1
	dl
	---
	h3 - fem masc
	table - inflections  //table[contains(@class,'inflection-table')]/tr/td
	dl - lista de acepciones importantes
		dt dd
		dt dd
	---
	h3 - adj
	dl - lista de acepciones importantes
	---
	h2
	stuff

	"""
	_extractions = ["Sinónimos", "Definiciones", "Hiperónimos", "Hipónimos" ]
	def __init__(self,extract):
		self.innerHtml = lxml.html.fragments_fromstring(extract) #, create_parent="div"

	def _parseDl(self, dlTag):
		#de = dlTag.xpath("./dd")[0].xpath("string()").split(" Sinónim")[0]
		de = ''
		syn = dlTag.xpath('./dd/ul/li/b[contains(text(),"Sinónimo")]/ancestor::li//a//text()')
		hip = dlTag.xpath('./dd/ul/li/b[contains(text(),"Hipónimo")]/ancestor::li//a//text()')
		hyp = dlTag.xpath('./dd/ul/li/b[contains(text(),"Hiperónimo")]/ancestor::li//a//text()')
		return Definicion(de,syn,hyp,hip)

	def _parseTable(self, table, tipo):
		infs = table.xpath("//table[contains(@class,'inflection-table')][1]/tr/td//text()")
		dicc = {}
		dicc["ms"] = None
		dicc["mp"] = None
		dicc["fs"] = None
		dicc["fp"] = None
		if infs != []:
			if len(infs) >= 4:
				dicc["ms"] = infs[0]
				dicc["mp"] = infs[1]
				dicc["fs"] = infs[2]
				dicc["fp"] = infs[3]
			if len(infs) == 2:
				if "masculino" in tipo:
					dicc["ms"] = infs[0]
					dicc["mp"] = infs[1]
				if "femenino" in tipo:
					dicc["fs"] = infs[0]
					dicc["fp"] = infs[1]
		return dicc

	def parse(self):
		acepciones = []
		acepcion = None
		tipo = ""
		for x in self.innerHtml:
			if x.tag == "h3":
				if acepcion is not None:
					acepciones.append(acepcion)
				acepcion = Acepcion(x.xpath(".//text()")[0])
				tipo = x.xpath(".//text()")[0]
			elif x.tag == "table" and acepcion is not None:
				acepcion.inflecciones =  self._parseTable(x, tipo)
			elif x.tag == "dl" and acepcion is not None:
				acepcion.definiciones.append(self._parseDl(x))
			elif x.tag == "h2":
				break
		if acepcion is not None:
			acepciones.append(acepcion)
		return acepciones

def getSynonyms(palabra):
	ur = UrlHandler()
	syns = []
	for e in ur.getExtracts(palabra):
		par = ParseExtract(e)
		ace = par.parse()
		for a in ace:
			for de in a.definiciones:
				syns += de.syn
	return syns
		
def getHypernyms(palabra):
	ur = UrlHandler()
	hyps = []
	for e in ur.getExtracts(palabra):
		par = ParseExtract(e)
		ace = par.parse()
		for a in ace:
			for de in a.definiciones:
				hyps += de.hyp
	return hyps
	
def getHiponyms(palabra):
	ur = UrlHandler()
	hips = []
	for e in ur.getExtracts(palabra):
		par = ParseExtract(e)
		ace = par.parse()
		for a in ace:
			for de in a.definiciones:
				hips += de.hip
	return hips

def getDefinitions(palabra):
	ur = UrlHandler()
	des = []
	for e in ur.getExtracts(palabra):
		par = ParseExtract(e)
		ace = par.parse()
		for a in ace:
			for de in a.definiciones:
				des.append(de.definicion)
	return des

def getInflections(palabra):
	ur = UrlHandler()
	des = []
	for e in ur.getExtracts(palabra):
		par = ParseExtract(e)
		ace = par.parse()
		for a in ace:
			des = a.inflecciones
	return des

def getAll(palabra):
	ur = UrlHandler()
	res = []
	for e in ur.getExtracts(palabra):
		par = ParseExtract(e)
		ace = par.parse()
		for a in ace:
			for de in a.definiciones:
				#res.append(de.definicion)
				res += de.syn
				res += de.hyp
				res += de.hip
	return res
		
if __name__ == '__main__':
	ur = UrlHandler()

	for e in ur.getExtracts("perro"):
		par = ParseExtract(e)
		ace = par.parse()
		for acep in ace:
			acep.printit()

	# print(getSynonyms("perro"))
