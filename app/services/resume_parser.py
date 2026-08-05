from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text(file_path: str) -> str:
    """
    Extract text from a supported resume file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return _extract_pdf_text(path)

    if extension == ".docx":
        return _extract_docx_text(path)

    raise ValueError(
        f"Unsupported resume type: {extension}. "
        "Foothold currently supports PDF and DOCX files."
    )


def _extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    page_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            page_text.append(text)

    return "\n".join(page_text).strip()


def _extract_docx_text(path: Path) -> str:
    document = Document(str(path))
    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()