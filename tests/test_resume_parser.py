import fitz
import pytest

from utils.resume_parser import extract_text_from_pdf


def create_test_pdf(text="Test resume content"):
    """Create a temporary PDF in memory for testing."""

    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        text
    )

    pdf_bytes = document.tobytes()

    document.close()

    return pdf_bytes


def test_extract_text_from_valid_pdf():
    pdf_bytes = create_test_pdf(
        "John Doe Python Developer"
    )

    extracted_text = extract_text_from_pdf(pdf_bytes)

    assert "John Doe" in extracted_text
    assert "Python Developer" in extracted_text


def test_extract_text_from_empty_file():
    with pytest.raises(ValueError, match="empty"):
        extract_text_from_pdf(b"")


def test_reject_invalid_pdf():
    invalid_bytes = b"This is not a PDF file"

    with pytest.raises(ValueError, match="Invalid PDF"):
        extract_text_from_pdf(invalid_bytes)


def test_reject_large_pdf():
    large_pdf = b"%PDF-" + (
        b"0" * (6 * 1024 * 1024)
    )

    with pytest.raises(ValueError, match="5 MB"):
        extract_text_from_pdf(large_pdf)


def test_reject_pdf_without_readable_text():
    document = fitz.open()
    document.new_page()

    pdf_bytes = document.tobytes()

    document.close()

    with pytest.raises(ValueError, match="No readable text"):
        extract_text_from_pdf(pdf_bytes)