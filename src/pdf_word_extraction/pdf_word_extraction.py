from __future__ import annotations

from functools import partial
from multiprocessing import get_context
from pathlib import Path

import polars as pl

from .cli import parse_cmd
from .pathio import make_dir
from .texter import process_text


def get_pdfs(pdf_dir: Path) -> list[Path]:
    """Get all PDFs from give directory."""
    pdf_files = list(pdf_dir.glob("*.pdf"))
    # panic when no pdfs found
    if not pdf_files:
        raise ValueError("Failed to find any PDF files within {}", pdf_dir)
    return pdf_files


def get_first_impression(pdfs: list[Path], nproc: int = 1) -> pl.DataFrame:
    """Extract words from pdfs with frequency."""
    words_dfs: list(pl.DataFrame) = []
    # use spawn to make independent child processes
    with get_context("spawn").Pool(processes=nproc) as pool:
        for res in pool.imap_unordered(partial(process_text), pdfs):
            words_dfs.append(res)

    # merge all word freq table from eac PDF doc
    words_freq_df = pl.concat([df for df in words_dfs if not df.is_empty()])
    # group by and count words, and sorted by count in reverse order
    words_freq_df = (
        words_freq_df
        .filter(pl.col("count") > 1)
        .group_by("words")
        .agg(pl.col("count").sum())
        .sort(by="count", descending=True)
    )
    return words_freq_df


def main():
    cmd_parser = parse_cmd()
    args = cmd_parser.parse_args()

    # create output directory
    make_dir(args.outdir)
    out_first = args.outdir / f"{args.me}.txt"

    first_impression_df = pl.DataFrame()
    # Skip re-reading all PDFs if previously done so
    if not out_first.exists() or args.overwrite:
        pdfs = get_pdfs(args.pdf_dir)
        first_impression_df = get_first_impression(pdfs, args.nproc)
        first_impression_df.write_csv(out_first, separator="\t")
    else:
        first_impression_df = pl.read_csv(out_first, separator="\t")

    # Customize the words to remove
    words_to_remove = [
        "placeholder_word_to_remove1",
        "placeholder_word_to_remove2",
        "placeholder_word_to_remove3",
    ]
    first_impression_df = first_impression_df.filter(
        ~pl.col("words").is_in(words_to_remove)
    )

    # Customize the words to replace
    replacements = {
        "placeholder_word1": "replacement_word1",
        "placeholder_word2": "replacement_word2",
    }
    repl_df = pl.DataFrame(
        [{"words": x, "repl_words": y} for x, y in replacements.items()]
    )
    second_chance_df = first_impression_df.join(repl_df, on="words", how="left")
    # replace word(s) and re-count and sort and keep only top_n
    second_chance_df = (
        second_chance_df.with_columns(
            words=pl.when(pl.col("repl_words").is_not_null())
            .then(pl.col("repl_words"))
            .otherwise(pl.col("words"))
        )
        .drop("repl_words")
        .group_by("words")
        .agg(pl.col("count").sum())
        .sort(by="count", descending=True)
        .top_k(args.top_n, by="count")
    )
    out_second = args.outdir / "me.second.txt"
    second_chance_df.write_csv(out_second, separator="\t")
