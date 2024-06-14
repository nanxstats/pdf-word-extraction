# PDF Word Extraction

This tool is designed to extract meaningful words from a collection of PDF
documents. The extracted words are processed and their frequencies are counted.
This frequency data can be used for various text analysis and visualization
tasks, such as generating word clouds or identifying common themes in the
document collection.

The tool leverages the modern text data toolchain in Python:

- pypdf: for reading PDFs.
- ftfy: for text cleaning.
- SpaCy: for natural language processing such as
  tokenization, lemmatization, and stop-word removal.

The tool also provides customizable features such as the ability to specify
words for removal or replacement.

## Workflow

Clone the repository:

```bash
git clone https://github.com/nanxstats/pdf-word-extraction.git
```

Create a [virtual environment](https://docs.python.org/3/library/venv.html)
inside the cloned repository, activate it, and install the required Python
packages into the virtual environment:

```bash
cd pdf-word-extraction
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Put the PDF files under `pdf/`, run

```
python3 pdf_word_extraction.py
```

If you use VS Code, open the project and select the recommended "venv"
Python interpreter. Edit the list of words to remove and replace in
`pdf_word_extraction.py`, save the file and run it again in terminal.
