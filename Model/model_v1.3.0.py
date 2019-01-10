# -*- coding: utf-8 -*-
"""
@author: AlbertoTP
"""

import time
import sys
import re
import requests

import spacy
#nlp = spacy.load('en')
nlp = spacy.load('en_vectors_web_lg')
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

from textblob import Word

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
#Stopwords in English
from nltk.corpus import stopwords as sw
en_sw = set(sw.words('english'))

from bs4 import BeautifulSoup

#wikipedia in english
import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('en')

#Sense2vec
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

def lemmalist(word):
    """
    Lemmatisation is the process of grouping together the inflected forms of a word so they can be analysed as a single item, identified by the word's lemma, or dictionary form
    Input: word (string)
    Return: lemma (dictionary)
    """
    syn_set = {}
    #print "lemmasWord",word
    cont=0
    for synset in wn.synsets(word):
        if cont<1:
            for item in synset.lemma_names():
                if not(item in syn_set):
                    syn_set[item]=2;
            cont+=1
        else:
            break
    #print syn_set
    return syn_set



def allSynLemma(lista):
    """
    Separates a list and insert each word in a dictionary, also it separtes compoun word (word_1 = word,1)
    Input: lista (list)
    Return: synonims (dictionary)
    """
    synonyms={}
    if len(lista)!=0:
        for element in lista:
            #print ">>> ", element.lemma_names()
            for i in element.lemma_names():
                #print i
                vec=i.split("_")
                if len(vec)>1:
                    for j in vec:
                        #if not(synonyms.has_key(j)):
                        if not(j in synonyms):#python3
                            synonyms[j]=3
                #elif not(synonyms.has_key(i)):
                elif not(i in synonyms):#python3
                    synonyms[i]=3;
    return synonyms

def synonym(word):
    """
    first synonyms, hypernyms, hyponyms and member_holonyms of the one word
    Input: word (String)
    Return: synonims (dictionary)
    """
    synonyms={}
    #print ">>>def synonym:", str(wn.morphy(word))
    palabras=wn.synsets(str(wn.morphy(word)))
    #print palabras
    if len(palabras)==0:
        return synonyms

    temp=str(palabras[0])
    temp=temp[8:-2]
    #print ">",temp
    palabras = wn.synset(str(temp))

    #hypernyms
    lista=palabras.hypernyms()
    temp=allSynLemma(lista)
    if len(temp)!=0:
        synonyms.update(temp)

    #hyponyms
    lista=palabras.hyponyms()
    temp=allSynLemma(lista)
    if len(temp)!=0:
        synonyms.update(temp)

    #member_holonyms
    lista=palabras.member_holonyms()
    temp=allSynLemma(lista)
    if len(temp)!=0:
        synonyms.update(temp)
    return synonyms



def wordDefinition(word):
    """
    The meaning of a word according to wordnet, remove stopwords
    Input: word (String)
    Return: (dictionary)
    """
    dic={}
    definitions=list(Word(word).definitions)
    #print definitions
    if len(definitions)!=0:
        lista=[]
        dic={}
        lista=definitions[0].split(' ')
        for palabra in lista:
            if palabra not in en_sw:
                #Meaning of a word
                palabra=lemmatize_word(palabra)
                #Insert in the dictionary
                if not(palabra in dic):
                    dic[palabra]=1
    return dic

def lemmatize_word(word):
    """
    Assign the base form of words
    Input: word (plural, capital letters)
    return: word (singular, lower letters)
    """
    palabra=word
    palabra=Word(str(palabra).lower() )
    palabra=palabra.lemmatize()
    if palabra==word:
        lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
        palabra = lemmatizer(word, u'NOUN')
        palabra=palabra[0]
    return palabra

def compareWorAtr(word,atri):
    """
    It extracts all the characteristics (Atributes) of a word according to the meaning of the WordNet dictionary
    remove stopwords and add synonyms (update dictionary with other dictionary)
    Input: word, atribut (string)
    return: (boolean)
    """
    definitions=list(Word(word).definitions)
    lista=[]
    dic={}
    syn={}
    #lemma={}
    for definition in definitions:
        lista=definition.split(' ')
        for palabra in lista:
            if palabra not in en_sw:

                #Meaning of a word (0)
                palabra=lemmatize_word(palabra)
                #Insert in the dictionary
                if not(palabra in dic):
                    dic[palabra]=0

                #Meaning of a word of the word (1)
                dicDef=wordDefinition(str(palabra))
                dic.update(dicDef)

                #Lemma of the word of the word (2)
                lemma=lemmalist(palabra)
                #print lemma
                dic.update(lemma)

    #Synonyms of the main word (3)
    syn=synonym(str(word).lower())
    #Update main dictionary
    dic.update(syn)
    #print "len:",len(dic),"\nDicc:",dic
    return (atri in dic)

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
            #if not( dic.has_key(word) ): #python2
            if not( word in dic ): #python3
                dic[(search,word)]=["R"]
    return dic


def search_word_dictionary(search):
    """
    Search a word in dictionary.com
    Input: search (string)
    Return: dic (dictionary)
    """
    dic={}
    r=requests.get("http://www.dictionary.com/browse/"+search)

    soup=BeautifulSoup(r.text, "html.parser")
    results=soup.find("div",{"class":"css-8lgfcg e1iplpfw1"})
    if results != None:
        all_info=results.findAll("ol",{"css-zw8qdz e1hk9ate4"})
        for item in all_info:
            line=item.findAll("li",{"class":"css-2oywg7 e1q3nk1v3"})
            for element in line:
                cad=element.get_text()
                words=cad.split(' ')
                if len(words)>0:
                    dic.update(words_to_dictionary(search,words))
    return dic

