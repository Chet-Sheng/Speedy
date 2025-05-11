from .base import BaseEmbedder
from ..registry import register_embedder
from ..types import EmbedderName

@register_embedder(EmbedderName.openai)
class OpenAIEmbedder(BaseEmbedder):
    def embed(self, text):
        return f"embedding:{text}" 