import logging
import time

import fitz  # PyMuPDF
import pymupdf4llm  # higher-level library for LLM/RAG use cases
from fastapi import FastAPI, File, UploadFile

# Configure basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()


def extract_markdown_from_bytes(
    pdf_bytes: bytes, write_images: bool = False
) -> tuple[str, float]:
    """
    Synchronous function that opens a PDF from bytes and converts it to Markdown.
    Returns a tuple: (markdown_text, execution_time in seconds).
    """
    start_time = time.perf_counter()
    # Open the PDF directly from bytes
    doc = fitz.open("pdf", pdf_bytes)
    # Convert the Document to Markdown using pymupdf4llm
    md_text = pymupdf4llm.to_markdown(doc, write_images=write_images)
    doc.close()
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    logging.info(f"Extraction completed in {elapsed:.3f} seconds")
    return md_text, elapsed


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    # Read the uploaded file synchronously from the underlying file object
    pdf_bytes = file.file.read()
    md_text, exec_time = extract_markdown_from_bytes(pdf_bytes, write_images=True)
    return {"markdown": md_text, "execution_time": exec_time}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
