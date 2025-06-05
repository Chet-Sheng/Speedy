from typing import Any, List, Literal, Optional, Tuple

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field



class RetrieverInput(BaseModel):
    query: str = Field(description="User query for information retrieval")

