# -*- coding: utf-8 -*-
"""
@author: Alberto
"""

import sys
import time


def compareDic(dicPos,dicNeg):
    """
    Delete duplicate keys in dictionay negative
    Input: 2 dictionaries dicPos and dicNeg (dictionary)
    Return: negative dictionary without duplicate keys (dictionary)
    """
    #cont=0
    for key in dicPos:
        #print "key ",key,type(key)
        if dicNeg.has_key(key):
            del dicNeg[key]
            #print "delete ",key
            #cont+=1
    #print "Se descartaron ",cont," palabras"
    return dicNeg


def readFile(ruta,diccPos,diccNeg):
    """
    Read file, extract information (Word 1, word 2, Feature, value) line per line, insert in dictionaries
    Input: ruta path of the file to be read (String)
            diccPos dictionary of candidate positive examples (dictionary)
            diccNeg dictionary of candidate negative examples (dictionary)
    Return: 2 dictionaries diccPos and diccNeg (dictionary)
    """
    print "\n>>> Archivo: ",ruta," extrayendo datos ..."
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
        diccNeg=compareDic(diccPos,diccNeg)
        #print "Elementos dicPos ",len(diccPos),"\nelementos dicNeg ",len(diccNeg),"\n"
        file.close()
    print "lineas Pos: ",linePos,"\nlineas Neg: ",lineNeg,"\n"
    return diccPos,diccNeg
    
    
def main():
    starting_point = time.time()
    dicPos={}
    dicNeg={}
    #dicPos,dicNeg=readFile("dataTrain/train.txt",dicPos,dicNeg) #diccionarios del train
    dicPos,dicNeg=readFile("dataTrain/validation.txt",dicPos,dicNeg)    
    #for key in dicPos: #imprime todo el diccionario
        #print "Word1: "+key[0]+"\tWord2: "+dicPos[key][0]+"\tAtrib: "+key[1]+"\nA: "+str(dicPos[key])
    print "elementos dicPos ",len(dicPos)
    print "elementos dicNeg ",len(dicNeg)
    
    #print dicPos.has_key(('elbow', 'arm'))
    #print dicNeg.has_key(('elbow', 'arm'))
    
    #print dicPos.keys() #llaves
    #print dicPos.values() #valor de llaves
    #print dicPos.get(('rabbit', 'hops'))
    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()