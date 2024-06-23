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

`pdf-word-extraction` repo uses [rye](https://rye.astral.sh/) as project manager. To run:

```
cd "$pdf-word-extraction-repo"
rye run protraitme -h
```


# Command Line

```
usage: protraitme [-h] --pdf_dir DIR --outdir DIR [--me STR] [--top_n INT] [--overwrite] [--nproc INT]

options:
  -h, --help     show this help message and exit
  --pdf_dir DIR  specify the path to directory of pdfs
  --outdir DIR   specify the path to output directory
  --me STR       specify a string to describe yourself [me]
  --top_n INT    specify the top # frequent word to keep
  --overwrite    specify to overwrite previous impression
  --nproc INT    specify the # of pdfs to process simultaneously [1]
```

## Example

```
rye run protraitme --pdf_dir "$pdf_dir" \
  --outdir "$outdir" \
  --me nanx
```
