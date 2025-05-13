from importlib import import_module
import logging
from typing import Dict, Type, Iterable
import pkgutil
from importlib import import_module

from .config import ModelConfig
from .types import ModelName, EmbedderName, SplitterName, RerankerName, FilterName

logger = logging.getLogger("model_builder")

MODEL_REGISTRY: Dict[str, Type] = {}
EMBEDDER_REGISTRY: Dict[str, Type] = {}
SPLITTER_REGISTRY: Dict[str, Type] = {}
RERANKER_REGISTRY: Dict[str, Type] = {}
FILTER_REGISTRY: Dict[str, Type] = {}

# alternative implementation to auto_discover_modules
def autodiscover(
        packages: Iterable[str] = ("dynamic_model_registry.models","dynamic_model_registry.splitters",)
    ) -> None:
    """
    Import every sub-module in each package listed.

    Parameters
    ----------
    packages : Iterable[str]
        One or more dotted-path package names whose modules contain
        `@register_*` decorators.

    Calling this *populates* all REGISTRY dictionaries as a side-effect.
    It is safe (and cheap) to call more than once; Python caches imports.
    """
    for pkg_name in packages:
        pkg = import_module(pkg_name)               # raises if the package is missing

        # Only packages (directories) have __path__.
        if not hasattr(pkg, "__path__"):
            raise ValueError(f"{pkg_name!r} is not a package")

        # Walk the package tree, importing every module & sub-package.
        # └─  (prefix ensures we get 'myproj.models.foo' not just 'foo')
        for _, mod_name, _ in pkgutil.walk_packages(pkg.__path__, prefix=pkg.__name__ + "."):
            import_module(mod_name)


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

