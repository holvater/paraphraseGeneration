#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
###############################
# Rodrigo Cabrera Pena
# programa de linea de comandos para generacion de parafrasis
# 20/08/2014
###############################

import argparse
import sys
import analyzer
stdout = sys.stdout;

aparser = argparse.ArgumentParser(description="generacion de parafrasis de manera automatica");

aparser.add_argument("-v", "--verbose", help="imprimir proceso", action="store_true");
aparser.add_argument("-o", "--output", help="archivo de salida");
aparser.add_argument("-l", "--limit", help="limite de parafrasis mostradas");
aparser.add_argument("-t", "--type", help="tipo de parafrasis a generar, sys -> sinonimos, hyp -> hiperonimos e hiponimos");

args = aparser.parse_args();

data = input("introduce una oracion>> ");

if args.output:                                                     
    outpath = args.output;
    outfile = open(outpath, "w");
    sys.stdout = outfile;

limit=100
if args.limit:
    limit = int(args.limit);

typ="syn"
if args.type and args.type=="hyp":
    typ = args.type;


for s in analyzer.generarParafrasis(data,typ, limit):
	print(s);

