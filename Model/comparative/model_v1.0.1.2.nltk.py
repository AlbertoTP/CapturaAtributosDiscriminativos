# -*- coding: utf-8 -*-
"""
@author: AlbertoTP
"""

import time
import sys

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

def similarityWordNet(word1,word2):
    """
    Similarity between two words with nltk
    Input: word1, word2 (String)
    Return: similarity (float)
    """
    #print (word1,"-",word2)
    word1=str(wn.morphy(word1))
    word2=str(wn.morphy(word2))
    
    palabras=wn.synsets(word1)
    #print (palabras)
    if len(palabras)==0:
        print ("no existe")
        return False
    temp=str(palabras[0])
    temp=temp[8:-2]
    #print (">",temp)
    word1=wn.synset(str(temp))
    #print (word1)
    
    palabras=wn.synsets(word2)
    #print (palabras)
    if len(palabras)==0:
        print ("no existe")
        return False
    temp=str(palabras[0])
    temp=temp[8:-2]
    #print (">",temp)
    word2=wn.synset(str(temp))
    #print (word2)
    
    #value1=path_sim(word1,word2)
    #value1=lch_sim(word1,word2)
    #value1=wup_sim(word1,word2)
    value1=res_sim(word1,word2)
    
    if value1 > 0.5:
        return True
    return False
    
    
    
def path_sim(word1,word2):
    """
    Return a score denoting how similar two word senses are,
    based on the shortest path that connects the senses in the is-a
    (hypernym/hypnoym) taxonomy. The score is in the range 0 to 1.
    
    By default, there is now a fake root node added to verbs so
    for cases where previously a path could not be found---and None
    was returned---it should return a value. The old behavior can be
    achieved by setting simulate_root to be False. A score of 1 represents
    identity i.e. comparing a sense with itself will return 1.
    """
    try:
        #return wn.path_similarity(word1, word2)
        try:
           value = float(wn.path_similarity(word1, word2))
           return value
        except ValueError:
           return 0
    except:
        return 0
    
def lch_sim(word1,word2):
    """
    Leacock-Chodorow Similarity: Return a score denoting how similar
    two word senses are, based on the shortest path that connects
    the senses (as above) and the maximum depth of the taxonomy in
    which the senses occur. range 3.6
    
    The relationship is given as -log(p/2d) where p is the
    shortest path length and d the taxonomy depth.
    """
    try:
        try:
            value = wn.lch_similarity(word1, word2)
            value = value / 3.6 #value in range of 0 to 1
            return value
        except ValueError:
           return 0
    except:
        return 0
    
def wup_sim(word1,word2):
    
    
    """
    Wu-Palmer Similarity: Return a score denoting how similar
    two word senses are, based on the depth of the two senses in
    the taxonomy and that of their Least Common Subsumer (most specific ancestor node).
    range 0.92
    
    Note that at this time the scores given do _not_ always agree with those given by Pedersen's
    Perl implementation of Wordnet Similarity.
    The LCS does not necessarily feature in the shortest path connecting the two senses,
    as it is by definition the common ancestor deepest in the taxonomy, not closest to
    the two senses. Typically, however, it will so feature. Where multiple candidates for
    the LCS exist, that whose shortest path to the root node is the longest will be selected.
    Where the LCS has multiple paths to the root, the longer path is used for the purposes
    of the calculation.
    """
    try:
        #print (wn.path_similarity(word1, word2))
        #if (wn.path_similarity(word1, word2) > 0.5): #(hypernym/hypnoym) taxonomy
        value=wn.wup_similarity(word1, word2)
        if value.isnumeric():
           return value
        return 0
    except:
        return 0

brown_ic = wordnet_ic.ic('ic-brown.dat')
def res_sim(word1,word2):
    """
    Resnik Similarity: Return a score denoting how similar two word senses are, based on the
    Information Content (IC) of the Least Common Subsumer (most specific ancestor node).
    Note that for any similarity measure that uses information content, the result is dependent on
    the corpus used to generate the information content and the specifics of how the information
    content was created. 0-8.43
    """
    try:
        try:
            value=word1.res_similarity(word2, brown_ic)
            value=value/8.4
            return value
        except ValueError:
           return 0
    except:
        return 0
    

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
    #ruta="resultados-nltk-path.txt"
    #ruta="resultados-nltk-lch.txt"
    #ruta="resultados-nltk-wup.txt"
    ruta="resultados-nltk-res.txt"
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
            #w1a=similaritySpyCy(line[0],line[2])
            w1a=similarityWordNet(line[0],line[2])
        else:
            w1a=True
        
        if not(w2aPos):
            #w2a=similaritySpyCy(line[1],line[2])
            w2a=similarityWordNet(line[1],line[2])
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
