from .PositionRankExtractor import PositionRankExtractor
from .YakeExtractor import YakeExtractor
from .KeyBERTExtractor import KeyBERTExtractor
from .RakeExtractor import RakeExtractor
from .TextRankExtractor import TextRankExtractor


extractors = {
    "Position Rank": PositionRankExtractor(),
    "YAKE": YakeExtractor(),
    "Key BERT": KeyBERTExtractor(),
    "RAKE": RakeExtractor(),
    "TextRank": TextRankExtractor(),
}
