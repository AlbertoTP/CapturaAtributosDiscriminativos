# -*- coding: utf-8 -*-
"""
@author: Alberto
"""

import sys
import time
from itertools import izip

def readFile(ruta1,ruta2):
    """
    Read files, extract information (Word 1, word 2, Feature, value) line per line, compares the information
    Input: rutas path of the file to be read (String)
    Return: 2 dictionaries diccPos and diccNeg (dictionary)
    """
    try:
        file1 = open(ruta1,"r")
        file2 = open(ruta2,"r")
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
    linesPos,linesNeg=0,0
    linesEP,linesEN=0,0
    cont=0
    #temp=""
    for linea0,linea1 in izip(file1.readlines(),file2.readlines()):
        line0=linea0.split(",")
        line1=linea1.split(",")
        
        if line0[3]==line1[3]=="1\n":
            linesPos+=1
        elif line0[3]==line1[3]=="0\n":
            linesNeg+=1
        elif line0[3]=="0\n" and line1[3]=="1\n":
            linesEN+=1
        elif line0[3]=="1\n" and line1[3]=="0\n":
            linesEP+=1
        
        if line0[3]!=line1[3]:
            cont+=1
            print cont,"\t0 >",line0
            #temp+=linea0
            print "\t1 >",line1
    #print temp

    print "\nLineas Positivas ",linesPos
    print "Lineas Negativas ",linesNeg
    print "Lineas Acertadas ",linesPos+linesNeg
    print "Total de lineas: ",linesPos+linesNeg+linesEP+linesEN
    print "% Total Acertado ", ((linesPos+linesNeg)/(linesPos+linesNeg+linesEP+linesEN*1.0))*100
    
    print "\nLineas Erroneas Pos (1,0) ",linesEP
    print "Lineas Erroneas Neg (0,1) ",linesEN
    print "lineas Erroneas total ",linesEP+linesEN
    print "Lineas total Pos: ",linesPos+linesEP
    print "lineas total Neg: ",linesNeg+linesEN
    print "% Lineas Pos = ",linesPos/(linesPos+linesEP*1.0)*100
    print "% Lineas Neg = ",linesNeg/(linesNeg+linesEN*1.0)*100
    
    file1.close()
    file2.close()

def main():
    starting_point = time.time()
    #readFile("dataTrain/validation.txt","resultadosValidation.txt")
    readFile("dataTrain/validation.txt","resultados-M1.2.0.txt")
    #readFile("dataTrain/validation.txt","resultadosTest.txt")
    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()