import os
import re
from collections import defaultdict

import ftfy
from pypdf import PdfReader
import spacy


def get_pdf_files(directory):
    return [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")
    ]


def read_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf = PdfReader(file)
        text = ""
        for page_num in range(len(pdf.pages)):
            text += pdf.pages[page_num].extract_text()
    return text


def process_text(text):
    # Fix unicode issues, including ligatures
    text = ftfy.fix_text(text)

    # Load the NLP model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    word_freq = defaultdict(int)
    skip_next = False
    for i, token in enumerate(doc):
        # If this token is 'al.' and the previous one was 'et', skip it
        if skip_next:
            skip_next = False
            continue

        # Skip stop words, punctuation, whitespaces, and single characters
        if token.is_stop or token.is_punct or token.is_space or len(token.text) == 1:
            continue

        # Skip tokens that are numbers, floats or look like author initials
        if (
            token.text.isdigit()
            or re.match(r"^\d+\.?\d*$", token.text)
            or (token.text[:-1].isupper() and token.text.endswith("."))
        ):
            continue

        # Regularize the case but preserve proper nouns
        word = token.text if token.tag_ == "NNP" else token.text.lower()

        # Check for 'et al.' and skip both 'et' and 'al.'
        if word == "et" and i < len(doc) - 1 and doc[i + 1].text.lower() == "al":
            skip_next = True
            continue

        word_freq[word] += 1

    return word_freq


def process_pdfs(directory):
    pdf_files = get_pdf_files(directory)
    total_word_freq = defaultdict(int)
    for pdf_file in pdf_files:
        text = read_pdf(pdf_file)
        word_freq = process_text(text)

        for word, freq in word_freq.items():
            total_word_freq[word] += freq

    return total_word_freq


# Tools for removing or replacing words manually
def remove_specific_words(word_freq, words_to_remove):
    """Remove specific words from the word frequency count."""
    for word in words_to_remove:
        word_freq.pop(
            word, None
        )  # The second argument to 'pop' is a default in case 'word' is not found in the dict
    return word_freq


def replace_specific_words(word_freq, replacements):
    """
    Replace specific words in the word frequency count.

    replacements should be a dict mapping old words to new words.
    """
    for old_word, new_word in replacements.items():
        if old_word in word_freq:
            # If the new word is already in the dictionary, add the count from the old word
            if new_word in word_freq:
                word_freq[new_word] += word_freq[old_word]
            else:
                word_freq[new_word] = word_freq[old_word]
            # Remove the old word from the dictionary
            del word_freq[old_word]
    return word_freq


# Directory containing the PDF files
directory = "pdf/"
word_freq = process_pdfs(directory)

# Customize the words to remove
words_to_remove = [
    "placeholder_word_to_remove1",
    "placeholder_word_to_remove2",
    "placeholder_word_to_remove3",
]
word_freq = remove_specific_words(word_freq, words_to_remove)

# Customize the words to replace
replacements = {
    "placeholder_word1": "replacement_word1",
    "placeholder_word2": "replacement_word2",
}
word_freq = replace_specific_words(word_freq, replacements)

# Print most frequent words
top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:250]
for word, freq in top_words:
    print(f"{word}: {freq}")


def write_to_file(word_freq, filename, top_n=250):
    """Write the top N words and their frequencies to a file."""
    with open(filename, "w") as f:
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        for word, freq in sorted_words[:top_n]:
            f.write((word + " ") * freq)
            f.write("\n")


# Write to txt after processing and customization
write_to_file(word_freq, "top_words.txt")
