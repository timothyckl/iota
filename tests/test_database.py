import numpy as np
import pytest

from iotadb.iotadb import (OPSET_LOOKUP, Collection, Document, EmbedModel,
                           IotaDB)


@pytest.mark.parametrize(
    "metric, embed_model, persist, persist_dir",
    [
        ("cosine", "all-mpnet-base-v2", False, None),
        ("cosine", "all-mpnet-base-v2", True, "data/"),
        ("dot", "all-mpnet-base-v2", False, None),
        ("dot", "all-mpnet-base-v2", True, "data/"),
        ("euclidean", "all-mpnet-base-v2", False, None),
        ("euclidean", "all-mpnet-base-v2", True, "data/"),
    ],
)
def test_database_init(metric, embed_model, persist, persist_dir):
    db = IotaDB(
        metric=metric, embed_model=embed_model, persist=persist, persist_dir=persist_dir
    )

    assert db.sim_func == OPSET_LOOKUP[metric]
    assert isinstance(db.embed_model, EmbedModel)
    assert db.persist == persist
    assert isinstance(db.persist, bool)
    assert db.persist_dir == persist_dir
    assert isinstance(db.persist_dir, str) or db.persist_dir is None


def test_create_collection(default_database, sample_documents):
    default_database.create_collection(
        name="test_collection", documents=sample_documents
    )

    assert isinstance(default_database.get_collection(), Collection)


# def test_load_collection():
#     pass


def test_get_document(default_database, sample_documents):
    default_database.create_collection(
        name="test_collection", documents=sample_documents
    )

    doc1 = default_database.get_documents(ids=[0])
    doc2 = default_database.get_documents(ids=[0], include_embeddings=True)

    assert isinstance(doc1, list)
    assert isinstance(doc1[0], Document)
    assert isinstance(doc2, list)
    assert isinstance(doc2[0], tuple)
    assert isinstance(doc2[0][0], Document)
    assert isinstance(doc2[0][1], np.ndarray)
    assert doc2[0][1].dtype == np.float32


def test_add_documents(default_database, sample_documents):
    default_database.create_collection(
        name="test_collection", documents=sample_documents
    )

    sample_doc_len = len(sample_documents)

    new_docs = [
        Document(id=5, text="The quick brown fox jumps over the lazy dog"),
        Document(id=6, text="The five boxing wizards jump quickly."),
    ]

    default_database.add_documents(documents=new_docs)
    collection = default_database.get_collection()

    assert len(collection.documents) == sample_doc_len + len(new_docs)


def test_update_document(default_database, sample_documents):
    default_database.create_collection(
        name="test_collection", documents=sample_documents
    )

    default_database.update_document(id=0, new_text="hello world")
    collection = default_database.get_collection()
    assert collection.documents[0].text == "hello world"


def test_remove_document(default_database, sample_documents):
    default_database.create_collection(
        name="test_collection", documents=sample_documents
    )

    sample_doc_len = len(sample_documents)
    default_database.remove_document(id=0)
    collection = default_database.get_collection()

    assert len(collection.documents) == sample_doc_len - 1


def test_search(default_database, sample_documents):
    default_database.create_collection(
        name="test_collection", documents=sample_documents
    )

    results1 = default_database.search(query="a dancing cat")
    results2 = default_database.search(query="a dancing cat", return_similarities=True)

    assert isinstance(results1, list)
    assert isinstance(results1[0], Document)
    assert isinstance(results2, list)
    assert isinstance(results2[0][0], Document)
    assert results2[0][1].dtype == np.float32


