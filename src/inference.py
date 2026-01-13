from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from src.config import GOOGLE_API_KEY, LLM_MODEL_NAME

class ComplianceResponse(BaseModel):
    """
    Schema for structured compliance response.
    """
    answer: str = Field(description="Concise natural language response answering the user query.")
    is_compliant: Optional[bool] = Field(description="Explicit compliance status if mentioned in the text. True for compliant, False for non-compliant, None if unknown.")
    confidence: float = Field(description="The maximum similarity score from the vector search.")
    sources: List[Dict[str, str]] = Field(description="List of sources used, each containing 'file' and 'section'.")

SYSTEM_PROMPT = """You are a Lead AI Compliance Engineer. Your task is to answer queries based ONLY on the provided context.

Context:
{context}

Guidelines:
1. If the answer is not in the context, clearly state that the information was not found.
2. Be concise and professional.
3. Identify if the regulation indicates compliance (True) or non-compliance (False).
4. Extract the sources using the 'source' and 'section_title' metadata fields from the context.
5. If no context is provided, return a response indicating that the information was not found.
"""

def generate_answer(query: str, context_docs: List[Document], max_confidence: float) -> ComplianceResponse:
    """
    Generates a structured answer using Gemini based on retrieved context.
    
    Args:
        query: The user query.
        context_docs: List of retrieved documents.
        max_confidence: The maximum similarity score found during retrieval.
        
    Returns:
        A ComplianceResponse object.
    """
    
    if not context_docs:
        return ComplianceResponse(
            answer="Information not found. The query did not meet the required grounding threshold or no relevant documents were found.",
            is_compliant=None,
            confidence=max_confidence,
            sources=[]
        )

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
        response_mime_type="application/json",
    )
    
    # Prepare context string
    context_str = "\n\n".join([
        f"--- Document: {doc.metadata.get('source')} | Section: {doc.metadata.get('section_title')} ---\n{doc.page_content}"
        for doc in context_docs
    ])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{query}")
    ])
    
    # Create the chain with structured output
    structured_llm = llm.with_structured_output(ComplianceResponse)
    chain = prompt | structured_llm
    
    try:
        response = chain.invoke({"context": context_str, "query": query})
        # Override the confidence with our verified retrieval score
        response.confidence = max_confidence
        return response
    except Exception as e:
        # Fallback if parsing or generation fails
        return ComplianceResponse(
            answer=f"An error occurred during response generation: {str(e)}",
            is_compliant=None,
            confidence=max_confidence,
            sources=[]
        )
