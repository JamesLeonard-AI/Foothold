from pathlib import Path

from pypdf import PdfReader


def extract_text(pdf_path: str) -> str:
    """
    Read a PDF resume and return all text.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text