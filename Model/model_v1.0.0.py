# -*- coding: utf-8 -*-
"""
@author: alternatif
"""

import time
import sys
import re
import requests
import spacy

nlp = spacy.load('en')
from textblob import Word
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw

from bs4 import BeautifulSoup
#Stopwords in English
en_sw = set(sw.words('english'))
#print en_sw



def readFile(ruta,diccPos,diccNeg):
    """
    Read file, extract information (Word 1, word 2, Feature, value) line per line, insert in dictionaries
    Input: ruta path of the file to be read (String)
            diccPos dictionary of candidate positive examples (dictionary)
            diccNeg dictionary of candidate negative examples (dictionary)
    Return: 2 dictionaries diccPos and diccNeg (dictionary)
    """
    print "\n>>> Archivo(train): ",ruta," extrayendo datos ..."
    for i in range (0,2):
        #print ">>>",i
        try:
            file = open(ruta,"r")
        except IOError:
            print "There was an ERROR reading file"
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
            #print line
            if line[3]=='1\n':          #agrega a positivos
                linePos+=1
                if diccPos.has_key((line[0],line[2])):
                    diccPos[line[0],line[2]].append(line[1])
                else:
                    diccPos[line[0],line[2]]=[line[1]]
                if diccNeg.has_key((line[1],line[2])):
                    diccNeg[line[1],line[2]].append(line[0])
                else:
                    diccNeg[line[1],line[2]]=[line[0]]
            else:            #agrega a negativos
                lineNeg+=1
                if not(diccPos.has_key((line[0],line[2]))):
                    if diccNeg.has_key((line[0],line[2])):
                        diccNeg[line[0],line[2]].append(line[1])
                    else:
                        diccNeg[line[0],line[2]]=[line[1]]
                else:
                    if not(diccPos.has_key((line[1],line[2]))):
                        diccPos[line[1],line[2]]=[line[0]]
        
        #Delete duplicate keys in dictionay negative
        #cont=0
        for key in diccPos:
            #print "key ",key,type(key)
            if diccNeg.has_key(key):
                del diccNeg[key]
                #print "delete ",key
                #cont+=1
        #print "Se descartaron ",cont," palabras"

        #print "Elementos dicPos ",len(diccPos),"\nelementos dicNeg ",len(diccNeg),"\n"
        file.close()
    print "lineas Pos: ",linePos,"\nlineas Neg: ",lineNeg,"\n"
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
                if not(syn_set.has_key(item)):
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
                        if not(synonyms.has_key(j)):
                            synonyms[j]=3
                elif not(synonyms.has_key(i)):
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
    #print palabras[0]," \tType: ",type(palabras[0])
    if len(palabras)==0:
        return synonyms
        
    temp=str(palabras[0])
    temp=temp[8:-2]
    #print ">",temp
    palabras = wn.synset(str(temp))
    
    #hypernyms
    lista=palabras.hypernyms()
    temp=allSynLemma(lista)
    if len(temp)!=0:
        synonyms.update(temp)
    
    #hyponyms
    lista=palabras.hyponyms()
    temp=allSynLemma(lista)
    if len(temp)!=0:
        synonyms.update(temp)
    
    #member_holonyms
    lista=palabras.member_holonyms()
    temp=allSynLemma(lista)
    if len(temp)!=0:
        synonyms.update(temp)
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
            #print palabra
            if palabra not in en_sw:
                #Meaning of a word
                palabra=Word(str(palabra).lower() )
                palabra=palabra.lemmatize()
                #print ">> ",palabra
                #Insert in the dictionary
                if not(dic.has_key(palabra)):
                    dic[palabra]=1
    #print dic
    return dic
    
def compareWorAtr(word,atri):
    """
    It extracts all the characteristics (Atributes) of a word according to the meaning of the WordNet dictionary
    remove stopwords and add synonyms (update dictionary with other dictionary)
    Input: word, atribut (string)
    return: (boolean)
    """    
    definitions=list(Word(word).definitions)
    #print definitions
    lista=[]
    dic={}
    syn={}
    #lemma={}
    for definition in definitions:
        #print "> ",definition
        lista=definition.split(' ')
        for palabra in lista:
            #print palabra
            if palabra not in en_sw:
                
                #Meaning of a word (0)
                palabra=Word(str(palabra).lower() )
                palabra=palabra.lemmatize()
                #print ">> ",palabra,type(palabra)
                #Insert in the dictionary
                if not(dic.has_key(palabra)):
                    dic[palabra]=0
                
                #Meaning of a word of the word (1)
                dicDef=wordDefinition(str(palabra))
                dic.update(dicDef)
                
                #Lemma of the word of the word (2)
                lemma=lemmalist(palabra)
                #print lemma
                dic.update(lemma)
                
                #Synonyms of the word of the word (3)
                #syn=synonym(str(palabra))
                #print syn
                #dic.update(syn)
                
    #Synonyms of the main word (3)
    syn=synonym(str(word).lower())
    #Update main dictionary
    dic.update(syn)
    #print "len:",len(dic),"\nDicc:",dic
    return dic.has_key(atri)

def words_to_dictionary(search,words):
    """
    delete special characters, numbers and stopwords. lemmatize the word and insert in a dictionary
    Input: words (Vector String)
    Return: dic (dictionary)
    """
    dic={}
    for word in words:
        #print (word)
        word=str(word.encode('ascii', 'ignore')).lower()
        word=re.sub(r'[0-9]', '', word)
        word=re.sub('\W+','', word )
        if word not in en_sw:
            #print (word)
            wordnet_lemmatizer = WordNetLemmatizer()
            word=wordnet_lemmatizer.lemmatize(word)
            if not( dic.has_key(word) ): #python2
            #if not( word in dic ): #python3
                dic[(search,word)]=["R"]
    return dic


