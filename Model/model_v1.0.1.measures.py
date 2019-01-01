# -*- coding: utf-8 -*-
"""
@author: AlbertoTP
"""

import time
import sys

import spacy
#nlp = spacy.load('en')
nlp = spacy.load('en_vectors_web_lg')
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

from textblob import Word

from nltk.corpus import wordnet as wn
#Stopwords in English
from nltk.corpus import stopwords as sw
en_sw = set(sw.words('english'))


def readFile(ruta,diccPos,diccNeg):
    """
    Read file, extract information (Word 1, word 2, Feature, value) line per line, insert in dictionaries
    Input: ruta path of the file to be read (String)
            diccPos dictionary of candidate positive examples (dictionary)
            diccNeg dictionary of candidate negative examples (dictionary)
    Return: 2 dictionaries diccPos and diccNeg (dictionary)
    """
    print ("\n>>> Archivo(train): ",ruta," extrayendo datos ...")
    #two times, one for fill dictionaries and other for delete duplicate key
    for i in range (0,2):
        try:
            file = open(ruta,"r")
        except IOError:
            print ("There was an ERROR reading file")
            sys.exit()
        """
        Data format: 4 comma-separated fields:
        - word 1 (pivot)
        - word 2 (comparison)
        - feature
        - label ("1" if the feature characterizes word 1 compared to word 2, "0" otherwise)
        Example:    word1,word2,feature,label(0/1)
        """
        linePos,lineNeg=0,0
        for linea in file.readlines():
            line=linea.split(",")
            if line[3]=='1\n': #agrega a positivos
                linePos+=1
                #if diccPos.has_key((line[0],line[2])):
                if ((line[0],line[2]) in diccPos):#python3
                    diccPos[line[0],line[2]].append(line[1])
                else:
                    diccPos[line[0],line[2]]=[line[1]]
                #if diccNeg.has_key((line[1],line[2])):
                if ((line[1],line[2]) in diccNeg):#python3
                    diccNeg[line[1],line[2]].append(line[0])
                else:
                    diccNeg[line[1],line[2]]=[line[0]]
            else:  #agrega a negativos
                lineNeg+=1
                #if not(diccPos.has_key((line[0],line[2]))):
                if not((line[0],line[2]) in diccPos):#python3
                    #if diccNeg.has_key((line[0],line[2])):
                    if ((line[0],line[2]) in diccNeg):#python3
                        diccNeg[line[0],line[2]].append(line[1])
                    else:
                        diccNeg[line[0],line[2]]=[line[1]]
                else:
                    #if not(diccPos.has_key((line[1],line[2]))):
                    if not((line[1],line[2]) in diccPos):#python3
                        diccPos[line[1],line[2]]=[line[0]]

        #Delete duplicate keys in dictionay negative
        #cont=0
        for key in diccPos:
            #if diccNeg.has_key(key):
            if (key in diccNeg):#python3
                del diccNeg[key]
                #cont+=1
        #print "Se descartaron ",cont," palabras"
        file.close()
    print ("lineas Pos: ",linePos,"\nlineas Neg: ",lineNeg,"\n")
    return diccPos,diccNeg

def lemmalist(word):
    """
    Lemmatisation is the process of grouping together the inflected forms of a word so they can be analysed as a single item, identified by the word's lemma, or dictionary form
    Input: word (string)
    Return: lemma (dictionary)
    """
    syn_set = {}
    #print "lemmasWord",word
    cont=0
    for synset in wn.synsets(word):
        if cont<1:
            for item in synset.lemma_names():
                if not(item in syn_set):
                    syn_set[item]=2;
            cont+=1
        else:
            break
    #print syn_set
    return syn_set



def allSynLemma(lista):
    """
    Separates a list and insert each word in a dictionary, also it separtes compoun word (word_1 = word,1)
    Input: lista (list)
    Return: synonims (dictionary)
    """
    synonyms={}
    if len(lista)!=0:
        for element in lista:
            #print ">>> ", element.lemma_names()
            for i in element.lemma_names():
                #print i
                vec=i.split("_")
                if len(vec)>1:
                    for j in vec:
                        #if not(synonyms.has_key(j)):
                        if not(j in synonyms):#python3
                            synonyms[j]=3
                #elif not(synonyms.has_key(i)):
                elif not(i in synonyms):#python3
                    synonyms[i]=3;
    return synonyms

def synonym(word):
    """
    first synonyms, hypernyms, hyponyms and member_holonyms of the one word
    Input: word (String)
    Return: synonims (dictionary)
    """
    synonyms={}
    #print ">>>def synonym:", str(wn.morphy(word))
    palabras=wn.synsets(str(wn.morphy(word)))
    #print palabras
    if len(palabras)==0:
        return synonyms

    temp=str(palabras[0])
    temp=temp[8:-2]
    #print ">",temp
    palabras = wn.synset(str(temp))

    #hypernyms
#    lista=palabras.hypernyms()
#    temp=allSynLemma(lista)
#    if len(temp)!=0:
#        synonyms.update(temp)

    #hyponyms
#    lista=palabras.hyponyms()
#    temp=allSynLemma(lista)
#    if len(temp)!=0:
#        synonyms.update(temp)

    #member_holonyms
#    lista=palabras.member_holonyms()
#    temp=allSynLemma(lista)
#    if len(temp)!=0:
#        synonyms.update(temp)
    return synonyms



