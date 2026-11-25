from pathlib import Path
from pypdf import PdfReader
from docx import Document

def load_text_document(file_path: str) -> str:
    """
    Load the contents of a plain-text merchant knowledge document.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    return path.read_text(encoding="utf-8")

def load_pdf_document(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text.strip())

    return "\n\n".join(pages)


def load_docx_document(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    document = Document(str(path))

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n\n".join(paragraphs)

def load_document(file_path: str) -> str:
    """
    Load a supported knowledge document and return
    its extracted text.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".txt":
        return load_text_document(file_path)

    if extension == ".pdf":
        return load_pdf_document(file_path)

    if extension == ".docx":
        return load_docx_document(file_path)

    raise ValueError(
        f"Unsupported document type: {extension}"
    )

def chunk_text(text: str, max_chars: int = 500) -> list[str]:
    """
    Split document text into chunks while preserving paragraph boundaries.
    """

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        candidate = (
            f"{current_chunk}\n\n{paragraph}"
            if current_chunk
            else paragraph
        )

        if len(candidate) <= max_chars:
            current_chunk = candidate

        else:
            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks