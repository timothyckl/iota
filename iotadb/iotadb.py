import os
from pickle import HIGHEST_PROTOCOL, dump, load
from typing import Dict, List, Literal, Optional, Union

from iotadb.schemas import Collection, Document, EmbedModel
from iotadb.utils import ALGORITHM_LOOKUP


class IotaDB:
    def __init__(
        self,
        metric: Literal["dot", "cosine", "euclidean"] = "cosine",
        embed_model: str = "all-mpnet-base-v2",
    ) -> None:
        if metric not in ALGORITHM_LOOKUP.keys():
            raise ValueError("Invalid search algorithm specified.")

        self.dist_func = ALGORITHM_LOOKUP[metric]
        self.embed_model = EmbedModel(name=embed_model)
        self._collection = None

    def create_collection(
        self,
        name: str,
        documents: Optional[List[Document]] = None,
        persist: bool = False,
        persist_dir: str = "",
    ) -> None:
        """
        creates a collection,
        this method can be called with or without documents,
        embeddings will be computed
        """
        if persist and persist_dir == "":
            raise ValueError("Path must be specified when persisting.")
        else:
            os.makedirs(persist_dir, exist_ok=True)

        documents = [] if documents is None else documents
        embeddings = (
            []
            if documents is None
            else [self._get_embedding(doc.text) for doc in documents]
        )

        self._collection = Collection(
            name=name, documents=documents, embeddings=embeddings
        )

        if persist:
            fname = f"{self._collection.name}.pickle"
            with open(os.path.join(persist_dir, fname), "wb") as f:
                dump(self._collection, f, HIGHEST_PROTOCOL)

    def load_collection(
        self,
    ) -> None:
        pass

    def get_collection(self, include_embedding: bool = False) -> None:
        if self._collection is None:
            raise Exception("No existing collection")

        return self._collection.__str__(include_embeddings=include_embedding)

    def add_documents(self, documents: List[Document]) -> None:
        if self._collection is None:
            raise Exception(
                "No collection exists. Create a collection before adding documents."
            )

        embeddings = [self._get_embedding(doc.text) for doc in documents]
        self._collection.add(documents=documents, embeddings=embeddings)

    def get_documents(self, ids: List[Union[str, int]]) -> List[Document]:
        pass

    def update_document(
        self,
        id: Union[str, int],
        text: str,
        metadata: Optional[Dict[str, Union[str, int, List, Dict]]] = None,
    ) -> None:
        pass

    def remove_document(self, id: Union[str, int]) -> None:
        pass

    def _get_embedding(self, text: str):
        return self.embed_model(text)
