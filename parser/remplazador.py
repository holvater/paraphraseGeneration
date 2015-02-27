#!/usr/bin/env python3
###############################
# Rodrigo Cabrera Pena
# 
# 11/11/2013
###############################

import wiktionaryParser as wp

oracion = str(input("> "))
for p in oracion.split(" "):
	print (p)
	remplazos = []
	remplazos += wp.getAll(p) 
	#remplazos.append(wp.getHypernyms(p))
	#remplazos.append(wp.getHiponyms(p))
	#remplazos.append(wp.getDefinitions(p))
	#print (remplazos)
	for w in remplazos:
		print(oracion.replace(" " + p + " "," " + w + " "))

