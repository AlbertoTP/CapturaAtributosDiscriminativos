# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 13:28:00 2018

@author: alternatif
"""

""" Lee archivo, extrae info y ordena en diccionario """
def readFile(ruta):
    diccPos={} #diccionario para ejemplos candidatos positivos
    diccNeg={} #diccionario para ejemplos candidatos negativos
    file = open(ruta,"r")
    #lin,pos,neg=0,0,0
    """
    Data format: 4 comma-separated fields:
    - word 1 (pivot)
    - word 2 (comparison)
    - feature
    - label ("1" if the feature characterizes word 1 compared to word 2, "0" otherwise)
    Example:
    word1,word2,feature,label(0/1)
    """
    for linea in file.readlines():
        line=linea.split(",")        
        #lin+=1
        #print line
        if line[3]=='1\n':
            #agrega a positivos
            diccPos[line[0],line[1],line[2]]=[line[0],line[2]]
            #pos+=1
        else:
            #agrega a negativos
            diccNeg[line[0],line[1],line[2]]=[line[0],line[2]]
            #neg+=1
    #print "lin ",lin
    #print "pos ",pos
    #print "neg ",neg
    return diccPos,diccNeg
    
    
def main():
    diccPos={}
    diccNeg={}
    diccPos,diccNeg=readFile("dataTrain/train.txt")
    for key in diccPos: #imprime todo el diccionario
        print "Word1: "+key[0]+"\tWord2: "+key[1]+"\tAtrib: "+key[2]+"\nW1|A: "+diccPos[key][0]+"|"+diccPos[key][1]
    print "elementos diccPos ",len(diccPos)
    print "elementos diccNeg ",len(diccNeg)
#    if diccPos.has_key(('comb', 'scissors', 'thin')): #key
#        print "existe"
#    else:
#        print "No existe"
#    if diccPos.get(('comb', 'scissors', 'thin')): #clave
#        print "existe"
#    else:
#        print "No existe"
    #print diccPos.keys()
    
if __name__ == "__main__":
    main()