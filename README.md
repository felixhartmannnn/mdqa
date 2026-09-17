# mdqa

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
</p>

**mdqa** scans Markdown documents for heading structure issues, empty sections, and broken local anchor links from the command line.

## About

Markdown documents can drift into inconsistent heading orders, empty titled sections, and links to anchors that do not match any heading. `mdqa` reports these issues so they can be fixed before docs go stale.

## Features

- Heading gap detection: skipped heading levels are reported in document order.
- Unclosed heading gap detection: abrupt jumps downward are surfaced separately.
- Empty section detection: sections with no meaningful content are flagged.
- Local link validation: inline and reference-style `#anchor` links are checked against document headings.
- Normalization mode: rewrites headings to a stable spacing convention.

## Installation

```bash
python -m pip install -e .
```

## Usage

```bash
mdqa scan README.md
mdqa scan README.md --output report.mdqa.txt
mdqa normalize README.md --in-place
```

## Project Structure

```
mdqa/
  README.md
  pyproject.toml
  .gitignore
  mdqa/
    __init__.py
    models.py
    scanner.py
    normalizer.py
  mdqa_cli.py
  tests/
    test_mdqa.py
```

## Tags

markdown, lint, heading, anchor, link, cli, quality
