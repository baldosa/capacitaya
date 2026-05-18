import io
import logging
from pathlib import PurePath

from fastapi import UploadFile
from pypdf import PdfReader
from docx import Document


logger = logging.getLogger(__name__)

MAX_BYTES = 5 * 1024 * 1024  # 5 MB
MIN_CHARS = 50

_ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


class DocumentTooLargeError(Exception):
    pass


class UnsupportedDocumentError(Exception):
    pass


class EmptyDocumentError(Exception):
    pass


def extract_text(upload_file: UploadFile) -> str:
    filename = upload_file.filename or ""
    suffix = PurePath(filename).suffix.lower()
    if suffix not in _ALLOWED_EXTENSIONS:
        raise UnsupportedDocumentError(
            f"Extension '{suffix or 'desconocida'}' no soportada. "
            f"Aceptamos: {sorted(_ALLOWED_EXTENSIONS)}"
        )

    raw = upload_file.file.read()
    if len(raw) > MAX_BYTES:
        raise DocumentTooLargeError(
            f"El archivo pesa {len(raw)} bytes, supera el limite de {MAX_BYTES}."
        )

    if suffix == ".pdf":
        text = _parse_pdf(raw)
    elif suffix == ".docx":
        text = _parse_docx(raw)
    else:
        text = _parse_txt(raw)

    text = text.strip()
    if len(text) < MIN_CHARS:
        raise EmptyDocumentError(
            f"El documento '{filename}' tiene solo {len(text)} caracteres tras extraer texto. "
            f"Asegurate de subir un PDF con texto seleccionable (no escaneado) o un DOCX/TXT con contenido."
        )
    return text


def _parse_pdf(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as exc:
        logger.warning("Failed to parse PDF: %s", exc)
        raise EmptyDocumentError("No se pudo extraer texto del PDF.") from exc


def _parse_docx(data: bytes) -> str:
    try:
        document = Document(io.BytesIO(data))
        return "\n".join(para.text for para in document.paragraphs if para.text)
    except Exception as exc:
        logger.warning("Failed to parse DOCX: %s", exc)
        raise EmptyDocumentError("No se pudo extraer texto del DOCX.") from exc


def _parse_txt(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")
