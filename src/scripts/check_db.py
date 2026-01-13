import sys
from pathlib import Path

# Add the project root to sys.path to allow importing from src
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import CHROMA_DIR, GOOGLE_API_KEY, EMBEDDING_MODEL_NAME

def inspect_chroma():
    """
    Connects to the ChromaDB and prints summary information.
    """
    print(f"Connecting to ChromaDB at: {CHROMA_DIR}")
    
    if not CHROMA_DIR.exists():
        print("Error: ChromaDB directory does not exist. Run ingestion first.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        google_api_key=GOOGLE_API_KEY
    )

    vectorstore = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )

    # Get collection info
    data = vectorstore.get()
    
    num_docs = len(data['ids'])
    print(f"\nTotal documents in collection: {num_docs}")

    if num_docs > 0:
        print("\n--- Sample Documents (First 3) ---")
        for i in range(min(3, num_docs)):
            print(f"\nID: {data['ids'][i]}")
            print(f"Metadata: {data['metadatas'][i]}")
            # Truncate content for readability
            content = data['documents'][i]
            sample_content = (content[:200] + '...') if len(content) > 200 else content
            print(f"Content: {sample_content}")
            print("-" * 30)
            
        # Example of unique sources
        sources = set(m.get('source', 'Unknown') for m in data['metadatas'])
        print(f"\nUnique sources found: {', '.join(sources)}")
    else:
        print("The collection is empty.")

if __name__ == "__main__":
    inspect_chroma()
