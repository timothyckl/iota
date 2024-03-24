import os
from pickle import HIGHEST_PROTOCOL, dump, load
from typing import Dict, Iterable, List, Literal, Optional, Tuple, Union

from numpy import argsort, float32, vstack

from iotadb.metrics import OPSET_LOOKUP
from iotadb.schemas import Collection, Document, EmbedModel


class IotaDB:
    def __init__(
        self,
        metric: Literal["dot", "cosine", "euclidean"] = "cosine",
        embed_model: str = "all-mpnet-base-v2",
        persist: bool = False,
        persist_dir: Optional[str] = None,
    ) -> None:
        if metric not in OPSET_LOOKUP.keys():
            raise NotImplementedError("Algorithm not implemented.")
        if persist and persist_dir is None:
            raise ValueError("Path must be specified when persisting.")

        self.sim_func = OPSET_LOOKUP[metric]
        self.embed_model = EmbedModel(name=embed_model)
        self.tokenizer = self.embed_model.tokenizer
        self.persist = persist
        self.persist_dir = persist_dir
        self._collection = None

        os.makedirs(self.persist_dir, exist_ok=True)

    def create_collection(
        self,
        name: str,
        documents: Optional[List[Document]] = None,
    ) -> None:
        """
        creates a collection,
        this method can be called with or without documents,
        embeddings will be computed
        """
        documents = [] if documents is None else documents
        embeddings = (
            []
            if documents is None
            else [self._get_embedding(doc.text) for doc in documents]
        )

        self._collection = Collection(
            name=name, documents=documents, embeddings=embeddings
        )

        if self.persist:
            self._save_to_disk(f"{self._collection.name}.pickle")

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

        if self.persist:
            self._save_to_disk(f"{self._collection.name}.pickle")

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

        if self.persist:
            self._save_to_disk(f"{self._collection.name}.pickle")

    def remove_document(self, id: Union[str, int]) -> None:
        if self._collection is None:
            raise Exception("No existing collection. Create one first.")

        index = self._collection.get_indices(target_ids=id)
        self._collection.remove(index=index)

        if self.persist:
            self._save_to_disk(f"{self._collection.name}.pickle")

    def search(
        self,
        query: str,
        top_k: int = 10,
        return_similarities: bool = False,
    ) -> List[Union[Document, Tuple[Document, float32]]]:
        """Brute-force search"""
        if self._collection is None:
            raise Exception("No existing collection. Create one first.")
        
        query_vector = self._get_embedding(query)
        vector_store = vstack(self._collection.embeddings)

        similarities = self.sim_func(query_vector, vector_store)
        indices = argsort(similarities)[-top_k:][::-1]
        documents = self._collection.documents

        if return_similarities:
            return [(documents[idx], similarities[idx]) for idx in indices]

        return [documents[idx] for idx in indices]

    def _get_embedding(self, text: str) -> None:
        return self.embed_model.encode(text)

    def _save_to_disk(self, fname: str) -> None:
        with open(os.path.join(self.persist_dir, fname), "wb") as f:
            dump(self._collection, f, HIGHEST_PROTOCOL)
