import logging
from typing import List
from pdf2image import convert_from_path

class PDFConversionDefaultOptions:
    """Default options for converting PDFs to images"""

    DPI = 300
    FORMAT = "png"
    SIZE = (None, 1056)
    THREAD_COUNT = 4
    USE_PDFTOCAIRO = True


def convert_pdf_to_images(local_path: str, temp_dir: str) -> List[str]:
    """Converts a PDF file to a series of images in the temp_dir. Returns a list of image paths in page order."""
    options = {
        "pdf_path": local_path,
        "output_folder": temp_dir,
        "dpi": PDFConversionDefaultOptions.DPI,
        "fmt": PDFConversionDefaultOptions.FORMAT,
        "size": PDFConversionDefaultOptions.SIZE,
        "thread_count": PDFConversionDefaultOptions.THREAD_COUNT,
        "use_pdftocairo": PDFConversionDefaultOptions.USE_PDFTOCAIRO,
        "paths_only": True,
    }

    try:
        image_paths = convert_from_path(**options)
        return image_paths
    except Exception as err:
        logging.error(f"Error converting PDF to images: {err}")


