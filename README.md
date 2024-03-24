# IotaDB

## Installation

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
