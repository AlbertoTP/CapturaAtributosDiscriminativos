# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 19:51:51 2018

@author: alternatif
"""

import spacy

nlp = spacy.load('en')
#nlp = spacy.load('en_core_web_sm')


from spacy.tokens import Token
fruit_getter = lambda token: token.text in ('apple', 'pear', 'banana')
Token.set_extension('is_fruit', getter=fruit_getter)
doc = nlp(u'I have an apple')
assert doc[3]._.is_fruit


tokens = nlp(u'dog cat banana')

for token1 in tokens:
    for token2 in tokens:
        print(token1, token2, token1.similarity(token2))
        
        
#nlp = spacy.load('en_core_web_lg')
#tokens = nlp(u'dog cat banana sasquatch')
#
#for token in tokens:
#    print(token.text, token.has_vector, token.vector_norm, token.is_oov)
    
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)



import spacy
from spacy import displacy

nlp = spacy.load('en')
doc = nlp(u'This is a sentence.')
displacy.serve(doc, style='dep')