def search_word_thesaurus(search):
    """
    Search a word in thesaurus.com
    Input: search (string)
    Return: dic (dictionary)
    """
    dic={}
    r=requests.get("https://www.thesaurus.com/browse/"+search)

    soup=BeautifulSoup(r.text, "html.parser")
    results=soup.find("section",{"class":"MainContentContainer css-7vy5fk e1h3b0ep0"})
    if results != None:
        all_info=results.findAll("ul",{"css-1lc0dpe et6tpn80"})
        for item in all_info:
            line=item.findAll("li")
            for element in line:
                cad=element.get_text()
                words=cad.split(' ')
                if len(words)>0:
                    dic.update(words_to_dictionary(search,words))
    return dic

def search_word_wiki(search):
    """
    Search a word in en.wikipedia.org
    Input: search (string)
    Return: dic (dictionary)
    """
    dic={}
    page_py = wiki_wiki.page(search)
    if page_py.exists():
        level=0
        for s in page_py.sections:
            cad=s.text
            words=cad.split(' ')
            if len(words)>0:
                dic.update(words_to_dictionary(search,words))
            level+=1
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
        words, scores = s2v.most_similar(vector, n=900)
        for word, score in zip(words, scores):
            if (score > 0.5):
                temp=word[0:-5]
                wordsV.append(temp)
        dic=words_to_dictionary(search,wordsV)
        return dic
    except:
        return dic

def compare_word_feature(word,atri):
    """
    It extracts all the characteristics (Atributes) of a word according to the meaning of the online dictionary, wiki and sense2vec
    Input: word, atribut (string)
    return: true or false (boolean)
    retunr: dictionary with word,atrib (dictionary)
    """
    features={}
    features=search_word_dictionary(word)
    features.update(search_word_thesaurus(word))
    features.update(search_word_wiki(word))
    features.update(search_word_sense2vec(word))

    #print "len:",len(features),"\nDicc:",features
    #return features.has_key((word,atri)),features
    return ((word,atri) in features),features#python3

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
    dicWeb={}
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
    ruta="resultados-M1.3.0.txt"
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
        temp0=line[0]
        temp1=line[1]
        temp2=line[2]
        line[0]=lemmatize_word(line[0])
        line[1]=lemmatize_word(line[1])
        line[2]=lemmatize_word(line[2])
        
        w1aPos=((line[0],line[2]) in dicPos)
        w2aPos=((line[1],line[2]) in dicPos)
        w1aNeg=((line[0],line[2]) in dicNeg)
        w2aNeg=((line[1],line[2]) in dicNeg)

        #Find the meaning of the word in a dictionary
        if not(w1aPos):
            w1a=compareWorAtr(line[0],line[2])
            #Search the word in WEB and update the variable and the dictionary
            if not(w1a) and not((line[0]) in dicWeb):
                w1a,features=compare_word_feature(line[0],line[2])
                dicPos.update(features)
                dicWeb[line[0]]=1
                if not(w1a) and not((line[2]) in dicWeb):
                    w1a,features=compare_word_feature(line[2],line[0])
                    dicPos.update(features)
                    dicWeb[line[2]]=1
                    if not(w1a):
                        w1a=similaritySpyCy(line[0],line[2])
        else:
            w1a=True

        if not(w2aPos):
            w2a=compareWorAtr(line[1],line[2])
            #Search the word in WEB and update the variable and the dictionary
            if not(w2a) and not((line[1]) in dicWeb):
                w2a,features=compare_word_feature(line[1],line[2])
                dicPos.update(features)
                dicWeb[line[1]]=1
                if not(w2a) and not(line[2] in dicWeb):
                    w2a,features=compare_word_feature(line[1],line[2])
                    dicPos.update(features)
                    dicWeb[line[1]]=1
                    if not(w2a):
                        w2a=similaritySpyCy(line[1],line[2])
        else:
            w2a=True

        if w1aNeg or (w1aPos and w2aPos): #dictionary negative
            #dicNeg[line[0],line[2]].append(line[1])
            result.write(str(temp0)+","+str(temp1)+","+str(temp2)+",0\n");
        elif ((w1aPos and w2aNeg) or (w1aPos and not(w2a)) or (w1a and w2aNeg) or (w1a and not(w2a)) ):
            #dictionary positive
            if not(w1aPos): #inserta w1 en dicPos
                dicPos[line[0],line[2]]=[line[1]]
            if not(w2aNeg): ##inserta w2 en dicNeg
                dicNeg[line[1],line[2]]=[line[0]]
            result.write(str(temp0)+","+str(temp1)+","+str(temp2)+",1\n");
        else: #dictionary negative
            #dicNeg[line[0],line[2]]=[line[1]]
            result.write(str(temp0)+","+str(temp1)+","+str(temp2)+",0\n");

    result.close()

    print ("\nDiccionarios Train y Test despues de clasificar")
    print ("elementos dicPos ",len(dicPos))
    print ("elementos dicNeg ",len(dicNeg))

    #print dicPos.keys()
    print ("\nPuede revisar el archivo de resultados en: ",ruta)
    print ("Execution Time: ",time.time()-starting_point)

if __name__ == "__main__":
    main()
