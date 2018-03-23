# -*- coding: utf-8 -*-
"""
@author: Alberto
"""

import sys
import time

def readFile(ruta,diccPos,diccNeg):
    """
    Read file, extract information (Word 1, word 2, Feature, value) line per line, insert in dictionaries
    Input: ruta path of the file to be read
            diccPos dictionary of candidate positive examples
            diccNeg dictionary of candidate negative examples
    Return: 2 dictionaries diccPos and diccNeg
    """
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
    cont=0
    for linea in file.readlines():
        line=linea.split(",")
        #print line
        if line[3]=='1\n':          #agrega a positivos
            if diccPos.has_key((line[0],line[2])):
                diccPos[line[0],line[2]].append(line[1])
            else:
                diccPos[line[0],line[2]]=[line[1]]
                if diccNeg.has_key((line[1],line[2])):
                    diccNeg[line[1],line[2]].append(line[0])
                else:
                    diccNeg[line[1],line[2]]=[line[0]]
        else:            #agrega a negativos
            if not(diccPos.has_key((line[0],line[2]))):
                if diccNeg.has_key((line[0],line[2])):
                    diccNeg[line[0],line[2]].append(line[1])
                else:
                    diccNeg[line[0],line[2]]=[line[1]]
            else:
                cont+=1
    print "descarto ",cont,"palabras duplicadas en diccionario"
    file.close()
    return diccPos,diccNeg
    
def main():
    starting_point = time.time()
    dicPos={}
    dicNeg={}
    #dicPos,dicNeg=readFile("dataTrain/train.txt",dicPos,dicNeg) #diccionarios del train
    dicPos,dicNeg=readFile("dataTrain/validation.txt",dicPos,dicNeg)
    #for key in dicPos: #imprime todo el diccionario
        #for 3 key 2 values
        #print "Word1: "+key[0]+"\tWord2: "+key[1]+"\tAtrib: "+key[2]+"\nW1|A: "+dicPos[key][0]+"|"+dicPos[key][1]
        #for 2 key 1 value
        #print "Word1: "+key[0]+"\tWord2: "+dicPos[key][0]+"\tAtrib: "+key[1]+"\nA: "+str(dicPos[key])
    print "elementos dicPos ",len(dicPos)
    print "elementos dicNeg ",len(dicNeg)
    
    print dicPos.has_key(('elbow', 'arm'))
    print dicNeg.has_key(('elbow', 'arm'))
    
    print dicPos.has_key(('barn', 'large'))
    print dicNeg.has_key(('barn', 'large'))
    #print dicPos.keys() #llaves
    #print dicPos.values() #valor de llaves
    #print dicPos.get(('rabbit', 'hops'))
    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()