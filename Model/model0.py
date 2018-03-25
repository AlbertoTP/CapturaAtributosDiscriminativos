# -*- coding: utf-8 -*-
"""
@author: alternatif
"""

import extractTrain
import extractAtrib
import time
import sys



def main():
    starting_point = time.time()
    dicPos={}
    dicNeg={}
    dicPos,dicNeg=extractTrain.readFile("dataTrain/train.txt",dicPos,dicNeg) #diccionarios del train
    dicPos1,dicNeg1=extractTrain.readFile("dataTrain/validation.txt",dicPos,dicNeg)
    dicPos.update(dicPos1)
    dicNeg.update(dicNeg1)
    print "Diccionarios Train"
    print "elementos dicPos ",len(dicPos)
    print "elementos dicNeg ",len(dicNeg)
    
    #path="dataTest/test_triples.txt"
    path="dataTrain/validation.txt"
    ruta="resultadosTest.txt"
    try:
        file = open(path,"r")
        result=open(ruta,"w")
    except IOError:
        print "There was an ERROR reading file"
        sys.exit()
    
    for linea in file.readlines():
        line=linea.rstrip('\n').split(",")
        #line=tuple(line)
        #print type(line)
        #print line #('word1', 'word2', 'atrib')
        #print line[0]," ",line[2]
        
        w1aPos=dicPos.has_key((line[0],line[2]))
        w2aPos=dicPos.has_key((line[1],line[2]))
        w1aNeg=dicNeg.has_key((line[0],line[2]))
        w2aNeg=dicNeg.has_key((line[1],line[2]))
        w1a=extractAtrib.compareWorAtr(line[0],line[2])
        w2a=extractAtrib.compareWorAtr(line[1],line[2])

        if w1aNeg: #dictionary negative
            dicNeg[line[0],line[2]].append(line[1])
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
            dicNeg[line[0],line[2]]=[line[1]]
            result.write(str(line[0])+","+str(line[1])+","+str(line[2])+",0\n");
    file.close()
    result.close()
                
    print "\nDiccionarios Train y Test"
    print "elementos dicPos ",len(dicPos)
    print "elementos dicNeg ",len(dicNeg)
        

    #print dicPos.keys()
    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()
