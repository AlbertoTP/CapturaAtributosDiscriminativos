# -*- coding: utf-8 -*-
"""
@author: AlbertoTP
"""

import time
import sys
import re

#import spacy
#nlp = spacy.load('en')
#nlp = spacy.load('en_vectors_web_lg')
from textblob import Word

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
#Stopwords in English
from nltk.corpus import stopwords as sw
en_sw = set(sw.words('english'))
from nltk.corpus import wordnet_ic

import sense2vec
s2v = sense2vec.load('/usr/local/lib/python3.5/dist-packages/sense2vec/reddit_vectors-1.1.0/')

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
                if ((line[0],line[2]) in diccPos):#python3
                    diccPos[line[0],line[2]].append(line[1])
                else:
                    diccPos[line[0],line[2]]=[line[1]]
                if ((line[1],line[2]) in diccNeg):#python3
                    diccNeg[line[1],line[2]].append(line[0])
                else:
                    diccNeg[line[1],line[2]]=[line[0]]
            else:  #agrega a negativos
                lineNeg+=1
                if not((line[0],line[2]) in diccPos):#python3
                    if ((line[0],line[2]) in diccNeg):#python3
                        diccNeg[line[0],line[2]].append(line[1])
                    else:
                        diccNeg[line[0],line[2]]=[line[1]]
                else:
                    if not((line[1],line[2]) in diccPos):#python3
                        diccPos[line[1],line[2]]=[line[0]]
        
        #Delete duplicate keys in dictionay negative
        #cont=0
        for key in diccPos:
            if (key in diccNeg):#python3
                #print (">",key,diccNeg[key])
                del diccNeg[key]
                #cont+=1
        #print ("Se descartaron ",cont," palabras")
        file.close()
    print ("lineas Pos: ",linePos,"\nlineas Neg: ",lineNeg,"\n")
    return diccPos,diccNeg

def words_to_dictionary(search,words):
    """
    delete special characters, numbers and stopwords. lemmatize the word and insert in a dictionary
    Input: words (Vector String)
    Return: dic (dictionary)
    """
    dic={}
    for word in words:
        #word=str(word.encode('ascii', 'ignore')).lower()
        word=str(word.lower())
        word=re.sub(r'[0-9]', '', word)
        word=re.sub('\W+','', word )
        if word not in en_sw:
            wordnet_lemmatizer = WordNetLemmatizer()
            word=wordnet_lemmatizer.lemmatize(word)
            if not( word in dic ): #python3
                dic[(search,word)]=["R"]
    return dic

def search_word_sense2vec(search):
    """
    Search a word with sense2vec to return the most similar words of the search
    Input: search (string)
    Return: dic (dictionary)
    """
    wsearch=search+"|NOUN"    
    wordsV=[]
    dic={}
    try:
        freq, vector = s2v[wsearch]
        words, scores = s2v.most_similar(vector, n=300)
        for word, score in zip(words, scores):
            if (score > 0.5):
                temp=word[0:-5]
                wordsV.append(temp)
        dic=words_to_dictionary(search,wordsV)
        return dic
    except:
        return dic

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
    ruta="resultados-s2v.txt"
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
        w1aPos=((line[0],line[2]) in dicPos) #python3
        w2aPos=((line[1],line[2]) in dicPos)
        w1aNeg=((line[0],line[2]) in dicNeg)
        w2aNeg=((line[1],line[2]) in dicNeg)
        
        #Find the meaning of the word in a dictionary
        if not(w1aPos):
            dicPos.update(search_word_sense2vec(line[0]))
            w1a=((line[0],line[2]) in dicPos)
        else:
            w1a=True
        if not(w2aPos):
            dicPos.update(search_word_sense2vec(line[1]))
            w2a=((line[1],line[2]) in dicPos)
        else:
            w2a=True
        if w1aNeg or (w1aPos and w2aPos): #dictionary negative
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
