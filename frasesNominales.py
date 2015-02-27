#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
###############################
# Rodrigo Cabrera Pena
# identificacion de frases nominales dentro de un arreglo con palabras
# 20/08/2014
###############################

def parteDeGrupoNominal(dicc):
	if dicc is None:
		return False;
	if esNombre(dicc) or dicc['tag'].find("AQ") != -1 or dicc['tag'].find("DA") != -1 or dicc['tag'].find("DI") != -1:
		return True;
	else:
		return False;

def esNombre(dicc):
	if dicc['tag'].find("NC") != -1:
		return True;
	else:
		return False;


def trataGrupoNominal(source):
	l = len(source);
	if l > 1 :
		if parteDeGrupoNominal(source[1]):
			if l > 2:
				if parteDeGrupoNominal(source[2]):
					return [[source.pop(0),source.pop(0),source.pop(0)]];
				else :
					return [[source.pop(0),source.pop(0)],source.pop(0)['form']];
			else:
				return [[source.pop(0),source.pop(0)]];
		else:
			if esNombre(source[0]):
				return [[source.pop(0)],source.pop(0)['form']];
			else:
				return [source.pop(0)['form'],source.pop(0)['form']];
	else:
		if esNombre(source[0]):
			return [[source.pop(0)]];
		else:
			return [source.pop(0)['form']];

def obtenerGruposNominales(source):
	out = [];
	while source:
		l = len(source);
		item = source[0];
		if parteDeGrupoNominal(item):
			out += trataGrupoNominal(source);
		else:
			out += [source.pop(0)['form']];

	return out;
