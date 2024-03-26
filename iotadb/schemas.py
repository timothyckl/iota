from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Union
from uuid import uuid4

from numpy import float32, ndarray
from sentence_transformers import SentenceTransformer


@dataclass
class EmbedModel:
    name: str
    model: SentenceTransformer = field(init=False)
    tokenizer: Callable = field(init=False)

    def __post_init__(self) -> None:
        self.model = SentenceTransformer(self.name)
        self.tokenizer = self.model[0].tokenizer

    def tokenize(self, input: str) -> List[str]:
        return self.tokenizer.tokenize(input)

    def encode(self, input: str) -> List[int]:
        return self.model.encode(input)


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

    def update(
        self,
        index: Union[str, int],
        text: str,
        embedding: List[ndarray[float32]],
        metadata: Dict[str, Union[str, int, List, Dict]],
    ) -> None:
        self.documents[index].text = text
        self.documents[index].metadata = metadata
        self.embeddings[index] = embedding

    def remove(self, index: Union[str, int]) -> None:
        del self.documents[index]
        del self.embeddings[index]

    def get_indices(
        self, target_ids: Union[List[Union[str, int]], str, int]
    ) -> Union[List[int], int]:
        if not isinstance(target_ids, (list, str, int)):
            raise ValueError("Invalid target id. Ensure target documents exists.")
        try:
            if isinstance(target_ids, list):
                return [
                    idx
                    for idx, doc in enumerate(self.documents)
                    if doc.id in target_ids
                ]
            else:
                return [
                    idx
                    for idx, doc in enumerate(self.documents)
                    if doc.id == target_ids
                ][0]
        except IndexError:
            raise IndexError("One or multiple target ids within  do not exist.")
