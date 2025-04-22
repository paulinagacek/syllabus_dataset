from typing import List
from extractors.BaseExtractor import BaseExtractor
import re

def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


class RakeExtractor(BaseExtractor):
    def __init__(self):
        BaseExtractor.__init__(self)

    def extractKeyWords(self, doc:str, top_k:int) -> List[str]:
        sentence_list = self.split_into_sentences(doc)
        phrase_list = self.generate_candidate_keywords(sentence_list)
        word_scores = self.calculate_word_scores(phrase_list)
        keyword_candidates = self.generate_candidate_keyword_scores(phrase_list, word_scores)

        sorted_keywords = sorted(keyword_candidates.items(), key=lambda item: item[1], reverse=True)[:top_k]
        return list(map(lambda x: x[0], sorted_keywords))
    
    def generate_candidate_keywords(self, sentence_list):
        phrase_list = []
        for s in sentence_list:
            tmp = re.sub(self.stop_words_pattern, '|', s.strip().lower())
            phrases = tmp.split("|")
            for phrase in phrases:
                phrase = phrase.strip()
                if phrase != "":
                    phrase_list.append(phrase)
        return phrase_list
    
    def calculate_word_scores(self, phraseList):
        word_frequency = {}
        word_degree = {}
        for phrase in phraseList:
            word_list = self.separate_words(phrase, 0)
            word_list_length = len(word_list)
            word_list_degree = word_list_length - 1
            #if word_list_degree > 3: word_list_degree = 3 #exp.
            for word in word_list:
                word_frequency.setdefault(word, 0)
                word_frequency[word] += 1
                word_degree.setdefault(word, 0)
                word_degree[word] += word_list_degree  #orig.
                #word_degree[word] += 1/(word_list_length*1.0) #exp.
        for item in word_frequency:
            word_degree[item] = word_degree[item] + word_frequency[item]

        # Calculate Word scores = deg(w)/frew(w)
        word_score = {}
        for item in word_frequency:
            word_score.setdefault(item, 0)
            word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
        #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
        return word_score
    
    def separate_words(self, text, min_word_return_size):
        """
        Utility function to return a list of all words that are have a length greater than a specified number of characters.
        @param text The text that must be split in to words.
        @param min_word_return_size The minimum no of characters a word must have to be included.
        """
        splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
        words = []
        for single_word in splitter.split(text):
            current_word = single_word.strip().lower()
            #leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
            if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
                words.append(current_word)
        return words


    def generate_candidate_keyword_scores(self, phrase_list, word_score):
        keyword_candidates = {}
        for phrase in phrase_list:
            keyword_candidates.setdefault(phrase, 0)
            word_list = self.separate_words(phrase, 0)
            candidate_score = 0
            for word in word_list:
                candidate_score += word_score[word]
            keyword_candidates[phrase] = candidate_score
        return keyword_candidates