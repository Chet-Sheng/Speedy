from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ModelProvider(ABC):
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Return list of available model names for this provider."""
        pass
    
    @abstractmethod
    def chat_completion(self, messages: List[Dict[str, str]], model: str, **kwargs) -> str:
        """Generate a chat completion using the specified model."""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the provider."""
        pass 