from __future__ import annotations

import re
from typing import TYPE_CHECKING

import ftfy
import polars as pl
from pypdf import PdfReader
import spacy

if TYPE_CHECKING:
    from pathlib import Path


def read_pdf(pdf_file: Path) -> str:
    # with open(pdf_file, "rb") as fIN:
    pdf = PdfReader(pdf_file)
    if not pdf.pages:
        raise ValueError("Found zero page in the given PDF: {}", pdf_file)
    text = ""
    for page_num in range(len(pdf.pages)):
        text += pdf.pages[page_num].extract_text()
    return text


def process_text(pdf: Path) -> pl.DataFrame:
    print(f"Processing {pdf}")
    # Fix unicode issues, including ligatures
    text = ftfy.fix_text(read_pdf(pdf))

    # Load the NLP model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # word_freq = defaultdict(int)
    skip_next = False
    words = pl.Series("words", [], dtype=pl.String)
    for i, token in enumerate(doc):
        # If this token is 'al.' and the previous one was 'et', skip it
        if skip_next:
            skip_next = False
            continue

        # Skip stop words, punctuation, whitespaces, and single characters
        if token.is_stop or token.is_punct or token.is_space or len(token.text) == 1:
            continue

        if token.like_url or token.like_email or token.is_title:
            continue

        if token.pos_ in ["AUX", "ADP", "SYM", "NUM", "PROPN"]:
            continue

        # Skip tokens that are numbers, floats or look like author initials
        if (
            token.text.isdigit()
            or re.match(r"^\d+\.?\d*$", token.text)
            or (token.text[:-1].isupper() and token.text.endswith("."))
        ):
            continue

        if re.match(r"^[|.]", token.text):
            continue

        # Regularize the case but preserve proper nouns
        word = token.text if token.tag_ == "NNP" else token.text.lower()

        # plural nouns to singular
        word = token.lemma_ if token.tag_ in ["NNS", "NNPS"] else token.text

        # Check for 'et al.' and skip both 'et' and 'al.'
        if word == "et" and i < len(doc) - 1 and doc[i + 1].text.lower() == "al":
            skip_next = True
            continue

        words.append(pl.Series("word", [word]))

    words_df = words.value_counts()

    return words_df
