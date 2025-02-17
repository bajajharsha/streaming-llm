import asyncio
import time

import fitz  # PyMuPDF
import pymupdf4llm  # higher-level library for LLM/RAG use cases
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


def extract_markdown_from_bytes(pdf_bytes: bytes, write_images: bool = False) -> str:
    """
    Synchronous function that opens a PDF from bytes and converts it to Markdown.
    Instead of a filename, we create a Document from the bytes.
    """
    # Open the PDF directly from bytes; "pdf" tells fitz the stream is a PDF.
    doc = fitz.open("pdf", pdf_bytes)
    # Pass the Document to pymupdf4llm's to_markdown.
    md_text = pymupdf4llm.to_markdown(doc, write_images=write_images)
    doc.close()
    return md_text


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Read file contents as bytes
    start_time = time.perf_counter()
    pdf_bytes = await file.read()
    loop = asyncio.get_running_loop()
    # Run the blocking extraction in a thread, passing pdf_bytes directly
    md_text = await loop.run_in_executor(
        None, extract_markdown_from_bytes, pdf_bytes, False
    )
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(elapsed)
    return {"markdown": md_text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
