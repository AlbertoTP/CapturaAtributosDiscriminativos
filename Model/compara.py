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
    Input: rutas path of the file to be read
    Return: 2 dictionaries diccPos and diccNeg
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
    for linea0,linea1 in izip(file1.readlines(),file2.readlines()):
        line0=linea0.split(",")
        line1=linea1.split(",")
        if line0[3]=="1\n":
            print "0 >",line0
            print "1 >",line1
        if line0[3]==line1[3]:
            linesPos+=1
        else:
            linesNeg+=1
    print "Lineas Positivas ",linesPos
    print "Lineas Negativas ",linesNeg
    print "Total de lineas: ",linesPos+linesNeg
    print " % bueno = ",linesPos/(linesPos+linesNeg*1.0)
    file1.close()
    file2.close()

def main():
    starting_point = time.time()
    readFile("dataTrain/validation.txt","resultadosTest.txt")
    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()