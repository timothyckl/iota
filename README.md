# IotaDB

## Installation

```
pip install iotadb
```

## Usage

```python
from iotadb import IotaDB, Document

docs = [
    Document(text="That is a happy dog"),
    Document(text="That is a very happy perso"),
    Document(text="Today is a sunny day")
]

db = IotaDB()
db.create_collection(name="my_collection", documents=docs)

results = db.search("That is a happy person", return_similarities=True)

for doc, score in results:
    print(f"Text: {doc.text}")
    print(f"similarity: {score:.3f}\n")
```
