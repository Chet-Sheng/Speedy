import logging
from typing import Dict, Type
from .config import ModelConfig
from .types import ModelName, EmbedderName, SplitterName, RerankerName, FilterName

logger = logging.getLogger("model_builder")

MODEL_REGISTRY: Dict[str, Type] = {}
EMBEDDER_REGISTRY: Dict[str, Type] = {}
SPLITTER_REGISTRY: Dict[str, Type] = {}
RERANKER_REGISTRY: Dict[str, Type] = {}
FILTER_REGISTRY: Dict[str, Type] = {}

def register_model(name: ModelName):
    def decorator(cls):
        MODEL_REGISTRY[name.value] = cls
        return cls
    return decorator

def register_embedder(name: EmbedderName):
    def decorator(cls):
        EMBEDDER_REGISTRY[name.value] = cls
        return cls
    return decorator

def register_splitter(name: SplitterName):
    def decorator(cls):
        SPLITTER_REGISTRY[name.value] = cls
        return cls
    return decorator

def register_reranker(name: RerankerName):
    def decorator(cls):
        RERANKER_REGISTRY[name.value] = cls
        return cls
    return decorator

def register_filter(name: FilterName):
    def decorator(cls):
        FILTER_REGISTRY[name.value] = cls
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