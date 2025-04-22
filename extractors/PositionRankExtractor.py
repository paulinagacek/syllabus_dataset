from typing import List
from extractors.BaseExtractor import BaseExtractor
import spacy
import pytextrank # used by spacy in the pipeline

class PositionRankExtractor(BaseExtractor):
    def __init__(self):
        BaseExtractor.__init__(self)
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("positionrank")
        

    def extractKeyWords(self, doc:str, top_k:int) -> List[str]:
        doc = self.nlp(doc)
        return list(map(lambda x:x.text, doc._.phrases[:top_k]))
