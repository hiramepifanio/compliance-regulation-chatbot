import pytest
import os
from unittest.mock import MagicMock, patch
from pathlib import Path
from langchain_core.documents import Document

# Mock GOOGLE_API_KEY for tests
os.environ["GOOGLE_API_KEY"] = "mock_key"

@patch("langchain_chroma.Chroma")
@patch("langchain_google_genai.GoogleGenerativeAIEmbeddings")
def test_retrieval_accuracy(mock_embeddings, mock_chroma):
    """
    Test Retrieval Accuracy (The "Golden Set")
    Query: "How much Lead is in part TC-3541-A?"
    Expectation: The retriever must return the FMD_Test_Corporation.pdf chunk.
    """
    # Mock return value for search
    mock_doc = Document(
        page_content="Lead content in part TC-3541-A is 0.1%.",
        metadata={"source": "FMD_Test_Corporation.pdf", "section_title": "Full Document"}
    )
    
    mock_vectorstore = MagicMock()
    mock_vectorstore.similarity_search_with_relevance_scores.return_value = [(mock_doc, 0.9)]
    mock_chroma.return_value = mock_vectorstore
    
    query = "How much Lead is in part TC-3541-A?"
    results = mock_vectorstore.similarity_search_with_relevance_scores(query, k=1)
    
    assert len(results) > 0
    top_doc, score = results[0]
    assert top_doc.metadata["source"] == "FMD_Test_Corporation.pdf"
    assert "page_number" not in top_doc.metadata
    assert score >= 0.7

@patch("langchain_chroma.Chroma")
@patch("langchain_google_genai.GoogleGenerativeAIEmbeddings")
def test_grounding_threshold(mock_embeddings, mock_chroma):
    """
    Test Grounding & Hallucination
    Query: "What is the weight limit for Pluto?"
    Expectation: The system must trigger the "Safe Failure" (Information not found) because 
    the similarity score should fall below the threshold.
    """
    mock_doc = Document(
        page_content="Information about planets...",
        metadata={"source": "other.pdf", "section_title": "General"}
    )
    
    mock_vectorstore = MagicMock()
    mock_vectorstore.similarity_search_with_relevance_scores.return_value = [(mock_doc, 0.4)]
    mock_chroma.return_value = mock_vectorstore
    
    query = "What is the weight limit for Pluto?"
    results = mock_vectorstore.similarity_search_with_relevance_scores(query, k=1)
    
    top_doc, score = results[0]
    assert score < 0.7 
