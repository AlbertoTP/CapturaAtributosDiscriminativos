# -*- coding: utf-8 -*-
"""
Usage with spaCy
"""
#import spacy
#import sense2vec
#from sense2vec import Sense2VecComponent
#
#nlp = spacy.load('en')
#s2v = Sense2VecComponent('/usr/local/lib/python3.5/dist-packages/sense2vec/reddit_vectors-1.1.0/')
#nlp.add_pipe(s2v)
#doc = nlp(u"A sentence about natural language processing.")
#assert doc[3].text == u'natural language processing'
#freq = doc[3]._.s2v_freq
#vector = doc[3]._.s2v_vec
#most_similar = doc[3]._.s2v_most_similar(3)
#print (most_similar)
# [(('natural language processing', 'NOUN'), 1.0),
#  (('machine learning', 'NOUN'), 0.8986966609954834),
#  (('computer vision', 'NOUN'), 0.8636297583580017)]


"""
Standalone usage without spaCy
"""
import sense2vec

s2v = sense2vec.load('/usr/local/lib/python3.5/dist-packages/sense2vec/reddit_vectors-1.1.0/')
query = u'natural_language_processing|NOUN'
assert query in s2v
freq, vector = s2v[query]
words, scores = s2v.most_similar(vector, 3)
most_similar = list(zip(words, scores))
print (most_similar)
#model.most_similar(['onion_rings|NOUN'])


"""
Function
"""

import re
from nltk.corpus import stopwords as sw
en_sw = set(sw.words('english'))
from nltk.stem import WordNetLemmatizer

import sense2vec
s2v = sense2vec.load('/usr/local/lib/python3.5/dist-packages/sense2vec/reddit_vectors-1.1.0/')

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


mword="otolaryngologist"
wsearch=mword+"|NOUN"

wordsV=[]
try:
    freq, vector = s2v[wsearch]
    words, scores = s2v.most_similar(vector, n=10)
    for word, score in zip(words, scores):
        #print(word, score)
        if (score > 0.5):
            #print(">",word,score)
            temp=word[0:-5]
            wordsV.append(temp)
            #print (temp)
    print (wordsV)
    dic=words_to_dictionary(mword,wordsV)
    print (dic)
except:
    print ("Word doesnt exist")