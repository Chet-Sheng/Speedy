from typing import List, Dict
from openai import OpenAI
from .base import ModelProvider
from .config import PROVIDER_CONFIGS

class OpenAIProvider(ModelProvider):
    def __init__(self, api_key: str, base_url: str = None):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self._available_models = PROVIDER_CONFIGS["openai"]["models"]
    
    def get_available_models(self) -> List[str]:
        return self._available_models
    
    def chat_completion(self, messages: List[Dict[str, str]], model: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    @property
    def provider_name(self) -> str:
        return PROVIDER_CONFIGS["openai"]["name"] 