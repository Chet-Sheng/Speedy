from .base import BaseSplitter
from ..registry import register_splitter
from ..types import SplitterName

@register_splitter(SplitterName.sentence)
class SentenceSplitter(BaseSplitter):
    def split(self, text):
        return text.split(".") 