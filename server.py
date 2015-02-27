#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from bottle import route, run, template, debug, request, get, post, static_file
import analyzer

def generarParafrasis(oracion, cantidad):
    try:
        result = analyzer.generarParafrasis(oracion,"syn",cantidad);
        return result;
    except ValueError:
        pass
    

# Static Routes
@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')

@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='static/fonts')


@get('/')
def index():
    return template('template', oraciones=[], oracion='', cantidad=1)

@post('/')
def posted():
    oraciones = []
    oracion = ''
    cantidad = 1
    if request.forms.get('generar','').strip():
        oracion = request.forms.get('oracionInput').encode('latin1').decode('utf8')
        cantidad = int(request.forms.get('cantidadInput'))
        if oracion[-1] != ".":
            oracion += '.'

        print(oracion)
        oraciones = generarParafrasis(oracion, cantidad)
    return template('template', oraciones=oraciones, oracion=oracion, cantidad=cantidad)

debug(True)
run(host='localhost', port=8080, reloader=True)