def wordDefinition(word):
    """
    The meaning of a word according to wordnet, remove stopwords
    Input: word (String)
    Return: (dictionary)
    """
    dic={}
    definitions=list(Word(word).definitions)
    #print definitions
    if len(definitions)!=0:
        lista=[]
        dic={}
        lista=definitions[0].split(' ')
        for palabra in lista:
            if palabra not in en_sw:
                #Meaning of a word
                palabra=lemmatize_word(palabra)
                #Insert in the dictionary
                if not(palabra in dic):
                    dic[palabra]=1
    return dic

def lemmatize_word(word):
    """
    Assign the base form of words
    Input: word (plural, capital letters)
    return: word (singular, lower letters)
    """
    palabra=word
    palabra=Word(str(palabra).lower() )
    palabra=palabra.lemmatize()
    if palabra==word:
        lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
        palabra = lemmatizer(word, u'NOUN')
        palabra=palabra[0]
    return palabra

def compareWorAtr(word,atri):
    """
    It extracts all the characteristics (Atributes) of a word according to the meaning of the WordNet dictionary
    remove stopwords and add synonyms (update dictionary with other dictionary)
    Input: word, atribut (string)
    return: (boolean)
    """
    definitions=list(Word(word).definitions)
    lista=[]
    dic={}
    syn={}
    #lemma={}
    for definition in definitions:
        lista=definition.split(' ')
        for palabra in lista:
            if palabra not in en_sw:

                #Meaning of a word (0)
                #palabra=lemmatize_word(palabra)
                #Insert in the dictionary
                if not(palabra in dic):
                    dic[palabra]=0

                #Meaning of a word of the word (1)
#                dicDef=wordDefinition(str(palabra))
#                dic.update(dicDef)

                #Lemma of the word of the word (2)
#                lemma=lemmalist(palabra)
                #print lemma
#                dic.update(lemma)

    #Synonyms of the main word (3)
    syn=synonym(str(word).lower())
    #Update main dictionary
    dic.update(syn)
    #print "len:",len(dic),"\nDicc:",dic
    return (atri in dic)


def main():
    starting_point = time.time()
    dicPos={}
    dicNeg={}
    dicPos,dicNeg=readFile("dataTrain/train.txt",dicPos,dicNeg) #diccionarios del train
    #dicPos1,dicNeg1=readFile("dataTrain/validation.txt",dicPos,dicNeg)
    #dicPos.update(dicPos1)
    #dicNeg.update(dicNeg1)
    print ("Diccionarios Train")
    print ("elementos dicPos ",len(dicPos))
    print ("elementos dicNeg ",len(dicNeg))
    print ("Espere ...")

    path="dataTrain/validation.txt"
    #path="dataTest/test_triples.txt" #original file
    ruta="resultados-m-syn.txt"
    try:
        file = open(path,"r")
        result=open(ruta,"w")
    except IOError:
        print ("There was an ERROR reading file")
        sys.exit()

    archivo=[]
    for linea in file.readlines():
        line=linea.rstrip('\n').split(",")
        #line=tuple(line)
        #print type(line)
        #print line #('word1', 'word2', 'atrib')
        #print line[0]," ",line[2]
        archivo.append(line)
    file.close()
    print ("\n>>> Archivo(test): ",path)
    print ("Numero de lineas",len(archivo))

    print ("\nClasificando (esto puede tomar tiempo) ...\n")

    for line in archivo:
        line[0]=lemmatize_word(line[0])
        line[1]=lemmatize_word(line[1])
        line[2]=lemmatize_word(line[2])
        w1aPos=((line[0],line[2]) in dicPos)
        w2aPos=((line[1],line[2]) in dicPos)
        w1aNeg=((line[0],line[2]) in dicNeg)
        w2aNeg=((line[1],line[2]) in dicNeg)

        #Find the meaning of the word in a dictionary
        if not(w1aPos):
            w1a=compareWorAtr(line[0],line[2])
        else:
            w1a=True

        if not(w2aPos):
            w2a=compareWorAtr(line[1],line[2])
        else:
            w2a=True

        if w1aNeg or (w1aPos and w2aPos): #dictionary negative
            #dicNeg[line[0],line[2]].append(line[1])
            result.write(str(line[0])+","+str(line[1])+","+str(line[2])+",0\n");
        elif ((w1aPos and w2aNeg) or (w1aPos and not(w2a)) or (w1a and w2aNeg) or (w1a and not(w2a)) ):
            #dictionary positive
            if not(w1aPos): #inserta w1 en dicPos
                dicPos[line[0],line[2]]=[line[1]]
            if not(w2aNeg): ##inserta w2 en dicNeg
                dicNeg[line[1],line[2]]=[line[0]]
            result.write(str(line[0])+","+str(line[1])+","+str(line[2])+",1\n");
        else: #dictionary negative
            #dicNeg[line[0],line[2]]=[line[1]]
            result.write(str(line[0])+","+str(line[1])+","+str(line[2])+",0\n");

    result.close()

    print ("\nDiccionarios Train y Test despues de clasificar")
    print ("elementos dicPos ",len(dicPos))
    print ("elementos dicNeg ",len(dicNeg))

    #print dicPos.keys()
    print ("\nPuede revisar el archivo de resultados en: ",ruta)
    print ("Execution Time: ",time.time()-starting_point)

if __name__ == "__main__":
    main()
