from abc import ABC, abstractmethod
import inspect
from typing import Any, Mapping

class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, text: str):
        pass 

    @classmethod
    def from_config(cls, cfg: Mapping[str, Any]) -> "BaseEmbedder":
        """
        Build an instance of `cls` from an arbitrary mapping.

        The default implementation keeps only the kwargs that actually
        appear in the class' __init__ signature; everything else is ignored.
        """
        # NOTE: this really completes `EMBEDDER_REGISTRY as it no longer enforces same constructor signature
        sig = inspect.signature(cls.__init__)
        valid_names = sig.parameters.keys() - {"self"}
        kwargs = {k: v for k, v in cfg.items() if k in valid_names}
        return cls(**kwargs)