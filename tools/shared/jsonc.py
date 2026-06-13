"""Utilities for reading JSON with JSONC-style comments."""

from __future__ import annotations

import json
from pathlib import Path


def strip_json_comments(text: str) -> str:
    """Remove JSONC comments while preserving string contents."""

    output: list[str] = []
    index = 0
    in_string = False
    escape = False
    length = len(text)

    while index < length:
        current = text[index]
        next_char = text[index + 1] if index + 1 < length else ""

        if in_string:
            output.append(current)
            if escape:
                escape = False
            elif current == "\\":
                escape = True
            elif current == '"':
                in_string = False
            index += 1
            continue

        if current == '"':
            in_string = True
            output.append(current)
            index += 1
            continue

        if current == "/" and next_char == "/":
            index = _skip_single_line_comment(text, index + 2)
            continue

        if current == "/" and next_char == "*":
            index = _skip_multi_line_comment(text, index + 2)
            continue

        output.append(current)
        index += 1

    return "".join(output)


def loads_jsonc(text: str) -> object:
    """Parse JSON or JSONC text into a Python object."""

    return json.loads(strip_json_comments(text))


def load_jsonc(path: Path) -> object:
    """Read and parse a JSON or JSONC file."""

    return loads_jsonc(path.read_text(encoding="utf-8"))


def _skip_single_line_comment(text: str, index: int) -> int:
    """Skip a single-line comment and preserve the line ending."""

    length = len(text)
    while index < length and text[index] not in "\r\n":
        index += 1
    return index


def _skip_multi_line_comment(text: str, index: int) -> int:
    """Skip a multi-line comment."""

    length = len(text)
    while index < length - 1:
        if text[index] == "*" and text[index + 1] == "/":
            return index + 2
        index += 1
    return length
