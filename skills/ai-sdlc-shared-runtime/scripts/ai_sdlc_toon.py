#!/usr/bin/env python3
"""Deterministic TOON 3.3 encoding and decoding for harness contracts."""

from __future__ import annotations

import ast
import math
import re
from typing import Any


_BARE_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")
_NUMBER = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?$")
_RESERVED = {"true", "false", "null"}


def _primitive(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _key(value: Any) -> str:
    text = str(value)
    return text if _BARE_KEY.fullmatch(text) else _quote(text)


def _quote(value: str) -> str:
    """Quote a TOON string without routing through another wire format."""
    escaped: list[str] = ['"']
    replacements = {
        '"': '\\"',
        "\\": "\\\\",
        "\b": "\\b",
        "\f": "\\f",
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
    }
    for character in value:
        if character in replacements:
            escaped.append(replacements[character])
        elif ord(character) < 0x20:
            escaped.append(f"\\u{ord(character):04x}")
        else:
            escaped.append(character)
    escaped.append('"')
    return "".join(escaped)


def _string(value: str) -> str:
    needs_quotes = (
        not value
        or value != value.strip()
        or value.lower() in _RESERVED
        or bool(_NUMBER.fullmatch(value))
        or value.startswith("-")
        or any(character in value for character in ':,"[]{}\n\r\t\\')
    )
    return _quote(value) if needs_quotes else value


def _scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("TOON cannot encode non-finite numbers")
        if value == 0:
            return "0"
        return repr(value)
    if isinstance(value, str):
        return _string(value)
    raise TypeError(f"unsupported TOON scalar: {type(value).__name__}")


def _table(value: list[Any]) -> list[str] | None:
    if not value or not all(isinstance(item, dict) and item for item in value):
        return None
    fields = sorted(value[0], key=str)
    if any(set(item) != set(fields) for item in value):
        return None
    if any(not _primitive(item[field]) for item in value for field in fields):
        return None
    return fields


def _emit_mapping(value: dict[Any, Any], depth: int) -> list[str]:
    lines: list[str] = []
    prefix = "  " * depth
    for raw_key in sorted(value, key=str):
        item = value[raw_key]
        key = _key(raw_key)
        if _primitive(item):
            lines.append(f"{prefix}{key}: {_scalar(item)}")
        elif isinstance(item, dict):
            if item:
                lines.append(f"{prefix}{key}:")
                lines.extend(_emit_mapping(item, depth + 1))
            else:
                lines.append(f"{prefix}{key}: {{}}")
        elif isinstance(item, list):
            lines.extend(_emit_named_list(key, item, depth))
        else:
            raise TypeError(f"unsupported TOON value: {type(item).__name__}")
    return lines


def _emit_named_list(key: str, value: list[Any], depth: int) -> list[str]:
    prefix = "  " * depth
    if not value:
        return [f"{prefix}{key}[0]:"]
    if all(_primitive(item) for item in value):
        return [f"{prefix}{key}[{len(value)}]: " + ",".join(_scalar(item) for item in value)]
    fields = _table(value)
    if fields is not None:
        header = ",".join(_key(field) for field in fields)
        rows = [f"{prefix}{key}[{len(value)}]{{{header}}}:"]
        rows.extend(
            f"{'  ' * (depth + 1)}" + ",".join(_scalar(item[field]) for field in fields)
            for item in value
        )
        return rows
    lines = [f"{prefix}{key}[{len(value)}]:"]
    lines.extend(_emit_list_items(value, depth + 1))
    return lines


def _emit_list_items(value: list[Any], depth: int) -> list[str]:
    lines: list[str] = []
    prefix = "  " * depth
    for item in value:
        if _primitive(item):
            lines.append(f"{prefix}- {_scalar(item)}")
        elif isinstance(item, dict):
            if not item:
                lines.append(f"{prefix}- {{}}")
                continue
            first, *rest = sorted(item, key=str)
            first_value = item[first]
            first_key = _key(first)
            if _primitive(first_value):
                lines.append(f"{prefix}- {first_key}: {_scalar(first_value)}")
            elif isinstance(first_value, dict):
                if first_value:
                    lines.append(f"{prefix}- {first_key}:")
                    lines.extend(_emit_mapping(first_value, depth + 2))
                else:
                    lines.append(f"{prefix}- {first_key}: {{}}")
            elif isinstance(first_value, list):
                nested = _emit_named_list(first_key, first_value, depth + 1)
                lines.append(f"{prefix}- {nested[0].lstrip()}")
                lines.extend(nested[1:])
            else:
                raise TypeError(f"unsupported TOON value: {type(first_value).__name__}")
            if rest:
                lines.extend(_emit_mapping({key: item[key] for key in rest}, depth + 1))
        elif isinstance(item, list):
            if not item:
                lines.append(f"{prefix}- [0]:")
            elif all(_primitive(child) for child in item):
                lines.append(f"{prefix}- [{len(item)}]: " + ",".join(_scalar(child) for child in item))
            else:
                lines.append(f"{prefix}- [{len(item)}]:")
                lines.extend(_emit_list_items(item, depth + 1))
        else:
            raise TypeError(f"unsupported TOON value: {type(item).__name__}")
    return lines


def encode_toon(value: Any) -> str:
    """Encode a portable value as canonical, newline-terminated TOON."""
    value = _normalize(value)
    if isinstance(value, dict):
        lines = _emit_mapping(value, 0) if value else ["{}"]
    elif isinstance(value, list):
        if all(_primitive(item) for item in value):
            lines = [f"[{len(value)}]: " + ",".join(_scalar(item) for item in value)]
        else:
            lines = [f"[{len(value)}]:", *_emit_list_items(value, 1)]
    elif _primitive(value):
        lines = [_scalar(value)]
    else:
        raise TypeError(f"unsupported TOON root: {type(value).__name__}")
    return "\n".join(lines) + "\n"


def _normalize(value: Any) -> Any:
    """Convert tuples to lists recursively before encoding."""
    if isinstance(value, tuple):
        return [_normalize(item) for item in value]
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize(item) for key, item in value.items()}
    return value


