from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Union
from uuid import uuid4

from numpy import float32, ndarray
from sentence_transformers import SentenceTransformer


@dataclass
class EmbedModel:
    name: str
    func: Callable = field(init=False)

    def __post_init__(self) -> None:
        self.func = SentenceTransformer(self.name)

    def __call__(self, input: str) -> None:
        return self.func.encode(input)


@dataclass
class Document:
    text: str
    metadata: Optional[Dict[str, Union[str, int, List, Dict]]] = None
    id: Union[str, int] = field(default_factory=lambda: uuid4().hex)


@dataclass
class Collection:
    name: str
    documents: Optional[List[Document]] = None
    embeddings: Optional[List[ndarray[float32]]] = None

    def add(
        self, documents: List[Document], embeddings: List[ndarray[float32]]
    ) -> None:
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)

    def __str__(self, include_embeddings: bool = False) -> str:
        embedding_repr = "None" if not include_embeddings else self.embeddings
        string = f"Collection(name={self.name}, documents={self.documents}, embeddings={embedding_repr})"
        return string
