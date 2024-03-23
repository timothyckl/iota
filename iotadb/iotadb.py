import os
from pickle import HIGHEST_PROTOCOL, dump, load
from typing import Dict, Iterable, List, Literal, Optional, Tuple, Union

from numpy import argsort, vstack

from iotadb.schemas import Collection, Document, EmbedModel
from iotadb.utils import ALGORITHM_LOOKUP


class IotaDB:
    def __init__(
        self,
        metric: Literal["dot", "cosine", "euclidean"] = "cosine",
        embed_model: str = "all-mpnet-base-v2",
    ) -> None:
        if metric not in ALGORITHM_LOOKUP.keys():
            raise NotImplementedError("Algorithm not implemented.")

        self.dist_func = ALGORITHM_LOOKUP[metric]
        self.embed_model = EmbedModel(name=embed_model)
        self.tokenizer = self.embed_model.tokenizer
        self._collection = None

    def create_collection(
        self,
        name: str,
        documents: Optional[List[Document]] = None,
        persist: bool = False,
        persist_dir: Optional[str] = None,
    ) -> None:
        """
        creates a collection,
        this method can be called with or without documents,
        embeddings will be computed
        """
        if persist and persist_dir is None:
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

    def load_collection(self, file_path: str) -> None:
        with open(file_path, "rb") as f:
            self._collection = load(f)

    def get_collection(self, include_embedding: bool = False) -> None:
        if self._collection is None:
            raise Exception("No existing collection. Create one first.")

        return self._collection.__str__(include_embeddings=include_embedding)

    def add_documents(self, documents: List[Document]) -> None:
        if self._collection is None:
            raise Exception(
                "No collection exists. Create a collection before adding documents."
            )

        embeddings = [self._get_embedding(doc.text) for doc in documents]
        self._collection.add(documents=documents, embeddings=embeddings)

    def get_documents(
        self, ids: List[Union[str, int]], include_embeddings: bool = False
    ) -> Union[List[Document], Iterable[Tuple]]:
        if self._collection is None:
            raise Exception("No existing collection. Create one first.")

        indices = self._collection.get_indices(target_ids=ids)
        documents = [self._collection.documents[i] for i in indices]

        if include_embeddings:
            embeddings = [self._collection.embeddings[i] for i in indices]
            return zip(documents, embeddings)

        return documents

    def update_document(
        self,
        id: Union[str, int],
        new_text: str,
        new_metadata: Optional[Dict[str, Union[str, int, List, Dict]]] = None,
    ) -> None:
        if self._collection is None:
            raise Exception("No existing collection. Create one first.")

        index = self._collection.get_indices(target_ids=id)
        new_embedding = self._get_embedding(new_text)

        self._collection.update(
            index=index, text=new_text, embedding=new_embedding, metadata=new_metadata
        )

    def remove_document(self, id: Union[str, int]) -> None:
        if self._collection is None:
            raise Exception("No existing collection. Create one first.")

        index = self._collection.get_indices(target_ids=id)

        self._collection.remove(index=index)

    def search(
        self,
        query: str,
        top_k: int = 10,
        return_similarities: bool = False,
    ) -> List[Union[Document, Tuple[Document, float]]]:
        query_vector = self._get_embedding(query)
        vector_store = vstack(self._collection.embeddings)

        similarities = self.dist_func(query_vector, vector_store)
        indices = argsort(similarities)[-top_k:][::-1]
        documents = self._collection.documents

        if return_similarities:
            return [(documents[idx], similarities[idx]) for idx in indices]

        return [documents[idx] for idx in indices]

    def _get_embedding(self, text: str):
        return self.embed_model.encode(text)