class ToonDecodeError(ValueError):
    """Raised when input is outside the canonical TOON subset."""


_TABLE_HEADER = re.compile(r"^(.+?)\[(\d+)\]\{(.*)\}:$")
_LIST_HEADER = re.compile(r"^(.+?)\[(\d+)\]:(?:\s*(.*))?$")
_ANON_LIST_HEADER = re.compile(r"^\[(\d+)\]:(?:\s*(.*))?$")


def _indent(raw: str) -> int:
    spaces = len(raw) - len(raw.lstrip(" "))
    if spaces % 2:
        raise ToonDecodeError("TOON indentation must use two-space levels")
    return spaces // 2


def _split_quoted(value: str, delimiter: str = ",") -> list[str]:
    """Split a row while preserving quoted delimiters and escapes."""
    if value == "":
        return []
    result: list[str] = []
    current: list[str] = []
    quoted = False
    escaped = False
    for character in value:
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character == "\\" and quoted:
            current.append(character)
            escaped = True
            continue
        if character == '"':
            current.append(character)
            quoted = not quoted
            continue
        if character == delimiter and not quoted:
            result.append("".join(current).strip())
            current = []
            continue
        current.append(character)
    if quoted:
        raise ToonDecodeError("unterminated quoted TOON scalar")
    result.append("".join(current).strip())
    return result


def _split_pair(value: str) -> tuple[str, str] | None:
    quoted = False
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\" and quoted:
            escaped = True
            continue
        if character == '"':
            quoted = not quoted
            continue
        if character == ":" and not quoted:
            return value[:index].strip(), value[index + 1 :].strip()
    return None


