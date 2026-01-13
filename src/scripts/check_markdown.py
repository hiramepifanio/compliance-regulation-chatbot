import os
from pathlib import Path

# Mock GOOGLE_API_KEY for scripts that don't need it
os.environ["GOOGLE_API_KEY"] = "mock_key"

from src.parser import ingest_fmd_pdf, ingest_reach_pdf, ingest_parts_html
from src.config import DATA_DIR

def main():
    """
    Reads files in DATA_DIR, transforms them to Markdown using specialized parsers,
    and prints the resulting chunks to the console.
    """
    if not DATA_DIR.exists():
        print(f"Data directory {DATA_DIR} does not exist.")
        return

    print(f"--- Checking Markdown Conversion for files in {DATA_DIR} ---\n")

    for file_path in DATA_DIR.iterdir():
        if file_path.is_file():
            print(f"=== File: {file_path.name} ===")
            chunks = []
            
            try:
                if file_path.name == "FMD_Test_Corporation.pdf":
                    chunks = ingest_fmd_pdf(file_path)
                elif file_path.name == "REACH_Certificate_of_Compliance_Test_Corporation.pdf":
                    chunks = ingest_reach_pdf(file_path)
                elif file_path.name == "part_measurements_test_corporation.html":
                    chunks = ingest_parts_html(file_path)
                else:
                    # Logic for unknown files could be added here if needed
                    continue
                
                for i, chunk in enumerate(chunks):
                    print(f"--- Chunk {i+1} (Section: {chunk['metadata'].get('section_title')}) ---")
                    print(chunk['content'])
                    print("-" * 40)
                print("\n")
                
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}\n")

if __name__ == "__main__":
    main()