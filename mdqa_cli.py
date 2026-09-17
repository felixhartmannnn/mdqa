from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence, TextIO

from mdqa.scanner import scan_document
from mdqa.normalizer import normalize_headings


def _read_input(path: Optional[Path], stdin: TextIO) -> str:
    if path is None:
        return stdin.read()
    return path.read_text(encoding="utf-8")


def scan(args: argparse.Namespace) -> int:
    text = _read_input(args.input, sys.stdin)
    sections, issues = scan_document(text)
    lines: list[str] = []
    lines.append(f"# mdqa report: {args.input or '<stdin>'}\n")
    lines.append(f"sections: {len(sections)}\n")
    lines.append(f"issues: {len(issues)}\n\n")
    for issue in issues:
        lines.append(f"{issue.code} line {issue.lineno}: {issue.message}\n")
    report = "".join(lines)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)
    return 0 if not issues else 1


def normalize(args: argparse.Namespace) -> int:
    text = _read_input(args.input, sys.stdin)
    normalized = normalize_headings(text)
    if args.in_place:
        path = args.input
        if path is None:
            sys.stderr.write("--in-place requires an input file\n")
            return 2
        path.write_text(normalized, encoding="utf-8")
    else:
        sys.stdout.write(normalized)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mdqa",
        description="Scan and normalize Markdown document quality issues.",
    )
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Scan a Markdown document for issues.")
    scan_parser.add_argument(
        "--input",
        type=Path,
        help="Markdown file to analyze. Defaults to stdin.",
    )
    scan_parser.add_argument(
        "--output",
        type=Path,
        help="Write the report to this file. Defaults to stdout.",
    )
    scan_parser.set_defaults(func=scan)

    norm_parser = subparsers.add_parser("normalize", help="Normalize heading casing and spacing.")
    norm_parser.add_argument(
        "--input",
        type=Path,
        help="Markdown file to analyze. Defaults to stdin.",
    )
    norm_parser.add_argument(
        "--in-place",
        action="store_true",
        help="Rewrite the input file instead of writing to stdout.",
    )
    norm_parser.set_defaults(func=normalize)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)
