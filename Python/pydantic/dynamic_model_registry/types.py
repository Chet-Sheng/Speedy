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