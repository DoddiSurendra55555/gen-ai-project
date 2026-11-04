import fitz


MAX_FILE_SIZE_MB = 5


def extract_text_from_pdf(pdf_bytes):
    """
    Extract readable text from a PDF resume.

    Args:
        pdf_bytes: PDF file contents as bytes.

    Returns:
        Extracted resume text as a string.

    Raises:
        ValueError: If the PDF is invalid, too large,
                    empty, corrupted, or contains no
                    selectable text.
    """

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    if not isinstance(pdf_bytes, bytes):
        raise ValueError("Invalid file data. Please upload a PDF.")

    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

    if len(pdf_bytes) > max_size_bytes:
        raise ValueError(
            f"PDF size must not exceed {MAX_FILE_SIZE_MB} MB."
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError(
            "Invalid PDF file. Please upload a valid PDF document."
        )

    try:
        pdf_document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        if pdf_document.page_count == 0:
            pdf_document.close()
            raise ValueError("The PDF contains no pages.")

        extracted_pages = []

        for page in pdf_document:
            page_text = page.get_text("text")
            if page_text.strip():
                extracted_pages.append(page_text.strip())

        pdf_document.close()

        extracted_text = "\n\n".join(extracted_pages).strip()

        if not extracted_text:
            raise ValueError(
                "No readable text was found in this PDF. "
                "It may be a scanned resume. Please upload "
                "a PDF containing selectable text."
            )

        return extracted_text

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            "Unable to read this PDF. The file may be corrupted "
            "or password-protected. Please upload another PDF."
        ) from error