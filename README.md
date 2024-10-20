# PDF to Text Converter

PDF to Text Converter is a powerful Python-based tool that transforms PDF files into high-quality markdown text. It utilizes OCR (Optical Character Recognition) and AI-powered text extraction to provide accurate and well-formatted output.

## Features

- Convert PDF files to markdown text
- OCR capability for extracting text from images
- AI-powered text extraction using Groq API
- Sophisticated processing pipeline including:
  - Initial markdown conversion
  - Feedback loop for refinement
  - Meta-reasoning for optimal output
- Support for both local and remote PDF files
- Ability to process specific pages from a PDF

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/tarekbadrsh/pdf_to_text.git
   cd pdf_to_text
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install system dependencies:

   For macOS (using Homebrew):
   ```
   brew install poppler
   brew install tesseract
   ```

   For Ubuntu (using apt-get):
   ```
   sudo apt-get update
   sudo apt-get install poppler-utils
   sudo apt-get install tesseract-ocr
   ```

   Note: For other operating systems, please install the equivalent packages for poppler and tesseract using your system's package manager.

4. Set up your environment variables:
   Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

To convert a PDF file to markdown text, run the following command:

```
python app.py
```

## Dependencies

This project relies on several Python libraries and system tools:

### Python Libraries
- aiofiles
- aiohttp
- pdf2image
- litellm
- aioshutil
- PyPDF2
- pytesseract
- Pillow (PIL)

For a complete list of Python dependencies and their versions, please refer to the `requirements.txt` file.

### System Tools
- poppler: Used for PDF manipulation and conversion
- tesseract: Optical Character Recognition (OCR) engine

Make sure to install these system tools as described in the installation section above.
