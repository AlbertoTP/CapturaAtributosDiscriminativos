# -*- coding: utf-8 -*-
"""

WordNet Integration

You can access the synsets for a Word via the synsets property
or the get_synsets method, optionally passing in a part of speech.

"""

from textblob import Word
from textblob.wordnet import VERB
word = Word("octopus")
print word.synsets
#[Synset('octopus.n.01'), Synset('octopus.n.02')]
print Word("hack").get_synsets(pos=VERB)
#[Synset('chop.v.05'), Synset('hack.v.02'), Synset('hack.v.03'), Synset('hack.v.04'), Synset('hack.v.05'), Synset('hack.v.06'), Synset('hack.v.07'), Synset('hack.v.08')]

"""
You can access the definitions for each synset via the definitions property
or the define() method, which can also take an optional part-of-speech argument.
"""

print Word("octopus").definitions
#['tentacles of octopus prepared as food', 'bottom-living cephalopod having a soft oval body with eight long tentacles']
print ">Ejemplo banana"
print Word("banana").definitions


"""
You can also create synsets directly.
"""
from textblob.wordnet import Synset
octopus = Synset('octopus.n.02')
shrimp = Synset('shrimp.n.03')
print "Synsets octopus - shrimp = ",octopus.path_similarity(shrimp)
#0.1111111111111111

apple = Synset('apple.n.01')
banana = Synset('banana.n.01')
print "Synsets apple - banana = ",apple.path_similarity(banana)


print ">Ejemplo apple"
significados=Word("apple").synsets
print significados
for i in significados:
    print i.definition()


"""
You can restrict which synsets to retrieve for a word for that word only
when used as a particular part of speech (say noun or verb).
"""
print "-----------------"
from textblob import Word
from textblob.wordnet import NOUN
synsets = Word("apple").get_synsets(pos=NOUN)
for synset in synsets:
    print synset.definition()
    
"""
We can also take any synset and use its .lemma_names()
method to get all of the words belonging to the synset,
essentially giving us a list of synonyms (words that mean the same thing).
Let’s find synonyms for “bank” in the sense of “financial institutions”
(element 1 from the list above):
"""
print "-----------------"
from textblob import Word
from textblob.wordnet import NOUN
synsets = Word("apple").get_synsets(pos=NOUN)
print ">solo uno"
print synsets[1].lemma_names()
print ">todos"
for synset in synsets:
    print synset.lemma_names()
#[u'depository_financial_institution', u'bank', u'banking_concern', u'banking_company']