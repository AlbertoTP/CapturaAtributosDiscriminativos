# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 19:51:51 2018

@author: alternatif
"""

from spacy.tokens import Token
fruit_getter = lambda token: token.text in ('apple', 'pear', 'banana')
Token.set_extension('is_fruit', getter=fruit_getter)
doc = nlp(u'I have an apple')
assert doc[3]._.is_fruit