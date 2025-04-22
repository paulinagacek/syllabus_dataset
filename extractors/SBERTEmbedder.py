from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class SBERTEmbedder:
    def __init__(self, embedding_model: str):
        super().__init__()
        self.embedding_model = SentenceTransformer(embedding_model)

    def embed(self, documents: List[str]) -> np.ndarray:
        """Embed a list of n documents/words into an n-dimensional
        matrix of embeddings

        Arguments:
            documents: A list of documents or words to be embedded
            verbose: Controls the verbosity of the process

        Returns:
            Document/words embeddings with shape (n, m) with `n` documents/words
            that each have an embeddings size of `m`
        """
        return self.embedding_model.encode(documents)
