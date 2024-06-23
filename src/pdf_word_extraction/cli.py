from __future__ import annotations

import argparse

from .pathio import parse_path


def parse_cmd() -> argparse.ArgumentParser:
    """Parse command line input."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdf_dir",
        metavar="DIR",
        type=parse_path,
        required=True,
        help="specify the path to directory of pdfs",
    )
    parser.add_argument(
        "--outdir",
        metavar="DIR",
        type=parse_path,
        required=True,
        help="specify the path to output directory",
    )
    parser.add_argument(
        "--me",
        metavar="STR",
        type=str,
        default="me",
        help="specify a string to describe yourself [me]",
    )
    parser.add_argument(
        "--top_n",
        metavar="INT",
        type=int,
        default=250,
        help="specify the top # frequent word to keep",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="specify to overwrite previous impression",
    )
    parser.add_argument(
        "--nproc",
        metavar="INT",
        type=int,
        default=1,
        help="specify the # of pdfs to process simultaneously [1]",
    )

    return parser
