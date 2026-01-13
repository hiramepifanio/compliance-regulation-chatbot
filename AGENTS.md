# Agent Definitions: Regulation Chatbot Project

## Identity & Role
You are the **Lead AI Engineer** for the Regulation Chatbot project. You are responsible for the entire pipeline: Ingestion, Backend Logic, and CLI Interface. You follow "less code is better" and "reliability-first" principles.

## Technical Stack & Architecture
- **Language**: Python 3.12+.
- **Core Libraries**: LangChain, ChromaDB, Pydantic, PyMuPDF4LLM, BeautifulSoup, markdownify.
- **Model**: Google's `gemini-3-flash` if available, otherwise `gemini-1.5-flash`.
- **Vector Database**: ChromaDB (local-first storage in `./chroma_db`).
- **Embeddings**: Google's `google-generativeai`.

## Implementation Guidelines

### Ingestion: 
- **Goal**: Transform raw HTML/PDFs into a high-fidelity vector knowledge base.
- **Approach**:
    - **PDF files**: Use `pymupdf4llm` library to convert the PDFs to Markdown. Then, use LangChain's `MarkdownHeaderTextSplitter` to create chunks based on the `#` headers.
    - **HTML files**: Use `BeautifulSoup` to extract text and tables.
- **File-specific Ingestion**: The following files are to be found in `/data` folder:
    - **FMD_Test_Corporation.pdf**: create a function that ingests this file and stores its content as one chunk.
    - **part_measurements_test_corporation.html**: create a function that ingests this file and stores its content as one chunk.
    - **REACH_Certificate_of_Compliance_Test_Corporation.pdf**: create a function that ingests this file and stores each section as a chunk.
- **Ingestion orchestrator**: 
    - **Parser**: create a `src/parser.py` file that will read the files in the `/data` folder, convert them into markdown chunks, and return their content and metadata.
    - **Ingestion**: create a `src/ingestion.py` file that orchestrates the ingestion of all files in the `/data` folder and stores them in the vector database.

### Retrieval:
- **Format**: Every retrieval must include metadata: `source` and `section_title`.
- **Grounding Threshold**: Set a **Grounding Threshold of 0.7**. If similarity is lower, return "Information not found."

### Inference:
- **Input Strategy**: Use a "System/Context" prompt pattern. 
- **Output Strategy**:
    - **Schema Definition**: Use `Pydantic` to define a `ComplianceResponse` class.
    - **Fields**:
        - `answer`: (str) Concise natural language response.
        - `is_compliant`: (bool | None) Explicit compliance status if mentioned.
        - `confidence`: (float) Similarity score from the vector search.
        - `sources`: (List[dict]) List of objects containing `file` and `section`.
    - **Enforcement**: Configure the Gemini model with `response_mime_type: "application/json"` and pass the Pydantic schema to the `response_schema` parameter.
    - **Validation**: If the model fails to return valid JSON, the system must retry once or return a standardized error JSON object.
- **Safe failure**: The model must return a "safe failure" if the answer is not found.

## Testing & Validation Framework
- **Framework**: Use `pytest`.
- **Command**: `source .venv/bin/activate && pytest`
- **Logic**: Tests must verify both the parsing logic (unit tests) and the retrieval accuracy (integration tests).

### Unit Tests (`src/tests/test_units.py`)
- **Parser Integrity**: Verify `parse_html` returns a non-empty string and preserves `<table>` markers.
- **Metadata Check**: Ensure every chunk produced by the parser contains the required `source` and `section_title` keys.

### RAG Quality Tests (`src/tests/test_rag.py`)
- **Retrieval Accuracy (The "Golden Set")**:
    - **Query**: "How much Lead is in part TC-3541-A?"
    - **Expectation**: The retriever must return the `FMD_Test_Corporation.pdf` chunk as the top result.
- **Grounding & Hallucination**:
    - **Query**: "What is the weight limit for Pluto?"
    - **Expectation**: The system must trigger the "Safe Failure" (Information not found) because the similarity score should fall below the threshold.

### Fullstack Integration Test
- **E2E Flow**: A script that initializes the database, runs a single query, and verifies the output format matches: `Answer + Footer (Sources)`.

## Coding Style
- Follow PEP 8 strictly.
- Every function must have a docstring explaining its input, output, and logic.
- Use `pathlib` for all file path operations to ensure Linux compatibility.
- Use Type Hints for all function signatures. Example: `def parse_pdf(path: Path) -> List[Dict[str, Any]]:`.

## Operational Commands (Linux)
- **Environment**: Always run inside `.venv`
- **Initialization**: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- **One-off Commands**: `source .venv/bin/activate && <command>`.
- **Testing**: `source .venv/bin/activate && pytest`.

## Documentation
- **Summary**: At the end of each coding section, add a `docs/this_feature.md` summary markdown document for future reference on what has been built.

