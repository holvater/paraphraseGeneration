#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
###############################
# Rodrigo Cabrera Pena
# programa que genera parafrasis a partir de una oracion
# realiza consultas a paginas en internet para obtener sinonimos o hiponimos
# 20/08/2014
###############################

from subprocess import *
import frasesNominales
import parser.wiktionaryParser as wp
import parser.wordreferenceParser as wrp
import random


def processSentence(sentence):
    f = open("temp.txt", "w");
    f.write(sentence + "\n");
    f.close();
    (output,err) = Popen(["./freelingAnalyze.sh"], stdout=PIPE).communicate();
    orac = [];
    for word in output.decode("utf-8").split("\n"):
        elements = word.split(" ");
        if len(elements) > 1 :
            orac += [{"lemma":elements[1], "tag":elements[2], "form":elements[0]}];
    return orac;


def processWord(word):
    return processSentence(word + ".")[:-1];



def getModifications(phrase, typ="syn"):
    modifications = [];
    for orig in phrase:
        word = [orig['form']];
        if orig['tag'].find("NC") != -1 or orig['tag'].find("AQ") != -1:
            word += wrp.getSynonyms(orig['lemma']);
            word += wp.getSynonyms(orig['lemma']);            
            word += wp.getHypernyms(orig['lemma']);
            word += wp.getHiponyms(orig['lemma']);
            word = word[0:3]
        else:
            word = orig['form'];
        modifications.append(word);
    return modifications;


def searchWords(arr):
    if not isinstance(arr, str):
        res = []
        for word in arr:
            res.append(searchWords(word));
        return res;
    else:
        return processWord(arr);


def concordar(word, num, gen, origWord):
    origNum="";
    if isinstance(origWord,dict):
        if origWord['tag'].find("NC") != -1:
            origNum = origWord["tag"][3];
        elif origWord['tag'].find("DA0") != -1 or origWord['tag'].find("DI0") != -1 :
            origNum = origWord["tag"][4];

    if origNum != "" and num != "":
        baseNum = origNum;
    else:
        baseNum = num;
    if gen=="" and num !="":
        baseGen="m";
    else:
        baseGen=gen;

    if word['tag'].find(baseGen+baseNum) != -1:
        return word;
    else:
        infs = wp.getInflections(word['form'].lower());
        if isinstance(infs, dict):
            if infs[(baseGen+baseNum).lower()] != None:
                return processWord(infs[(baseGen+baseNum).lower()])[0];
    return word;

def numGen(word):
    num = word['tag'][3];
    gen = 'M' if (word['tag'][2]=='C') else word['tag'][2];
    return (num,gen);

def numGenInPhrase(phraseFragment):
    num = '';
    gen = '';
    for fragment in phraseFragment:
        if isinstance(fragment,list):
            for w in fragment:
                if w['tag'].find("NC") != -1:
                    num,gen = numGen(w);
        else:                        
            if fragment['tag'].find("NC") != -1:
                num, gen = numGen(fragment);
    return (num, gen);

def processPhrase(phrase, origPhrase):
    phraseFragments = [[]];
    for wordOrPhrase in phrase:
        if not isinstance(wordOrPhrase,list): #is word
            phraseFragments = [phraseSoFar+[wordOrPhrase] for phraseSoFar in phraseFragments];
        else:
            phraseFragments = [phraseSoFar+[word] for phraseSoFar in phraseFragments for word in wordOrPhrase];
    oraciones = [];
    for phraseFragment in phraseFragments:
        num, gen = numGenInPhrase (phraseFragment);
        oracion = [];
        for i,phraseFragment2 in enumerate(phraseFragment):
            if isinstance(origPhrase, list):
                origWord = origPhrase[i];
            else:
                origWord = origPhrase;
            if isinstance(phraseFragment2,list):
                for w in phraseFragment2:
                    oracion.append(concordar(w,num,gen, origWord));
            else:
                oracion.append(concordar(phraseFragment2,num,gen, origWord));
        oraciones.append(oracion);
    return oraciones;


def generarParafrasis(oracion, tipo="syn", limite=1):
    sentence = processSentence(oracion);
    sentence = frasesNominales.obtenerGruposNominales(sentence);
    original = sentence;

    typ=tipo;
    limit = limite;
    words = [];
    for word in sentence:
        if not isinstance(word,str):
            words.append(getModifications(word));
        else:
            words.append(word);

    results = searchWords(words);

    sentences = [[]];
    for i,wordOrPhrase in enumerate(results):
        if not isinstance(wordOrPhrase,list):
            sentences = [sentenceSoFar+[wordOrPhrase] for sentenceSoFar in sentences];
        else:
            sentences = [sentenceSoFar + phrase for sentenceSoFar in sentences for phrase in processPhrase(wordOrPhrase,original[i])];

    if len(sentences) > limit:
        output = random.sample(sentences,limit);
    else:
        output = sentences;
        random.shuffle(output);

    rets = [];
    for sentence in output:
        if sentence != [] and sentence[-1]['form'] == '.':
            sent = "";
            for i,w in enumerate(sentence):
                if i==0:
                    sent += w['form'].capitalize();
                elif w['form'] == ".":
                    sent += w['form'];
                else:
                    sent += " " + w['form'].replace("_", " ");
            rets += [sent];
    return rets;


if __name__ == '__main__':
    print(generarParafrasis("El autobús estaba lleno.", "syn", 6));
