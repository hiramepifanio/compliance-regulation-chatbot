import pytest
import os
from pathlib import Path

# Mock GOOGLE_API_KEY for tests that don't need it
os.environ["GOOGLE_API_KEY"] = "mock_key"

from src.parser import ingest_fmd_pdf, ingest_reach_pdf, ingest_parts_html

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def test_ingest_fmd_pdf():
    fmd_path = DATA_DIR / "FMD_Test_Corporation.pdf"
    chunks = ingest_fmd_pdf(fmd_path)
    assert len(chunks) == 1
    assert chunks[0]["metadata"]["source"] == "FMD_Test_Corporation.pdf"
    assert "content" in chunks[0]
    assert len(chunks[0]["content"]) > 0

def test_ingest_reach_pdf():
    reach_path = DATA_DIR / "REACH_Certificate_of_Compliance_Test_Corporation.pdf"
    chunks = ingest_reach_pdf(reach_path)
    assert len(chunks) > 1
    for chunk in chunks:
        assert "source" in chunk["metadata"]
        assert "section_title" in chunk["metadata"]

def test_ingest_parts_html():
    html_path = DATA_DIR / "part_measurements_test_corporation.html"
    chunks = ingest_parts_html(html_path)
    assert len(chunks) == 1
    assert "<table>" in chunks[0]["content"].lower() or "| " in chunks[0]["content"] # markdown conversion
    assert chunks[0]["metadata"]["source"] == "part_measurements_test_corporation.html"
