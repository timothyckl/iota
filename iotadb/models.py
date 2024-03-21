from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from uuid import uuid4

from numpy import float32, ndarray


@dataclass
class Document:
    text: str
    metadata: Optional[Dict[str, Union[str, int, List, Dict]]] = None
    id: Union[str, int] = field(default_factory=lambda: uuid4().hex)


@dataclass
class Embedding:
    vector: ndarray[float32]


@dataclass
class Collection:
    name: str
    documents: Optional[List[Document]] = None
    embeddings: Optional[List[Embedding]] = None

    def __str__(self, include_embeddings: bool = False) -> str:
        embedding_repr = "None" if not include_embeddings else self.embeddings
        string = f"Collection(name={self.name}, documents={self.documents}, embeddings={embedding_repr})"
        return string
