from importlib import import_module
import logging
import pkgutil
from typing import Dict, Iterable, Type
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


def auto_discover_modules(
    packages: Iterable[str] = [
        "dynamic_model_registry.embedders",
    ],
) -> None:
    """Import every sub-module in each package listed.

    Calling this populates all REGISTERY dictionaries as a side-effect.
    It is safe (and cheap) to call more than onces; Python caches imports.
    Args:
        packages (Iterable[str], optional): One or more dotted-path package names whose modules contains
            `register_*` decorators.
    """
    for pkg_name in packages:
        pkg = import_module(pkg_name)

        if not hasattr(pkg, "__path__"):
            raise ValueError(f"Package {pkg_name} is not a valid package.")

        # Walk the package tree, importing every module & sub-package.
        for _, module_name, _ispkg in pkgutil.walk_packages(
            pkg.__path__, prefix=pkg.__name__ + "."
        ):
            import_module(module_name)