# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 19:16:58 2018

@author: alternatif
"""

import multiprocessing as mp
import nltk

corpus = {f_id: nltk.corpus.gutenberg.raw(f_id)
          for f_id in nltk.corpus.gutenberg.fileids()}

def tokenize_and_pos_tag(pair):
    f_id, doc = pair
    return f_id, nltk.pos_tag(nltk.word_tokenize(doc))


if __name__ == '__main__':
    # automatically uses mp.cpu_count() as number of workers
    # mp.cpu_count() is 4 -> use 4 jobs
    with mp.Pool() as pool:
        tokens = pool.map(tokenize_and_pos_tag, corpus.items())