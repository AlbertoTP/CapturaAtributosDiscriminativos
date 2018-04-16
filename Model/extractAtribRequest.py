# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 19:42:31 2018

@author: AlbertoTP
"""
import requests
import time
import re
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords as sw
#Stopwords in English
en_sw = set(sw.words('english'))



def words_to_dictionary(search,words):
    """
    delete special characters, numbers and stopwords. lemmatize the word and insert in a dictionary
    Input: words (Vector String)
    Return: dic (dictionary)
    """
    dic={}
    for word in words:
        #print (word)
        word=str(word.encode('ascii', 'ignore')).lower()
        word=re.sub(r'[0-9]', '', word)
        word=re.sub('\W+','', word )
        if word not in en_sw:
            #print (word)
            wordnet_lemmatizer = WordNetLemmatizer()
            word=wordnet_lemmatizer.lemmatize(word)
            if not( dic.has_key(word) ): #python2
            #if not( word in dic ): #python3
                dic[(search,word)]=["R"]
    return dic


def search_word_dictionary(search):
    """
    Search a word in dictionary.com
    Input: search (string)
    Return: dic (dictionary)
    """
    #print search
    dic={}
    r=requests.get("http://www.dictionary.com/browse/"+search)
    
    soup=BeautifulSoup(r.text, "html.parser")
    results=soup.find("div",{"class":"source-data"})
    #print results
    if results != None:
        all_info=results.findAll("section",{"class":"def-pbk ce-spot"})
        #print (all_info)
        
        for item in all_info:
            line=item.findAll("div",{"class":"def-content"})
            for element in line:
                cad=element.get_text()
                #print (cad)
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
    r=requests.get("https://en.wikipedia.org/wiki/"+search)
    
    soup=BeautifulSoup(r.text, "html.parser")
    results=soup.find("div",{"class":"mw-parser-output"})
    all_info=results.findAll("p")
    #print (all_info)
    #print (len(all_info))
    if len(all_info)<2:
        return dic
    
    i=0
    for item in all_info:
        if (i<3):
            #print (item.get_text())
            #print (type(line))
            line=item.get_text()
            words=line.split(' ')
            #print (words)
            if len(words)>0:
                dic.update(words_to_dictionary(search,words))
        i+=1
    return dic
    
def compare_word_feature(word,atri):
    """
    It extracts all the characteristics (Atributes) of a word according to the meaning of the WordNet dictionary
    Input: word, atribut (string)
    return: true or false (boolean)
    retunr: dictionary with word,atrib (dictionary)
    """
    features={}
    features=search_word_dictionary(word)
    features.update(search_word_wiki(word))
    
    #print "len:",len(features),"\nDicc:",features
    return features.has_key((word,atri)),features

        
def main():
    starting_point = time.time()
    print ('Search "sandwich" with BeautifulSoup')
    search = "Sandwich"
    dic={}
    print("Search a word in en.wikipedia.org")
    dic=search_word_wiki(search)
    print (dic)
    print (len(dic))
    print("Search a word in dictionary.com")
    dic.update(search_word_dictionary(search))
    print (dic)
    print (len(dic))
    
    print("\nWith one function\nWord: Sandwich, Feature: lunch")
    key,feat=compare_word_feature(search,"lunch")
    print (key)
    print (len(feat))
    
    print ("Execution Time: ",time.time()-starting_point)
    
if __name__ == "__main__":
    main()