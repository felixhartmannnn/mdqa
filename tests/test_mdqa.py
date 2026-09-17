from pathlib import Path

from mdqa.normalizer import normalize_headings
from mdqa.scanner import scan_document
from mdqa_cli import main


def test_scan_reports_heading_gap() -> None:
    text = "# Alpha\n### Bravo\n"
    _, issues = scan_document(text)
    codes = [issue.code for issue in issues]
    assert "MQ001" in codes


def test_scan_detects_broken_local_link() -> None:
    text = "# Alpha\n[missing](#missing)\n"
    _, issues = scan_document(text)
    assert any(issue.code == "MQ004" for issue in issues)


def test_scan_valid_document_is_clean() -> None:
    text = "# Alpha\n## Beta\nHello\n"
    _, issues = scan_document(text)
    assert issues == []


def test_normalize_skipped_heading_level() -> None:
    text = "# Alpha\n### Bravo\n"
    normalized = normalize_headings(text)
    assert normalized == "# Alpha\n### Bravo\n"


def test_normalize_adjacent_level() -> None:
    text = "# Alpha\n## Beta\n"
    normalized = normalize_headings(text)
    assert normalized == "# Alpha\n## Beta\n"


def test_main_scan_stdout(tmp_path: Path) -> None:
    target = tmp_path / "doc.md"
    target.write_text("# Title\n## Intro\n", encoding="utf-8")
    rc = main(["scan", "--input", str(target)])
    assert rc == 0
