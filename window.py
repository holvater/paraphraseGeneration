#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
###############################
# Rodrigo Cabrera Pena
# GUI para generacion de parafrasis
# 20/08/2014
###############################

from tkinter import *
from tkinter import ttk

import analyzer

def generarParafrasis(*args):
    try:
        value = source.get();
        limit = int(w.get());
        result = analyzer.generarParafrasis(value,"syn",limit);
        output.delete(0, END);
        for sentence in result:
            output.insert(END, sentence);
    except ValueError:
        pass
    
root = Tk();
root.title("Generar parafrasis");

mainframe = ttk.Frame(root, padding="3 3 12 12");
mainframe.grid(column=0, row=0, sticky=(N, W, E, S));
mainframe.columnconfigure(0, weight=1);
mainframe.rowconfigure(0, weight=1);

source = StringVar();
w = Spinbox(mainframe, from_=1, to=100);
w.grid(column=3, row=1, sticky=(W, E));

source_entry = ttk.Entry(mainframe, width=50, textvariable=source);
source_entry.grid(column=2, row=1, sticky=(W, E));

output = Listbox(mainframe);
output.grid(column=2, row=2, sticky=(W, E));
ttk.Button(mainframe, text="Generar", command=generarParafrasis).grid(column=3, row=2, sticky=W);

ttk.Label(mainframe, text="Oracion:").grid(column=1, row=1, sticky=W);
ttk.Label(mainframe, text="Parafrasis:").grid(column=1, row=2, sticky=E);

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5);

source_entry.focus();
root.bind('<Return>', generarParafrasis);

root.mainloop();

