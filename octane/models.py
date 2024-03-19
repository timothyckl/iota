from typing import Dict, List, Optional, Union
from uuid import uuid4

from numpy import float32, ndarray
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: Union[str, int] = Field(default_factory=lambda: uuid4().hex)
    text: str
    metadata: Optional[Dict[str, Union[str, int, List, Dict]]] = None


class Embedding(BaseModel):
    vector: ndarray[float32]

    class Config:
        arbitrary_types_allowed = True


class Collection(BaseModel):
    name: str
    documents: Optional[List[Document]] = None
    embeddings: Optional[List[Embedding]] = None
