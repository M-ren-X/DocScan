# DocScan

DocScan is a document processing desktop application built using PyQt5 for the UI. It supports document classification and metadata extraction for identity documents
and receipts/invoices, with extensibility for additional document types and metadata customization.

## Features

- Drag and drop or choose documents using the file dialog.
- Document classification using GEMMA 7b-it through the Hugging Face Inferece API.
- Metadata extraction using GEMMA 2b-it through the Hugging Face Inference API.
- Extensible architecture for adding new document types and customizing metadata extraction.


## Installation

1. Clone the repository:
    git clone https://github.com/M-ren-X/DocScan.git
    cd DocScan

3. Install dependencies:
    pip install -r requirements.txt


## Usage

4. Usage:
    First of all add your API key from Hugging Face to the "headers" variable in main.py after creating an account.
    Add / Change whatever document types or meta-data you want extracted in the code.
    Run using: python main.py

6. How to use:
    Drag and drop a document onto the application or use the file dialog to select a document.
    The document will be processed through the OCR model (docTR) to extract text.
    Extracted text is classified using GEMMA 7b-it for document type.
    Metadata fields are populated using GEMMA 2b-it based on extracted text.
    Customize document types and metadata extraction by extending the codebase.

7. Contributing:
    Contributions are welcome! If you want to contribute to DocScan, please fork the repository and submit a pull request.
    You can also report issues or suggest improvements by opening an issue.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
