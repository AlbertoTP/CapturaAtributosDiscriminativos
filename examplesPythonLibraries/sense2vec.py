# -*- coding: utf-8 -*-
#import spacy
#from sense2vec import Sense2VecComponent
#
#nlp = spacy.load('en')
#s2v = Sense2VecComponent('/usr/local/lib/python3.5/dist-packages')
#nlp.add_pipe(s2v)
#
#doc = nlp(u"A sentence about natural language processing.")
#assert doc[3].text == u'natural language processing'
#freq = doc[3]._.s2v_freq
#vector = doc[3]._.s2v_vec
#most_similar = doc[3]._.s2v_most_similar(3)
# [(('natural language processing', 'NOUN'), 1.0),
#  (('machine learning', 'NOUN'), 0.8986966609954834),
#  (('computer vision', 'NOUN'), 0.8636297583580017)]

import sense2vec

s2v = sense2vec.load('/usr/local/lib/python3.5/dist-packages/sense2vec/')
query = u'natural_language_processing|NOUN'
assert query in s2v
freq, vector = s2v[query]
words, scores = s2v.most_similar(vector, 3)
most_similar = list(zip(words, scores))