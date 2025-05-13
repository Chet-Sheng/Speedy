from .base import BaseEmbedder
from ..registry import register_embedder
from ..types import EmbedderName

@register_embedder(EmbedderName.openai)
class OpenAIEmbedder(BaseEmbedder):
    def __init__(self, api_key: str, base_url: str = None):
        # NOTE: BaseEmbedder implemented a `from_config`` method
        # which really completes `EMBEDDER_REGISTRY as it no longer enforces same constructor signature
        self.api_key = api_key
        self.base_url = base_url

    def embed(self, text):
        return f"embedding:{text}" 
    
