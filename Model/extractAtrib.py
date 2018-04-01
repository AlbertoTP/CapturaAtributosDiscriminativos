# -*- coding: utf-8 -*-
"""
@author: Alberto
"""
import time
import spacy
nlp = spacy.load('en')
from textblob import Word
from textblob.wordnet import Synset
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
#Stopwords in English
en_sw = set(sw.words('english'))
#print en_sw

def similarityWords(word1,word2):
    """
    Similarity between two words with textblob
    Input: word1, word2 (String)
    Return: similarity (float)
    """
    #print Word(word1).lemmatize()
    #print Word(word2).lemmatize()
    word1=Synset(str(word1)+'.n.01')
    word2=Synset(str(word2)+'.n.01')
    return word1.path_similarity(word2)



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
                if not(syn_set.has_key(item)):
                    syn_set[item]=2;
            cont+=1
        else:
            break
    #print syn_set
    return syn_set
    
    
    
def allSynLemma(lista):
    synonyms={}
    if len(lista)!=0:
        for element in lista:
            #print ">>> ", element.lemma_names()
            for i in element.lemma_names():
                #print i
                vec=i.split("_")
                if len(vec)>1:
                    for j in vec:
                        if not(synonyms.has_key(j)):
                            synonyms[j]=3
                elif not(synonyms.has_key(i)):
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
    #print palabras[0]," \tType: ",type(palabras[0])
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
            #print palabra
            if palabra not in en_sw:
                #Meaning of a word
                palabra=Word(str(palabra).lower() )
                palabra=palabra.lemmatize()
                #print ">> ",palabra
                #Insert in the dictionary
                if not(dic.has_key(palabra)):
                    dic[palabra]=1
    #print dic
    return dic

def featuresWord(word):
    """
    The meaning of a word according to wordnet, remove stopwords and add synonyms (update dictionary with other dictionary)
    Input: word (String)
    Return: (dictionary)
    """
    definitions=list(Word(word).definitions)
    #print definitions
    lista=[]
    dic={}
    syn={}
    #lemma={}
    for definition in definitions:
        #print "> ",definition
        lista=definition.split(' ')
        for palabra in lista:
            #print palabra
            if palabra not in en_sw:
                
                #Meaning of a word (0)
                palabra=Word(str(palabra).lower() )
                palabra=palabra.lemmatize()
                #print ">> ",palabra,type(palabra)
                #Insert in the dictionary
                if not(dic.has_key(palabra)):
                    dic[palabra]=0
                
                #Meaning of a word of the word (1)
                dicDef=wordDefinition(str(palabra))
                dic.update(dicDef)
                
                #Lemma of the word of the word (2)
                lemma=lemmalist(palabra)
                #print lemma
                dic.update(lemma)
                
                #Synonyms of the word of the word (3)
                #syn=synonym(str(palabra))
                #print syn
                #dic.update(syn)
                
    #Synonyms of the main word (3)
    syn=synonym(str(word).lower())
    #Update main dictionary
    dic.update(syn)
    #print dic
    #print "len ",len(dic)
    return dic
    
def compareWorAtr(word,atri):
    """
    It extracts all the characteristics (Atributes) of a word according to the meaning of the WordNet dictionary
    Input: word, atribut (string)
    return: (boolean)
    """
    features={}
    features=featuresWord(word)
    #print "len:",len(features),"\nDicc:",features
    return features.has_key(atri)



def main():
    starting_point = time.time()
    #print compareWorAtr("apple","oval")
    #print featuresWord("apple")
    print "1:apple-red ",compareWorAtr("apple","red")
    print "2:apple-blue ",compareWorAtr("apple","blue")

    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()