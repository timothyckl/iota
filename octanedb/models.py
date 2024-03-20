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

    def __str__(self, include_embeddings: bool = False) -> str:
        embedding_repr = "None" if not include_embeddings else self.embeddings
        string = f"Collection(documents={self.documents}, embeddings={embedding_repr})"
        return string
