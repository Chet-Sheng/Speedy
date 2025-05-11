from pydantic import BaseModel
from enum import Enum

from .types import ModelName, EmbedderName, SplitterName, RerankerName, FilterName

class ModelConfig(BaseModel):
    model_name: ModelName
    embedder: EmbedderName
    splitter: SplitterName
    reranker: RerankerName = RerankerName.none
    filter: FilterName = FilterName.none 