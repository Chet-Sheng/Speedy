from .base_model import BaseModel
from ..registry import register_model
from ..types import ModelName

@register_model(ModelName.sparse)
class SparseRetriever(BaseModel):
    def predict(self, text: str):
        if self.filter:
            text = self.filter.apply(text)
        chunks = self.splitter.split(text)
        embeddings = [self.embedder.embed(c) for c in chunks]
        if self.reranker:
            embeddings = self.reranker.rerank(embeddings)
        return f"SparseRetriever: {embeddings}" 