import pytest
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document
from src.retriever import retrieve_context
from src.inference import generate_answer, ComplianceResponse

@patch("src.retriever.get_vectorstore")
def test_retrieval_accuracy_unit(mock_get_vs):
    """
    Test Retrieval Accuracy (The "Golden Set") logic using mocked vectorstore.
    Query: "How much Lead is in part TC-3541-A?"
    Expectation: The retriever must return the FMD_Test_Corporation.pdf chunk.
    """
    mock_doc = Document(
        page_content="Lead content in part TC-3541-A is 0.1%.",
        metadata={"source": "FMD_Test_Corporation.pdf", "section_title": "Full Document"}
    )
    
    mock_vectorstore = MagicMock()
    mock_vectorstore.similarity_search_with_relevance_scores.return_value = [(mock_doc, 0.9)]
    mock_get_vs.return_value = mock_vectorstore
    
    query = "How much Lead is in part TC-3541-A?"
    docs, max_score = retrieve_context(query)
    
    assert len(docs) == 1
    assert docs[0].metadata["source"] == "FMD_Test_Corporation.pdf"
    assert max_score >= 0.7

@patch("src.retriever.get_vectorstore")
def test_grounding_threshold_unit(mock_get_vs):
    """
    Test Grounding & Hallucination logic using mocked vectorstore.
    Query: "What is the weight limit for Pluto?"
    Expectation: Return empty docs list if score < threshold.
    """
    mock_doc = Document(
        page_content="Information about planets...",
        metadata={"source": "other.pdf", "section_title": "General"}
    )
    
    mock_vectorstore = MagicMock()
    # Below the 0.7 default threshold
    mock_vectorstore.similarity_search_with_relevance_scores.return_value = [(mock_doc, 0.4)]
    mock_get_vs.return_value = mock_vectorstore
    
    query = "What is the weight limit for Pluto?"
    docs, max_score = retrieve_context(query)
    
    assert len(docs) == 0
    assert max_score == 0.4

def test_inference_safe_failure():
    """
    Test that generate_answer handles empty context as a safe failure.
    """
    query = "What is the weight limit for Pluto?"
    response = generate_answer(query, [], 0.4)
    
    assert "Information not found" in response.answer
    assert response.is_compliant is None
    assert response.confidence == 0.4
    assert len(response.sources) == 0

@patch("src.inference.ChatPromptTemplate.from_messages")
@patch("src.inference.ChatGoogleGenerativeAI")
def test_inference_success(mock_llm_class, mock_prompt_class):
    """
    Test successful inference with mocked Gemini response.
    """
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_prompt = MagicMock()
    
    # Mocking the response from the structured LLM
    mock_response = ComplianceResponse(
        answer="Part TC-3541-A contains 0.1% Lead.",
        is_compliant=True,
        confidence=0.9,
        sources=[{"file": "FMD_Test_Corporation.pdf", "section": "Full Document"}]
    )
    
    # Mock prompt | structured_llm
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = mock_response
    
    mock_prompt.__or__.return_value = mock_chain
    mock_prompt_class.return_value = mock_prompt
    
    mock_llm.with_structured_output.return_value = mock_structured_llm
    mock_llm_class.return_value = mock_llm
    
    query = "How much Lead is in part TC-3541-A?"
    context = [Document(page_content="Lead: 0.1%", metadata={"source": "FMD.pdf", "section_title": "All"})]
    
    response = generate_answer(query, context, 0.9)
    
    assert response.answer == "Part TC-3541-A contains 0.1% Lead."
    assert response.confidence == 0.9
    assert response.is_compliant is True