def _decode_key(value: str) -> str:
    parsed = _decode_scalar(value)
    if not isinstance(parsed, str):
        raise ToonDecodeError(f"TOON mapping key must be text: {value}")
    return parsed


def _decode_scalar(value: str) -> Any:
    value = value.strip()
    if value == "{}":
        return {}
    if value.startswith('"'):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ToonDecodeError(f"invalid quoted TOON scalar: {value}") from exc
        if not isinstance(parsed, str):
            raise ToonDecodeError(f"quoted TOON scalar is not text: {value}")
        return parsed
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "null":
        return None
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)", value):
        return int(value)
    if _NUMBER.fullmatch(value):
        return float(value)
    return value


class _Parser:
    """Inverse parser for the exact canonical subset emitted above."""

    def __init__(self, text: str) -> None:
        self.lines = [line for line in text.splitlines() if line.strip()]

    def parse(self) -> Any:
        if not self.lines:
            raise ToonDecodeError("empty TOON input")
        first = self.lines[0].strip()
        anonymous = _ANON_LIST_HEADER.fullmatch(first)
        if anonymous:
            count = int(anonymous.group(1))
            inline = anonymous.group(2) or ""
            if inline:
                values = [_decode_scalar(item) for item in _split_quoted(inline)]
                self._count(values, count, "root list")
                if len(self.lines) != 1:
                    raise ToonDecodeError("unexpected data after inline root list")
                return values
            values, index = self.parse_list(1, 1, count)
            if index != len(self.lines):
                raise ToonDecodeError("unexpected data after root list")
            return values
        if _split_pair(first) is None and not _TABLE_HEADER.fullmatch(first) and not _LIST_HEADER.fullmatch(first):
            if len(self.lines) != 1:
                raise ToonDecodeError("scalar TOON root has trailing data")
            return _decode_scalar(first)
        value, index = self.parse_mapping(0, 0)
        if index != len(self.lines):
            raise ToonDecodeError(f"unexpected TOON content at line {index + 1}")
        return value

    @staticmethod
    def _count(values: list[Any], expected: int, label: str) -> None:
        if len(values) != expected:
            raise ToonDecodeError(
                f"{label} declares {expected} items but contains {len(values)}"
            )

    def parse_mapping(self, index: int, depth: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(self.lines):
            raw = self.lines[index]
            current = _indent(raw)
            if current < depth:
                break
            if current > depth:
                raise ToonDecodeError(f"unexpected indentation at line {index + 1}")
            text = raw.strip()
            if text.startswith("- "):
                break
            key, value, index = self.parse_named(index, depth, text, depth + 1)
            if key in result:
                raise ToonDecodeError(f"duplicate TOON key: {key}")
            result[key] = value
        return result, index

    def parse_named(
        self,
        index: int,
        depth: int,
        text: str,
        child_depth: int,
    ) -> tuple[str, Any, int]:
        table = _TABLE_HEADER.fullmatch(text)
        if table:
            key = _decode_key(table.group(1))
            count = int(table.group(2))
            fields = [_decode_key(item) for item in _split_quoted(table.group(3))]
            rows: list[dict[str, Any]] = []
            index += 1
            for _ in range(count):
                if index >= len(self.lines) or _indent(self.lines[index]) != child_depth:
                    raise ToonDecodeError(f"missing table row for {key}")
                cells = [
                    _decode_scalar(item)
                    for item in _split_quoted(self.lines[index].strip())
                ]
                if len(cells) != len(fields):
                    raise ToonDecodeError(
                        f"table {key} row has {len(cells)} cells; expected {len(fields)}"
                    )
                rows.append(dict(zip(fields, cells)))
                index += 1
            return key, rows, index

        named_list = _LIST_HEADER.fullmatch(text)
        if named_list:
            key = _decode_key(named_list.group(1))
            count = int(named_list.group(2))
            inline = named_list.group(3) or ""
            index += 1
            if inline:
                values = [_decode_scalar(item) for item in _split_quoted(inline)]
                self._count(values, count, key)
                return key, values, index
            if count == 0:
                return key, [], index
            values, index = self.parse_list(index, child_depth, count)
            return key, values, index

        pair = _split_pair(text)
        if pair is None:
            raise ToonDecodeError(f"invalid TOON mapping line: {text}")
        raw_key, rest = pair
        key = _decode_key(raw_key)
        index += 1
        if rest:
            return key, _decode_scalar(rest), index
        if index >= len(self.lines) or _indent(self.lines[index]) <= depth:
            return key, {}, index
        if _indent(self.lines[index]) != child_depth:
            raise ToonDecodeError(f"invalid nested indentation for {key}")
        if self.lines[index].strip().startswith("- "):
            values, index = self.parse_list(index, child_depth, None)
            return key, values, index
        value, index = self.parse_mapping(index, child_depth)
        return key, value, index

    def parse_list(
        self,
        index: int,
        depth: int,
        expected: int | None,
    ) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(self.lines):
            raw = self.lines[index]
            current = _indent(raw)
            if current < depth:
                break
            if current != depth or not raw.strip().startswith("- "):
                break
            content = raw.strip()[2:].strip()
            index += 1
            if content == "{}":
                item: Any = {}
            else:
                anonymous = _ANON_LIST_HEADER.fullmatch(content)
                table = _TABLE_HEADER.fullmatch(content)
                named_list = _LIST_HEADER.fullmatch(content)
                pair = _split_pair(content)
                if anonymous:
                    count = int(anonymous.group(1))
                    inline = anonymous.group(2) or ""
                    if inline:
                        item = [
                            _decode_scalar(value)
                            for value in _split_quoted(inline)
                        ]
                        self._count(item, count, "anonymous list")
                    elif count == 0:
                        item = []
                    else:
                        item, index = self.parse_list(index, depth + 1, count)
                elif table or named_list:
                    key, value, index = self.parse_named(
                        index - 1,
                        depth,
                        content,
                        depth + 2,
                    )
                    item = {key: value}
                elif pair is not None:
                    raw_key, rest = pair
                    key = _decode_key(raw_key)
                    item = {}
                    if rest:
                        item[key] = _decode_scalar(rest)
                    elif (
                        index < len(self.lines)
                        and _indent(self.lines[index]) == depth + 2
                    ):
                        if self.lines[index].strip().startswith("- "):
                            value, index = self.parse_list(index, depth + 2, None)
                        else:
                            value, index = self.parse_mapping(index, depth + 2)
                        item[key] = value
                    else:
                        item[key] = {}
                else:
                    item = _decode_scalar(content)

            if isinstance(item, dict) and index < len(self.lines):
                if (
                    _indent(self.lines[index]) == depth + 1
                    and not self.lines[index].strip().startswith("- ")
                ):
                    rest, index = self.parse_mapping(index, depth + 1)
                    duplicate = set(item) & set(rest)
                    if duplicate:
                        raise ToonDecodeError(
                            "duplicate TOON list-item keys: "
                            + ", ".join(sorted(duplicate))
                        )
                    item.update(rest)
            result.append(item)
            if expected is not None and len(result) == expected:
                break
        if expected is not None:
            self._count(result, expected, "list")
        return result, index


def decode_toon(text: str) -> Any:
    """Decode canonical TOON into portable Python values."""
    return _Parser(text).parse()


def loads(text: str) -> Any:
    """Alias used by harness loaders."""
    return decode_toon(text)


def load(handle: Any) -> Any:
    """Read and decode TOON from a text handle."""
    return decode_toon(handle.read())


def dumps(value: Any, **_options: Any) -> str:
    """Return canonical TOON without the terminating newline."""
    return encode_toon(value).rstrip("\n")


def dump(value: Any, handle: Any, **_options: Any) -> None:
    """Write canonical TOON to a text handle."""
    handle.write(dumps(value))
