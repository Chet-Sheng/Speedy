from abc import ABC, abstractmethod
from typing import Optional

class BaseModel(ABC):
    def __init__(self, embedder, splitter, reranker=None, filter_=None):
        self.embedder = embedder
        self.splitter = splitter
        self.reranker = reranker
        self.filter = filter_

    @abstractmethod
    def predict(self, text: str):
        pass 