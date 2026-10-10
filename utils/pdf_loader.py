from pathlib import Path

from pypdf import PdfReader


class PDFLoader:
    """
    Utility class for reading PDF resumes.
    """

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text as a single string.
        """

        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(
                f"File not found: {pdf_path}"
            )

        reader = PdfReader(pdf_file)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages).strip()