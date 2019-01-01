# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

from nltk.stem import WordNetLemmatizer

#wikipedia in english
import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('en')

from nltk.corpus import stopwords as sw
en_sw = set(sw.words('english'))

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
    Search a word in dictionary.com
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

word="lunch"
#print (search_word_dictionary(word))
#print (search_word_thesaurus(word))
print (search_word_wiki(word))