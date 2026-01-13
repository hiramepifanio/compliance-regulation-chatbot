import sys
import argparse
from typing import Optional
from src.retriever import retrieve_context
from src.inference import generate_answer, ComplianceResponse

def run_query(query: str, verbose: bool = False):
    """
    Orchestrates the RAG flow for a single query.
    """
    if verbose:
        print(f"\nUser Query: {query}")
        print("Retrieving context...")
        
    context_docs, max_confidence = retrieve_context(query)
    
    if verbose:
        print(f"Max Confidence: {max_confidence:.4f}")
        print(f"Documents Retrieved: {len(context_docs)}")
    
    response: ComplianceResponse = generate_answer(query, context_docs, max_confidence)
    
    print("\n" + "="*50)
    print(f"ANSWER: {response.answer}")
    
    if response.is_compliant is not None:
        status = "COMPLIANT" if response.is_compliant else "NON-COMPLIANT"
        print(f"STATUS: {status}")
        
    print(f"CONFIDENCE: {response.confidence:.4f}")
    
    if response.sources:
        print("\nSOURCES:")
        for idx, src in enumerate(response.sources, 1):
            print(f"  {idx}. {src['file']} (Section: {src['section']})")
    print("="*50 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Regulation Compliance Chatbot")
    parser.add_argument("query", nargs="?", help="The natural language query to ask the chatbot.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    
    args = parser.parse_args()
    
    if args.query:
        run_query(args.query, args.verbose)
    else:
        print("Welcome to the Regulation Compliance Chatbot CLI.")
        print("Type 'exit' or 'quit' to stop.")
        while True:
            try:
                query = input("\nQuery > ").strip()
                if query.lower() in ["exit", "quit"]:
                    break
                if not query:
                    continue
                run_query(query, args.verbose)
            except KeyboardInterrupt:
                break
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
