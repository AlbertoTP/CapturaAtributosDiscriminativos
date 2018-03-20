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
    Similarity between two words
    Input: word1, word2 (String)
    Return: similarity (float)
    """
    #print Word(word1).lemmatize()
    #print Word(word2).lemmatize()
    word1=Synset(str(word1)+'.n.01')
    word2=Synset(str(word2)+'.n.01')
    return word1.path_similarity(word2)
    
def synonym(word):
    """
    first synonyms, hypernyms, hyponyms and member_holonyms of the one word
    Input: word (String)
    Return: synonims (dictionary)
    """
    synonyms={}
    palabras = wn.synset(str(word)+'.n.01')
    #Agregar >>>>>exception<<<<
    lista=palabras.hypernyms()
    for element in lista:
        #print ">>> ",i.lemma_names()
        for i in element.lemma_names():
            #print i
            vec=i.split("_")
            if len(vec)>1:
                for j in vec:
                    if not(synonyms.has_key(j)):
                        synonyms[j]=0;
            elif not(synonyms.has_key(i)):
                synonyms[i]=0;
    #print palabras.hyponyms()
    #print palabras.member_holonyms()
    return synonyms

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
    for definition in definitions:
        #print definition
        lista=definition.split(' ')
        for palabra in lista:
            if palabra not in en_sw:
                dic[palabra.lower()]=1
                #syn=synonym(palabra.lower())
                #dic.update(syn)
    return dic
    
def compareWorAtr(word,atri):
    """
    It extracts all the characteristics (Atributes) of a word according to the meaning of the WordNet dictionary
    Input: word, atribut (string)
    return: (boolean)
    """
    features={}
    features=featuresWord(word)
    return features.has_key(atri)

def main():
    starting_point = time.time()
    #print compareWorAtr("apple","oval")
    #print featuresWord("apple")
    print compareWorAtr("apple","red")
    print compareWorAtr("apple","blue")    

    print "Execution Time: ",time.time()-starting_point
    
if __name__ == "__main__":
    main()