def search_word_dictionary(search):
    """
    Search a word in dictionary.com
    Input: search (string)
    Return: dic (dictionary)
    """
    #print search
    dic={}
    r=requests.get("http://www.dictionary.com/browse/"+search)
    
    soup=BeautifulSoup(r.text, "html.parser")
    results=soup.find("div",{"class":"source-data"})
    #print results
    if results != None:
        all_info=results.findAll("section",{"class":"def-pbk ce-spot"})
        #print (all_info)
        
        for item in all_info:
            line=item.findAll("div",{"class":"def-content"})
            for element in line:
                cad=element.get_text()
                #print (cad)
                words=cad.split(' ')
                if len(words)>0:
                    dic.update(words_to_dictionary(search,words))
    return dic
            
    
def search_word_wiki(search):
    """
    Search a word in en.wikipedia.org
    Input: search (string)
    Return: dic (dictionary)
    """
    dic={}
    r=requests.get("https://en.wikipedia.org/wiki/"+search)
    
    soup=BeautifulSoup(r.text, "html.parser")
    results=soup.find("div",{"class":"mw-parser-output"})
    all_info=results.findAll("p")
    #print (all_info)
    #print (len(all_info))
    if len(all_info)<2:
        return dic
    
    i=0
    for item in all_info:
        if (i<3):
            #print (item.get_text())
            #print (type(line))
            line=item.get_text()
            words=line.split(' ')
            #print (words)
            if len(words)>0:
                dic.update(words_to_dictionary(search,words))
        i+=1
    return dic
    
def compare_word_feature(word,atri):
    """
    It extracts all the characteristics (Atributes) of a word according to the meaning of the WordNet dictionary
    Input: word, atribut (string)
    return: true or false (boolean)
    retunr: dictionary with word,atrib (dictionary)
    """
    features={}
    features=search_word_dictionary(word)
    features.update(search_word_wiki(word))
    
    #print "len:",len(features),"\nDicc:",features
    return features.has_key((word,atri)),features

    
    

def main():
    starting_point = time.time()
    dicPos={}
    dicNeg={}
    dicWeb={}
    dicPos,dicNeg=readFile("dataTrain/train.txt",dicPos,dicNeg) #diccionarios del train
#    dicPos1,dicNeg1=readFile("dataTrain/validation.txt",dicPos,dicNeg)
#    dicPos.update(dicPos1)
#    dicNeg.update(dicNeg1)
    print "Diccionarios Train"
    print "elementos dicPos ",len(dicPos)
    print "elementos dicNeg ",len(dicNeg)
    print "Espere ..."
    
    path="dataTrain/validation.txt"
    #path="dataTest/test_triples.txt" #original file
    ruta="resultadosTest.txt"
    try:
        file = open(path,"r")
        result=open(ruta,"w")
    except IOError:
        print "There was an ERROR reading file"
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
    print "\n>>> Archivo(test): ",path
    print "Numero de lineas",len(archivo)
    
    print "\nClasificando (esto puede tomar tiempo) ...\n"
        
    for line in archivo:
        w1aPos=dicPos.has_key((line[0],line[2]))
        w2aPos=dicPos.has_key((line[1],line[2]))
        w1aNeg=dicNeg.has_key((line[0],line[2]))
        w2aNeg=dicNeg.has_key((line[1],line[2]))
        
        #Find the meaning of the word in a dictionary
        w1a=compareWorAtr(line[0],line[2])
        if not(w1a) and not(dicWeb.has_key(line[0])):
            w1a,features=compare_word_feature(line[0],line[2])
            dicPos.update(features)
            dicWeb[line[0]]=1
        
        w2a=compareWorAtr(line[1],line[2])
        if not(w2a) and not(dicWeb.has_key(line[1])):
            w2a,features=compare_word_feature(line[1],line[2])
            dicPos.update(features)
            dicWeb[line[1]]=1
    
        if w1aNeg or (w1aPos and w2aPos): #dictionary negative
            #dicNeg[line[0],line[2]].append(line[1])
            result.write(str(line[0])+","+str(line[1])+","+str(line[2])+",0\n");
        elif ((w1aPos and w2aNeg) or (w1aPos and not(w2a)) or (w1a and w2aNeg) or (w1a and not(w2a)) ):
            #dictionary positive
            if w1aPos: #inserta w1 en dicPos
                dicPos[line[0],line[2]].append(line[1])
            else:
                dicPos[line[0],line[2]]=[line[1]]
            if w2aNeg: ##inserta w2 en dicNeg
                dicNeg[line[1],line[2]].append(line[0])
            else:
                dicNeg[line[1],line[2]]=[line[0]]
            result.write(str(line[0])+","+str(line[1])+","+str(line[2])+",1\n");
        else: #dictionary negative
            #dicNeg[line[0],line[2]]=[line[1]]
            result.write(str(line[0])+","+str(line[1])+","+str(line[2])+",0\n");

    result.close()
                
    print "\nDiccionarios Train y Test despues de clasificar"
    print "elementos dicPos ",len(dicPos)
    print "elementos dicNeg ",len(dicNeg)

    #print dicPos.keys()
    print "\nPuede revisar el archivo de resultados en: ",ruta
    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()