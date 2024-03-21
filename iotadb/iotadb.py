from typing import List, Optional

from sentence_transformers import SentenceTransformer

from iotadb.models import Collection, Document, Embedding
from iotadb.utils import ALGORITHM_LOOKUP


class IotaDB:
    def __init__(
        self,
        sim_func: str = "cosine_similarity",
        embed_model: str = "all-mpnet-base-v2",
    ) -> None:
        if sim_func not in ALGORITHM_LOOKUP.keys():
            raise ValueError("Invalid search algorithm specified.")

        self.sim_func = ALGORITHM_LOOKUP[sim_func]
        self.embed_model = SentenceTransformer(embed_model)
        self._collection = None

    def create_collection(
        self,
        name: str,
        documents: Optional[List[Document]] = None,
        persist: bool = False,
        path: Optional[str] = None,
    ) -> None:
        """
        creates a collection,
        this method can be called with or without documents,
        embeddings will be computed
        """
        if persist and path is None:
            raise ValueError("Path must be specified when persisting.")

        if documents is not None:
            embeddings = [
                Embedding(vector=self._get_embedding(doc.text)) for doc in documents
            ]

        else:
            documents = []
            embeddings = []

        self._collection = Collection(
            name=name, documents=documents, embeddings=embeddings
        )

        # serialize collection to path
        if persist:
            pass

    def get_collection(self, include_embedding: bool = False):
        if self._collection is None:
            raise Exception("No existing collection")

        return self._collection.__str__(include_embeddings=include_embedding)

    def add_documents(self, documents: List[Document]) -> None:
        if self._collection is None:
            raise Exception(
                "No collection exists. Create a collection before adding documents."
            )

    def _get_embedding(self, text: str):
        return self.embed_model.encode(text)
