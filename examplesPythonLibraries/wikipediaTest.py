# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 00:57:41 2018
@author: alternatif
"""
search="sandwich"

import time
import wptools


#https://github.com/siznax/wptools
starting_point = time.time()
page = wptools.page(search)
print (page.get_query())
print ("Execution Time wptools: ",time.time()-starting_point)


import requests
from bs4 import BeautifulSoup
starting_point = time.time()

dic={}
r=requests.get("https://en.wikipedia.org/wiki/"+search)
soup=BeautifulSoup(r.text, "html.parser")
results=soup.find("div",{"class":"mw-parser-output"})
all_info=results.findAll("p")
#print (all_info)
#print (len(all_info))
print ("Execution Time request: ",time.time()-starting_point)


#http://wikipedia-api.readthedocs.io/en/latest/README.html
import wikipediaapi
starting_point = time.time()

wiki_wiki = wikipediaapi.Wikipedia('en')
page_py = wiki_wiki.page(search)
print("Page - Exists: %s" % page_py.exists())
#print("Page - Title: %s" % page_py.title)
print("Page - Summary: %s" % page_py.summary)

#wiki_wiki = wikipediaapi.Wikipedia(
#        language='en',
#        extract_format=wikipediaapi.ExtractFormat.WIKI
#)
#
#p_wiki = wiki_wiki.page(search)
#print(p_wiki.text)

def print_sections(sections, level=0):
    for s in sections:
        print (s.text)
        #print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:50]))
        print_sections(s.sections, level + 1)


print_sections(page_py.sections)

#def print_links(page):
#        links = page.links
#        for title in sorted(links.keys()):
#            #print("%s: %s" % (title, links[title]))
#            print("%s" % (title))
#
#print_links(page_py)



print ("Execution Time wikipediaapi: ",time.time()-starting_point)


dic1={"hola":1,"adios":2}
dic2={"hola":1,"adios":2,"saludo":3}
print ("hola1" in dic1)