# Retrieval Component Summary

The Retrieval and Inference part of the Regulation Chatbot has been implemented.

## Components Built

### 1. Retriever (`src/retriever.py`)
- **Functionality**: Loads the local ChromaDB and performs similarity searches.
- **Threshold Logic**: Implements a configurable grounding threshold (defaulting to `GROUNDING_THRESHOLD` from `config.py`) to filter out low-confidence results.
- **Scoring**: Uses LangChain's `similarity_search_with_relevance_scores` for normalized confidence values.

### 2. Inference Engine (`src/inference.py`)
- **Model**: Google Gemini (`gemini-3-flash-preview` by default).
- **Structured Output**: Uses Pydantic's `ComplianceResponse` schema and Gemini's JSON mode to ensure consistent responses.
- **Schema**:
    - `answer`: Natural language explanation.
    - `is_compliant`: Boolean status.
    - `confidence`: Maximum retrieval score.
    - `sources`: List of `{file, section}` objects.
- **Safe Failure**: Explicitly handles cases where no context is found by returning a "Safe Failure" response.

### 3. CLI Interface (`src/main.py`)
- **Usage**: `python3 src/main.py "Your query"` or `python3 src/main.py` for an interactive loop.
- **Verbose Mode**: `-v` flag to see confidence scores and document counts.

## Testing & Validation

### Automated Tests (`src/tests/test_rag.py`)
- **Unit Tests**: Verify retrieval logic and threshold filtering using mocked vector stores.
- **Inference Tests**: Verify Gemini integration and structured output parsing using mocked LLM responses.
- **Safe Failure Test**: Ensures the system correctly identifies when context is missing.

### Observation on Grounding Threshold
> [!WARNING]
> During end-to-end testing with `models/embedding-001`, similarity scores for highly relevant queries (including the "Golden Set" query) were found to range between **0.60 and 0.67**.
>
> With the strict **0.7 threshold** active, these queries currently trigger a "Safe Failure". We may need to:
> 1. Adjust the `GROUNDING_THRESHOLD` in `.env` or `src/config.py` to **0.6**.
> 2. Implement finer-grained chunking for the `FMD_Test_Corporation.pdf` file (currently a single large chunk).
