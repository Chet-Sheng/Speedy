# config.py
from pydantic import BaseModel
from enum import Enum

from .types import ModelName, EmbedderName, SplitterName, RerankerName, FilterName

class ModelConfig(BaseModel):
    model_name: ModelName
    embedder: EmbedderName
    splitter: SplitterName
    reranker: RerankerName = RerankerName.none
    filter: FilterName = FilterName.none

# types.py
from enum import Enum

class ModelName(str, Enum):
    dense = "dense"
    sparse = "sparse"

class EmbedderName(str, Enum):
    openai = "openai"

class SplitterName(str, Enum):
    sentence = "sentence"

class RerankerName(str, Enum):
    none = "none"

class FilterName(str, Enum):
    none = "none" 


# registry.py
import logging
from typing import Dict, Type
from config import ModelConfig

logger = logging.getLogger("model_builder")

MODEL_REGISTRY: Dict[str, Type] = {}
EMBEDDER_REGISTRY: Dict[str, Type] = {}
SPLITTER_REGISTRY: Dict[str, Type] = {}
RERANKER_REGISTRY: Dict[str, Type] = {}
FILTER_REGISTRY: Dict[str, Type] = {}

def register_model(name: str):
    def decorator(cls):
        MODEL_REGISTRY[name] = cls
        return cls
    return decorator

def register_embedder(name: str):
    def decorator(cls):
        EMBEDDER_REGISTRY[name] = cls
        return cls
    return decorator

def register_splitter(name: str):
    def decorator(cls):
        SPLITTER_REGISTRY[name] = cls
        return cls
    return decorator

def register_reranker(name: str):
    def decorator(cls):
        RERANKER_REGISTRY[name] = cls
        return cls
    return decorator

def register_filter(name: str):
    def decorator(cls):
        FILTER_REGISTRY[name] = cls
        return cls
    return decorator

def build_model(config: ModelConfig):
    logger.info(f"Building model: {config.model_name}")

    model_class = MODEL_REGISTRY[config.model_name.value]
    embedder_class = EMBEDDER_REGISTRY[config.embedder.value]
    splitter_class = SPLITTER_REGISTRY[config.splitter.value]
    reranker_class = RERANKER_REGISTRY.get(config.reranker.value)
    filter_class = FILTER_REGISTRY.get(config.filter.value)

    embedder = embedder_class()
    splitter = splitter_class()
    reranker = reranker_class() if reranker_class else None
    filter_ = filter_class() if filter_class else None

    logger.debug("Instantiating model with components")
    return model_class(embedder=embedder, splitter=splitter, reranker=reranker, filter_=filter_)


# models/dense_retriever.py
from models.base_model import BaseModel

class DenseRetriever(BaseModel):
    def predict(self, text: str):
        if self.filter:
            text = self.filter.apply(text)
        chunks = self.splitter.split(text)
        embeddings = [self.embedder.embed(c) for c in chunks]
        if self.reranker:
            embeddings = self.reranker.rerank(embeddings)
        return f"DenseRetriever: {embeddings}"


# models/sparse_retriever.py
from models.base_model import BaseModel

class SparseRetriever(BaseModel):
    def predict(self, text: str):
        if self.filter:
            text = self.filter.apply(text)
        chunks = self.splitter.split(text)
        embeddings = [self.embedder.embed(c) for c in chunks]
        if self.reranker:
            embeddings = self.reranker.rerank(embeddings)
        return f"SparseRetriever: {embeddings}"


# embedders/openai_embedder.py
from embedders.base import BaseEmbedder

class OpenAIEmbedder(BaseEmbedder):
    def embed(self, text):
        return f"embedding:{text}"


# splitters/sentence_splitter.py
from splitters.base import BaseSplitter

class SentenceSplitter(BaseSplitter):
    def split(self, text):
        return text.split(".")


# bindings.py
from registry import register_model, register_embedder, register_splitter
from models.dense_retriever import DenseRetriever
from models.sparse_retriever import SparseRetriever
from embedders.openai_embedder import OpenAIEmbedder
from splitters.sentence_splitter import SentenceSplitter

register_model("dense")(DenseRetriever)
register_model("sparse")(SparseRetriever)
register_embedder("openai")(OpenAIEmbedder)
register_splitter("sentence")(SentenceSplitter)


# main.py
from config import ModelConfig
from registry import build_model
import bindings  # Ensures all components are registered

cfg = ModelConfig(model_name="dense", embedder="openai", splitter="sentence")
model = build_model(cfg)
print(model.predict("This is a test. Another sentence here."))
