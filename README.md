# IotaDB

## Features

- Simple interface: Easy-to-use API for database operations.
- Lightweight implementation: Minimal resource utilization.
- Local embedding storage: Stores embeddings locally for fast and retrieval.
- Fast Indexing: Efficient embedding indexing for storage and retrieval.

## Use cases

- **Query with Natural Language**: Search for relevant documents using simple natural language queries.
- **Contextual Summarization**: Integrate documents into LLM contexts like GPT-3 for data-augmented tasks.
- **Similarity Search**: Find similar items/documents based on their embeddings.

## Installation

Install the package via PyPI:

```
pip install iotadb
```

## Usage

```python
from iotadb import IotaDB, Document

# Define a list of documents
docs = [
    Document(text="That is a happy dog"),
    Document(text="That is a very happy person"),
    Document(text="Today is a sunny day")
]

# Create a collection
db = IotaDB()
db.create_collection(name="my_collection", documents=docs)

# Query documents within your collection
results = db.search("That is a happy person", return_similarities=True)

for doc, score in results:
    print(f"Text: {doc.text}")
    print(f"similarity: {score:.3f}\n")
```

More examples can be found in the `/examples` directory.

## Contributing
