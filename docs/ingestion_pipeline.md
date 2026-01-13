# Feature Summary: Ingestion & Parsing Pipeline

## Overview
The Ingestion & Parsing Pipeline is responsible for transforming raw regulatory documents (PDF and HTML) into a structured markdown format, chunking them appropriately, and storing them in a vector database (ChromaDB) for retrieval-augmented generation (RAG).

## Components

### 1. Parser (`src/parser.py`)
Provides specialized ingestion functions for each document type to ensure high fidelity and structural integrity:
- `ingest_fmd_pdf`: Handles `FMD_Test_Corporation.pdf`. Returns the document as a single atomic chunk.
- `ingest_reach_pdf`: Handles `REACH_Certificate_of_Compliance_Test_Corporation.pdf`. Uses `MarkdownHeaderTextSplitter` to create chunks based on H1 and H2 headers.
- `ingest_parts_html`: Handles `part_measurements_test_corporation.html`. Preserves tables using `markdownify` and returns the document as a single chunk.

### 2. Ingestion Orchestrator (`src/ingestion.py`)
- Iterates through the `data/` directory.
- Maps specific filenames to their corresponding parser functions.
- Initializes `GoogleGenerativeAIEmbeddings`.
- Populates/Updates a local `ChromaDB` instance in `chroma_db/`.

### 3. Markdown Verification Utility (`src/scripts/check_markdown.py`)
- A standalone script to preview how documents are being parsed into markdown.
- Runs without requiring a `GOOGLE_API_KEY` (using mocks) for quick local verification of parsing logic.

### 4. Test Suite (`src/tests/`)
- `test_units.py`: Unit tests for the parser functions to ensure correct chunking and metadata attribution (specifically `source` and `section_title`).
- `test_rag.py`: Integration tests (mocked) to verify retrieval accuracy and the enforcement of the 0.7 grounding threshold.

## Metadata Schema
Each chunk stored in the vector database contains:
- `source`: The original filename (e.g., `FMD_Test_Corporation.pdf`).
- `section_title`: The specific heading or "Full Document"/"General" indicator.
*Note: `page_number` was deliberately removed from the schema per project requirements.*

## Setup & Execution
- **Environment**: Requires Python 3.12+ and dependencies in `requirements.txt` (notably `pymupdf4llm`, `langchain-chroma`, `markdownify`).
- **Dependencies**: `pip install -r requirements.txt`.
- **Run Ingestion**: `source .venv/bin/activate && python3 src/ingestion.py`.
- **Verify Parsing**: `source .venv/bin/activate && python3 src/scripts/check_markdown.py`.
