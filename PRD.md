# PRD: Compliance Regulation Chatbot

## Overview
A CLI-based AI tool that allows users to query specific regulation documents (1 HTML, 2 PDFs).

## Target Requirements
- **Input**: Natural language questions from users.
- **Output**: Grounded answers + clear source attribution.
- **Tech Stack**: Python 3.12+, LangChain, Gemini 3 Flash (`gemini-3-flash-preview`), ChromaDB.

## User Flows
1. **Startup**: System pre-indexes documents in the `/data` folder using Structural Chunking.
2. **Querying**: User asks "How many parts contain substance bar?"
3. **Response**: 
   - [Accurate Answer Text]
   - Source: [PDF/HTML Name], Section: [Y]

## Compliance-Specific Requirements
- **Strict Grounding**: The system must verify the answer exists in the retrieved context. If the similarity score is below a threshold (0.7), the bot must respond with a "Safe Failure" message.
- **Source Attribution**: Every response must include a footer with specific metadata (Filename, Section).
- **Data Integrity**: 
    - **HTML Tables**: Ingestion must handle HTML tables without fragmenting row-level relationships.
    - **PDF Tables**: Must be extracted using structural analysis to preserve row/column context.
    - **Representation**: Tables must be stored in the vector database as Markdown strings to maintain readability for the LLM during retrieval.
    
## Acceptance Criteria
- [ ] Successfully parses HTML tablesRoHS (/lREACH imit tables).
- [ ] Correctly identifies headings in PDFs.
- [ ] Operates via CLI with a 12-Factor App config (.env).
- [ ] Zero tolerance for hallucinations; "Information not found" is the default for low-confidence queries.