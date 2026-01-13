import os
import shutil
from pathlib import Path
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.parser import ingest_fmd_pdf, ingest_reach_pdf, ingest_parts_html
from src.config import DATA_DIR, CHROMA_DIR, GOOGLE_API_KEY, EMBEDDING_MODEL_NAME

def is_ingested() -> bool:
    """
    Checks if ChromaDB contains data by looking for the existance of the CHROMA_DIR.
    """
    return CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir())

def clear_database():
    """
    Deletes the ChromaDB directory.
    """
    if CHROMA_DIR.exists():
        print(f"Clearing database at {CHROMA_DIR}...")
        shutil.rmtree(CHROMA_DIR)
        print("Database cleared.")
    else:
        print("Database directory does not exist. Nothing to clear.")

def ingest_data(verbose: bool = True):
    """
    Orchestrates the ingestion of all files in the DATA_DIR into ChromaDB.
    Uses specific ingestion functions for each file type/name.
    """
    def vprint(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    if not DATA_DIR.exists():
        vprint(f"Data directory {DATA_DIR} does not exist.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        google_api_key=GOOGLE_API_KEY
    )

    all_docs = []

    for file_path in DATA_DIR.iterdir():
        if file_path.is_file():
            vprint(f"Processing {file_path.name}...")
            chunks = []
            
            if file_path.name == "FMD_Test_Corporation.pdf":
                chunks = ingest_fmd_pdf(file_path)
            elif file_path.name == "REACH_Certificate_of_Compliance_Test_Corporation.pdf":
                chunks = ingest_reach_pdf(file_path)
            elif file_path.name == "part_measurements_test_corporation.html":
                chunks = ingest_parts_html(file_path)
            else:
                vprint(f"Skipping unknown file: {file_path.name}")
                continue
            
            for chunk in chunks:
                all_docs.append(Document(
                    page_content=chunk["content"],
                    metadata=chunk["metadata"]
                ))

    if not all_docs:
        vprint("No documents found to ingest.")
        return

    vprint(f"Ingesting {len(all_docs)} chunks into ChromaDB at {CHROMA_DIR}...")
    
    # Initialize Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=all_docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )
    
    vprint("Ingestion complete.")

if __name__ == "__main__":
    ingest_data()
