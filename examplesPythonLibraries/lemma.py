# -*- coding: utf-8 -*-

from textblob import Word
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

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

print (lemmatize_word("dogs"))
print (lemmatize_word("CATS"))
print (lemmatize_word("men"))
print (lemmatize_word("children"))
print (lemmatize_word("knives"))
print (lemmatize_word("feet"))
print (lemmatize_word("people"))
print (lemmatize_word("teeth"))
print (lemmatize_word("sheep"))
print (lemmatize_word("gokussj"))


lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
lemmas = lemmatizer(u'ducks', u'NOUN')
print (lemmas)
lemmas = lemmatizer(u'men', u'NOUN')
print (lemmas)
lemmas = lemmatizer(u'people', u'NOUN')
print (lemmas)
lemmas = lemmatizer(u'sheep', u'NOUN')
print (lemmas)