from typing import List
from extractors.BaseExtractor import BaseExtractor
import yake

class YakeExtractor(BaseExtractor):
    def extractKeyWords(self, doc:str, top_k:int) -> List[str]:
        kw_extractor = yake.KeywordExtractor(top=top_k, n=self.n_grams_max, windowsSize=1)
        keywords = kw_extractor.extract_keywords(doc)
        return list(map(lambda x:x[0], keywords))
