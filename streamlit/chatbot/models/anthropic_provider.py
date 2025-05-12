from typing import List, Dict
import anthropic
from .base import ModelProvider

class AnthropicProvider(ModelProvider):
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self._available_models = [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ]
    
    def get_available_models(self) -> List[str]:
        return self._available_models
    
    def chat_completion(self, messages: List[Dict[str, str]], model: str, **kwargs) -> str:
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "user":
                anthropic_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                anthropic_messages.append({"role": "assistant", "content": msg["content"]})
        
        response = self.client.messages.create(
            model=model,
            messages=anthropic_messages,
            **kwargs
        )
        return response.content[0].text
    
    @property
    def provider_name(self) -> str:
        return "anthropic" 