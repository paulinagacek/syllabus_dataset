from typing import List
from nltk import PorterStemmer
import re
import os
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.resolve())

nb_dir = os.path.split(os.getcwd())[0]
if nb_dir not in sys.path:
    sys.path.append(nb_dir)

class BaseExtractor:
    def __init__(self) -> None:
        self.n_grams_max=3
        
        self.porter = PorterStemmer()

        self.stop_words_path = "config/SmartStoplist.txt"
        self.stop_words_pattern = self.build_stop_word_regex()

    def extractKeyWords(self, doc:str, top_k:int) -> List[str]:
        pass
    
    def split_into_sentences(self, text:str):
        sentence_delimiters = re.compile(u'[.!?,;:\'\t\\\\"\\(\\)\\\u2019\u2013]|\\s\\-\\s')
        sentences = sentence_delimiters.split(text)
        return sentences
    
    def load_stop_words(self):
        stop_words = []
        with open(self.stop_words_path, 'r') as f:
            stop_words = f.read().split('\n')
        return stop_words
    
    def build_stop_word_regex(self):
        stop_word_regex_list = map(lambda word:  r'\b' + word + r'(?![\w-])' , self.load_stop_words())
        return re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
