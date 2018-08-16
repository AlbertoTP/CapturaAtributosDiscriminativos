# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 21:30:21 2018

@author: alternatif
"""
import time
from nltk.corpus import wordnet as wn
import spacy
#nlp = spacy.load('en')
#nlp = spacy.load('en_core_web_lg')
nlp = spacy.load('en_vectors_web_lg')

def similarityWordNet(word1,word2):
    """
    Similarity between two words with nltk
    Input: word1, word2 (String)
    Return: similarity (float)
    """
    #print Word(word1).lemmatize()
    #print Word(word2).lemmatize()
    word1=wn.synset(str(word1)+'.n.01')
    word2=wn.synset(str(word2)+'.n.01')
    
    """
    Return a score denoting how similar two word senses are,
    based on the shortest path that connects the senses in the is-a
    (hypernym/hypnoym) taxonomy. The score is in the range 0 to 1.
    """
    #similarity1 = word1.path_similarity(word2)
    similarity1 = wn.path_similarity(word1, word2)
    
    """
    Leacock-Chodorow Similarity: Return a score denoting how similar
    two word senses are, based on the shortest path that connects
    the senses (as above) and the maximum depth of the taxonomy in
    which the senses occur. range 3.6
    """
    similarity2 = wn.lch_similarity(word1, word2)
    
    """
    Wu-Palmer Similarity: Return a score denoting how similar
    two word senses are, based on the depth of the two senses in
    the taxonomy and that of their Least Common Subsumer (most specific ancestor node).
    range 0.92
    """
    similarity3 = wn.wup_similarity(word1, word2)
    
    print ("similarity1: ",similarity1)
    print ("similarity2: ",similarity2)
    print ("similarity3: ",similarity3)
    
def similaritySpyCy(word1,word2):        
    """
    Similarity between two words with Spicy
    Input: word1, word2 (String)
    Return: similarity (float)
    """    
    tokens = nlp( (word1+" "+word2))
    #print tokens
    #print "Similarity Spacy:",tokens[0].similarity(tokens[1])
    try:
        if tokens[0].similarity(tokens[1])>0.5:
            return True
    except:
        return False
    return False

    
def main():
    starting_point = time.time()
    
    word1="sandwich"
    word2="lunch"
    print ("\nSimilarity between "+word1+" "+word2)
    similarityWordNet(word1,word2)
    print ("Similarity Spacy:",similaritySpyCy(word1,word2))
    
    word1="sandwich"
    word2="sandwich"
    print ("\nSimilarity between "+word1+" "+word2)
    print ("Similarity WordNet:",similarityWordNet(word1,word2))
    print ("Similarity Spacy:",similaritySpyCy(word1,word2))

    word1="breakfast"
    word2="lunch"
    print ("\nSimilarity between "+word1+" "+word2)
    similarityWordNet(word1,word2)
    print ("Similarity Spacy:",similaritySpyCy(word1,word2))
    
    word1="pig"
    word2="pink"
    print ("\nSimilarity between "+word1+" "+word2)
    similarityWordNet(word1,word2)
    print ("Similarity Spacy:",similaritySpyCy(word1,word2))
    
    print ("\nExecution Time: ",time.time()-starting_point)
    
if __name__ == "__main__":
    main()
    