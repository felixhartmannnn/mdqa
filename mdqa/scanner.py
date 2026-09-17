from __future__ import annotations

import re
from typing import List, Optional, Tuple

from mdqa.models import (
    EmptySectionIssue,
    HeadingGapIssue,
    Issue,
    LinkTargetIssue,
    Section,
    UnclosedHeadingGapIssue,
)

_HEADING_RE = re.compile(r"^(#{1,6})(\s+)(.+)$")
_ANCHOR_LINK_RE = re.compile(r"\[[^\]]+\]\(#([^)]+)\)")
_REF_LINK_RE = re.compile(r"^\[(.+?)\]:\s*(#\S+)", re.MULTILINE)
_LOCAL_LINK_RE = re.compile(r"\]\((#[^)]+)\)")


def _collect_link_targets(text: str) -> List[str]:
    return _ANCHOR_LINK_RE.findall(text) + _REF_LINK_RE.findall(text)


def scan_document(text: str) -> Tuple[List[Section], List[Issue]]:
    lines = text.splitlines()
    sections: List[Section] = []
    issues: List[Issue] = []

    headings: List[Tuple[int, int]] = []
    for lineno, raw in enumerate(lines, start=1):
        match = _HEADING_RE.match(raw)
        if match:
            headings.append((lineno, len(match.group(1))))

    for idx, (lineno, level) in enumerate(headings):
        next_lineno = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines) + 1
        body = lines[lineno:next_lineno - 1]
        sections.append(
            Section(
                title=lines[lineno - 1],
                lineno=lineno,
                level=level,
                content_lines=body,
                link_targets=_collect_link_targets("\n".join(body)),
                end_lineno=next_lineno - 1 if idx + 1 < len(headings) else len(lines),
            )
        )

    for idx, (lineno, level) in enumerate(headings):
        if idx + 1 < len(headings):
            next_level = headings[idx + 1][1]
            if next_level > level + 1:
                issues.append(
                    UnclosedHeadingGapIssue(
                        message=f"Unclosed heading gap from H{level} to H{next_level}",
                        lineno=lineno,
                        from_level=level,
                        to_level=next_level,
                    )
                )
        if idx > 0:
            previous_level = headings[idx - 1][1]
            if level > previous_level + 1:
                issues.append(
                    HeadingGapIssue(
                        message=f"Heading gap from H{previous_level} to H{level}",
                        lineno=lineno,
                        previous_level=previous_level,
                        skipped_level=level,
                    )
                )

    for section in sections:
        has_body = any(line.strip() and line.strip() != "<!-- -->" for line in section.content_lines)
        if not has_body and section.end_lineno is not None and section.end_lineno > section.lineno + 1:
            issues.append(
                EmptySectionIssue(
                    message=f"Empty section at line {section.lineno}: {section.title.strip()}",
                    lineno=section.lineno,
                    section_level=section.level,
                )
            )
        for target in _LOCAL_LINK_RE.findall("\n".join(section.content_lines)):
            found = any(
                section.title.lstrip("#").strip().lower() == target.lstrip("#").lower()
                for section in sections
            )
            if not found:
                issues.append(
                    LinkTargetIssue(
                        message=f"Link target `{target}` is not defined by a heading in this document",
                        lineno=section.lineno,
                        target=target,
                    )
                )

    return sections, issues
