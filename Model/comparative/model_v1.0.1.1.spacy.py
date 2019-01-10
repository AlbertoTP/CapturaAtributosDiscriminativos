# -*- coding: utf-8 -*-
"""
@author: AlbertoTP
"""

import time
import sys

import spacy
#nlp = spacy.load('en')
nlp = spacy.load('en_vectors_web_lg')
from textblob import Word

from nltk.stem import WordNetLemmatizer
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


def similaritySpyCy(word1,word2):        
    """
    Similarity between two words with Spicy
    Input: word1, word2 (String)
    Return: similarity (float)
    """    
    tokens = nlp( (word1+" "+word2))
    #print tokens
    #print "Similarity Spacy:",tokens[0].similarity(tokens[1])
    try:
        if tokens[0].similarity(tokens[1])>0.5:
            return True
    except:
        return False
    return False
    
    

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
    ruta="resultados-spacy.txt"
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
            w1a=similaritySpyCy(line[0],line[2])
        else:
            w1a=True
        
        if not(w2aPos):
            w2a=similaritySpyCy(line[1],line[2])
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
