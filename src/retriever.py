from typing import List, Tuple
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from src.config import CHROMA_DIR, EMBEDDING_MODEL_NAME, GOOGLE_API_KEY, GROUNDING_THRESHOLD

def get_vectorstore() -> Chroma:
    """
    Loads the Chroma vector store from the persist directory.
    """
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        google_api_key=GOOGLE_API_KEY
    )
    
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )

def retrieve_context(query: str, threshold: float = None) -> Tuple[List[Document], float]:
    """
    Performs a similarity search on ChromaDB and filters results based on a threshold.
    
    Args:
        query: The user query string.
        threshold: Similarity threshold (0.0 to 1.0). Defaults to GROUNDING_THRESHOLD from config.
        
    Returns:
        A tuple containing:
        - A list of Document objects that passed the threshold.
        - The highest similarity score found.
    """
    if threshold is None:
        threshold = GROUNDING_THRESHOLD
        
    vectorstore = get_vectorstore()
    
    # search_with_score returns (Document, score)
    # Note: Chroma score is often distance, so lower might be better depending on the method.
    # However, for LangChain's vectorstore.similarity_search_with_relevance_scores, 
    # it normalizes it to a similarity score where higher is better (0 to 1).
    
    results = vectorstore.similarity_search_with_relevance_scores(query, k=5)
    
    filtered_docs = []
    max_score = 0.0
    
    for doc, score in results:
        if score > max_score:
            max_score = score
            
        if score >= threshold:
            filtered_docs.append(doc)
            
    return filtered_docs, max_score
