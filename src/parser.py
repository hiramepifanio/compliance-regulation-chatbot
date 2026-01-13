import pymupdf4llm
from langchain_text_splitters import MarkdownHeaderTextSplitter
from bs4 import BeautifulSoup
import markdownify
from pathlib import Path
from typing import List, Dict, Any

def ingest_fmd_pdf(path: Path) -> List[Dict[str, Any]]:
    """
    Ingests FMD_Test_Corporation.pdf and returns its content as one chunk.
    """
    md_text = pymupdf4llm.to_markdown(str(path))
    return [{
        "content": md_text,
        "metadata": {
            "source": path.name,
            "section_title": "Full Document"
        }
    }]

def ingest_reach_pdf(path: Path) -> List[Dict[str, Any]]:
    """
    Ingests REACH_Certificate_of_Compliance_Test_Corporation.pdf and stores each section as a chunk.
    """
    md_text = pymupdf4llm.to_markdown(str(path))
    
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    split_docs = splitter.split_text(md_text)
    
    chunks = []
    for doc in split_docs:
        section_title = doc.metadata.get("Header 1") or doc.metadata.get("Header 2") or "General"
        chunks.append({
            "content": doc.page_content,
            "metadata": {
                "source": path.name,
                "section_title": section_title
            }
        })
    return chunks

def ingest_parts_html(path: Path) -> List[Dict[str, Any]]:
    """
    Ingests part_measurements_test_corporation.html and returns its content as one chunk.
    Extracted tables are preserved in Markdown format.
    """
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    # Convert HTML to Markdown, ensuring table integrity
    md_text = markdownify.markdownify(str(soup), heading_style="ATX")
    
    return [{
        "content": md_text,
        "metadata": {
            "source": path.name,
            "section_title": "Full Document"
        }
    }]
