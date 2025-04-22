from extractors.BaseExtractor import BaseExtractor
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer

# https://maartengr.github.io/KeyBERT/

class KeyBERTExtractor(BaseExtractor):
    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        BaseExtractor.__init__(self)
        self.kw_model = KeyBERT(model= "all-mpnet-base-v2")

    def extractKeyWords(self, doc: str, top_k:int):
        doc = [doc]
        v = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
        keywords = self.kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), top_n=top_k, 
                                     diversity=0.7, use_mmr=True, vectorizer=v)
        return list(map(lambda x: x[0], keywords))
