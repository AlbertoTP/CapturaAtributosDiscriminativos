# -*- coding: utf-8 -*-
"""
@author: alternatif
"""

import extractTrain
import time
import sys

def meaningWord():
    pass

def isNegPos():
    pass

def main():
    starting_point = time.time()
    dicPos={}
    dicNeg={}
    listWordsPos=[]
    dicPos,dicNeg=extractTrain.readFile("dataTrain/train.txt",dicPos,dicNeg) #diccionarios del train
    dicPos,dicNeg=extractTrain.readFile("dataTrain/validation.txt",dicPos,dicNeg)
    print "elementos dicPos ",len(dicPos)
    print "elementos dicNeg ",len(dicNeg)
    
    listWordsPos=dictoList(dicPos,listWordsPos)
    
    ruta="dataTest/test_triples.txt"
    try:
        file = open(ruta,"r")
    except IOError:
        print "There was an ERROR reading file"
        sys.exit()
    
    for linea in file.readlines():
        line=linea.rstrip('\n').split(",")
        line=tuple(line)
        #print type(line)
        #print line
        
        w1aPos=dicPos.has_key(line[0],line[2])
        w2aPos=dicPos.has_key(line[1],line[2])
        w1aNeg=dicNeg.has_key(line[0],line[2])
        w2aNeg=dicNeg.has_key(line[1],line[2])
        w1a=isNegPos(line[0],line[2])
        w2a=isNegPos(line[1],line[2])
        
        if w1aNeg:
            continue
        elif ((w1aPos and w2aNeg) or (w1a and not(w2a)) ):
            if not(w1aPos):
                insertDicPos(line)
        else:
            if not(w1aNeg):
                insertDicNeg(line)
        

    #print dicPos.keys()
    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()
