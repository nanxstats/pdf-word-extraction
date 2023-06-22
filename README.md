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

## Setup

You can install the latest versions of the required Python packages using pip:

```bash
pip install ftfy pypdf spacy
python3 -m spacy download en_core_web_sm
```

Alternatively, you can install all the dependencies at once with:

```bash
pip install -r requirements.txt
```
