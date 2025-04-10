# PDF to Text Converter

This project is a powerful Python-based tool designed to convert PDF files into high-quality markdown text. It combines **Optical Character Recognition (OCR)** for extracting text from images and **AI-powered processing** via the Groq API to deliver accurate and well-formatted output. Whether you're working with scanned documents, complex PDFs, or remote files, this converter provides a robust solution for transforming content into a usable markdown format.

## Features

- **PDF to Markdown Conversion**: Transforms PDF files into clean, structured markdown text.
- **OCR Support**: Extracts text from scanned documents or images embedded in PDFs using Tesseract.
- **AI-Powered Processing**: Leverages the Groq API for advanced text extraction and formatting.
- **Flexible Input**: Supports both local PDF files and remote URLs.
- **Page Selection**: Allows processing of specific pages from a PDF.
- **Sophisticated Pipeline**: Includes initial conversion, feedback loops for refinement, and meta-reasoning to optimize the final output.

## Installation

Follow these steps to set up the PDF to Text Converter on your system:

1. **Clone the Repository**  
   Clone the project from GitHub and navigate to the project directory:

   ```
   git clone https://github.com/tarekbadrsh/pdf_to_text.git
   cd pdf_to_text
   ```

2. **Install Python Dependencies**  
   Install the required Python libraries listed in `requirements.txt`:

   ```
   pip install -r requirements.txt
   ```

3. **Install System Dependencies**  
   The project relies on `poppler` and `tesseract` for PDF manipulation and OCR. Install them based on your operating system:

   - **macOS (using Homebrew)**:

     ```
     brew install poppler
     brew install tesseract
     ```

   - **Ubuntu (using apt-get)**:

     ```
     sudo apt-get update
     sudo apt-get install poppler-utils
     sudo apt-get install tesseract-ocr
     ```

   - **Other Operating Systems**: Use your package manager to install equivalent packages for `poppler` and `tesseract`.

4. **Set Up Environment Variables**  
   The project requires a Groq API key for AI processing. Create a `.env` file in the project root and add your key:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   To obtain a Groq API key, sign up at [Groq's website](https://www.groq.com) and follow their instructions.

## Usage

To convert a PDF file to markdown text, run the main script:

```
python app.py
```

By default, this processes the file located at `./file.pdf` and saves the markdown output in the `./data` directory. To process a different PDF:

1. Place your PDF file in the project root (e.g., `my_document.pdf`).
2. Update the `file_path` variable in `app.py` to point to your file (e.g., `"./my_document.pdf"`).
3. Run the script again.

The output will be saved as individual markdown files (one per page) in a subdirectory under `./data`, named after your input file (e.g., `./data/my_document/markdowns/page_1.md`).

For advanced usage, such as processing specific pages or integrating the tool into other projects, see the **Examples** section below.

## Examples

### Basic Usage

Convert a PDF named `example.pdf`:

1. Place `example.pdf` in the project root.
2. Edit `app.py` to set `file_path = "./example.pdf"`.
3. Run:

   ```
   python app.py
   ```

   Output will be saved in `./data/example/markdowns/`.

### Processing Specific Pages

To convert only pages 1, 3, and 5 from `example.pdf`:

```python
from processor.utils import create_selected_pages_pdf

selected_pages_pdf = create_selected_pages_pdf(
    original_pdf_path="example.pdf",
    select_pages=[1, 3, 5],
    save_directory="./data",
    suffix="_selected"
)
```

Then, update `file_path` in `app.py` to `selected_pages_pdf` and run `python app.py`.

### Integrating into Other Projects

Use the conversion functions in your own code. For example, to convert a PDF to images:

```python
from processor.pdf import convert_pdf_to_images

image_paths = convert_pdf_to_images("example.pdf", "./temp_images")
```

Explore `processor/pdf.py`, `processor/image.py`, and `processor/text.py` for more functions and details.

## Dependencies

### Python Libraries

- `aiofiles`: Asynchronous file operations
- `aiohttp`: Asynchronous HTTP requests
- `aioshutil`: Asynchronous shutil utilities
- `litellm`: Lightweight language model utilities
- `pdf2image`: PDF to image conversion
- `PyPDF2`: PDF manipulation
- `pytesseract`: OCR integration with Tesseract
- `Pillow (PIL)`: Image processing

For exact versions, see `requirements.txt`.

### System Tools

- **poppler**: PDF rendering and manipulation
- **tesseract**: OCR engine

Install these as described in the **Installation** section. An active internet connection is also required for Groq API calls.

## Troubleshooting

- **Missing Dependencies**: Verify `poppler` and `tesseract` are installed by running `pdfinfo` and `tesseract --version`. Install them if missing.
- **Groq API Issues**: Ensure your API key is correct in `.env` and that your Groq account is active.
- **Conversion Errors**: Protected PDFs or complex layouts may cause issues. Test with simpler PDFs or adjust DPI in `processor/pdf.py`.
- **Poor OCR Quality**: Increase DPI in `processor/pdf.py` (default is 300) for better image resolution.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a branch for your changes.
3. Submit a Pull Request or open an Issue on [GitHub](https://github.com/tarekbadrsh/pdf_to_text).

Please ensure your code follows the project's style and includes tests where applicable.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/tarekbadrsh/pdf_to_text).
