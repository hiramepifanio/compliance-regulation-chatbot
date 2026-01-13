# Checking Ingested Data in ChromaDB

After running the ingestion pipeline (`python src/ingestion.py`), you might want to verify that the data was correctly stored in ChromaDB.

This guide provides different ways to inspect the database.

## 1. Using the Utility Script (Recommended)

A helper script is provided to quickly check the number of documents and see sample content.

### How to Run
From the project root:
```bash
python src/scripts/check_db.py
```

### What it Shows
- Total count of chunks/documents in the database.
- Metadata and content snippets for the first few documents.
- A list of unique source filenames present in the database.

## 2. Manual Inspection via Python Code

If you want more control, you can interact with the vector store directly in a Python script or notebook.

```python
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import CHROMA_DIR, GOOGLE_API_KEY, EMBEDDING_MODEL_NAME

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL_NAME,
    google_api_key=GOOGLE_API_KEY
)

# Load the vector store
vectorstore = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings
)

# Get all data
# Warning: Might be slow for very large databases
data = vectorstore.get()

print(f"Total IDs: {len(data['ids'])}")
print(f"First Metadata: {data['metadatas'][0]}")
```

## 3. Advanced Queries

You can also test similarity searches to see what the database returns for specific queries:

```python
query = "What are the rules for REACH compliance?"
docs = vectorstore.similarity_search(query, k=2)

for i, doc in enumerate(docs):
    print(f"\nResult {i+1}:")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Content: {doc.page_content[:200]}...")
```

## Database Location
The database is stored as files in the directory specified by `CHROMA_DIR` in `src/config.py` (default: `chroma_db/`). Do not manually edit these files.
