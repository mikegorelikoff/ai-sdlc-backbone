#!/usr/bin/env python3
"""Render the complete AI SDLC context-cache graph as a standalone HTML file."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sqlite3
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


GOLDEN_ANGLE = math.pi * (3.0 - math.sqrt(5.0))
VIEW_SCHEMA = "ai-sdlc-context-graph-view/v1"


def stable_phase(value: str) -> float:
    raw = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(raw[:4], "big") / 2**32 * math.tau


def safe_json(value: object) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def load_graph(database: Path, root: Path, include_source: bool = False) -> tuple[
    list[list[object]], list[list[object]], dict[str, int], dict[str, int],
    list[list[object]], dict[str, list[object]],
]:
    uri = f"{database.resolve().as_uri()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        raw_nodes = connection.execute(
            "SELECT id, kind, path, label FROM graph_nodes ORDER BY kind, path, label, id"
        ).fetchall()
        raw_edges = connection.execute(
            "SELECT source_id, target_id, kind, label, evidence_path "
            "FROM graph_edges ORDER BY source_id, target_id, kind, label, evidence_path"
        ).fetchall()
        ranges: dict[str, tuple[int, int]] = {}
        for table in ("chunks", "symbols", "occurrences", "ast_calls"):
            ranges.update({
                str(node_id): (int(start_line), int(end_line))
                for node_id, start_line, end_line in connection.execute(
                    f"SELECT id, start_line, end_line FROM {table}"
                )
            })
        documents = [
            (str(path), str(sha256), int(line_count))
            for path, sha256, line_count in connection.execute(
                "SELECT path, sha256, line_count FROM documents ORDER BY path"
            )
        ]
    line_counts = {path: line_count for path, _sha256, line_count in documents}

    by_path: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for node_id, kind, path, label in raw_nodes:
        node_path = str(path or "")
        by_path[node_path].append((str(node_id), str(kind), str(label or "")))

    by_root: dict[str, list[str]] = defaultdict(list)
    for path in by_path:
        root_name = path.split("/", 1)[0] if path else "repository"
        by_root[root_name].append(path)

    root_counts = {
        root_name: sum(len(by_path[path]) for path in paths)
        for root_name, paths in by_root.items()
    }
    ordered_roots = sorted(by_root, key=lambda root_name: (-root_counts[root_name], root_name))
    root_centers: dict[str, tuple[float, float]] = {}
    for index, root_name in enumerate(ordered_roots):
        if index == 0:
            radius = 0.0
        else:
            radius = 2350.0 * math.sqrt(index)
        angle = index * GOLDEN_ANGLE
        root_centers[root_name] = (math.cos(angle) * radius, math.sin(angle) * radius)

    coordinates: dict[str, tuple[float, float]] = {}
    root_labels: list[list[object]] = []
    for root_name in ordered_roots:
        center_x, center_y = root_centers[root_name]
        root_labels.append([root_name, round(center_x, 2), round(center_y, 2), root_counts[root_name]])
        paths = sorted(by_root[root_name], key=lambda path: (-len(by_path[path]), path))
        phase = stable_phase(root_name)
        for path_index, path in enumerate(paths):
            path_radius = 105.0 * math.sqrt(path_index)
            path_angle = phase + path_index * GOLDEN_ANGLE
            anchor_x = center_x + math.cos(path_angle) * path_radius
            anchor_y = center_y + math.sin(path_angle) * path_radius
            kind_order = {"file": 0, "trace-hub": 1, "chunk": 2, "symbol": 3, "call": 4, "occurrence": 5}
            members = sorted(by_path[path], key=lambda row: (kind_order.get(row[1], 9), row[2], row[0]))
            member_phase = stable_phase(path)
            for member_index, (node_id, kind, _label) in enumerate(members):
                if member_index == 0 and kind == "file":
                    x, y = anchor_x, anchor_y
                else:
                    layer = {
                        "file": 0.0,
                        "trace-hub": 4.0,
                        "chunk": 7.0,
                        "symbol": 11.0,
                        "call": 16.0,
                        "occurrence": 21.0,
                    }.get(kind, 24.0)
                    radius = layer + 2.35 * math.sqrt(member_index + 1)
                    angle = member_phase + member_index * GOLDEN_ANGLE
                    x = anchor_x + math.cos(angle) * radius
                    y = anchor_y + math.sin(angle) * radius
                coordinates[node_id] = (round(x, 2), round(y, 2))

    nodes: list[list[object]] = []
    node_index: dict[str, int] = {}
    node_counts: Counter[str] = Counter()
    for node_id, kind, path, label in raw_nodes:
        x, y = coordinates[str(node_id)]
        node_index[str(node_id)] = len(nodes)
        start_line, end_line = ranges.get(str(node_id), (0, 0))
        if str(kind) == "file":
            start_line, end_line = 1, line_counts.get(str(path or ""), 0)
        nodes.append([
            str(node_id), str(kind), str(path or ""), str(label or ""), x, y,
            start_line, end_line,
        ])
        node_counts[str(kind)] += 1

    edges: list[list[object]] = []
    edge_counts: Counter[str] = Counter()
    for source, target, kind, label, evidence_path in raw_edges:
        source_index = node_index.get(str(source))
        target_index = node_index.get(str(target))
        if source_index is None or target_index is None:
            continue
        edges.append([source_index, target_index, str(kind), str(label or ""), str(evidence_path or "")])
        edge_counts[str(kind)] += 1

    sources: dict[str, list[object]] = {}
    if include_source:
        resolved_root = root.resolve()
        for path, expected_sha256, _line_count in documents:
            candidate = root / path
            try:
                resolved = candidate.resolve()
                resolved.relative_to(resolved_root)
                relative = candidate.relative_to(root)
            except (OSError, ValueError):
                continue
            cursor = resolved_root
            if any((cursor := cursor / part).is_symlink() for part in relative.parts):
                continue
            if not resolved.is_file() or candidate.is_symlink():
                continue
            data = resolved.read_bytes()
            current_sha256 = hashlib.sha256(data).hexdigest()
            sources[path] = [
                data.decode("utf-8", errors="replace"),
                current_sha256 == expected_sha256,
            ]

    return nodes, edges, dict(node_counts), dict(edge_counts), root_labels, sources


HTML = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; font-src 'none'; base-uri 'none'; form-action 'none'">
  <title>AI SDLC Harness · Full Context Graph</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #0d0e10;
      --surface: rgba(20, 21, 23, .97);
      --surface-raised: #18191c;
      --surface-soft: rgba(255, 255, 255, .018);
      --border: #292a2e;
      --border-strong: #3a3b40;
      --text: #f1f1f2;
      --text-secondary: #a2a3a9;
      --text-tertiary: #686970;
      --accent: #5e6ad2;
      --accent-soft: rgba(94, 106, 210, .13);
      --cyan: #55d6cf;
      --green: #64d49a;
      --amber: #e8a95b;
      --radius: 7px;
      --shadow: 0 14px 42px rgba(0, 0, 0, .38);
    }
    * { box-sizing: border-box; }
    html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }
    body {
      background: var(--bg);
      color: var(--text);
      font: 13px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        radial-gradient(circle at 42% 46%, rgba(38, 40, 54, .28), transparent 46%),
        linear-gradient(rgba(255,255,255,.009) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.009) 1px, transparent 1px);
      background-size: auto, 40px 40px, 40px 40px;
      mask-image: linear-gradient(to bottom, black, transparent 90%);
    }
    ::selection { background: rgba(124,140,255,.32); }
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,.1); border: 3px solid transparent; border-radius: 999px; background-clip: padding-box; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,.17); border: 3px solid transparent; background-clip: padding-box; }
    canvas { position: fixed; inset: 0; width: 100%; height: 100%; cursor: grab; }
    canvas.dragging { cursor: grabbing; }
    .hover-card {
      position: fixed;
      z-index: 3;
      display: none;
      max-width: 310px;
      padding: 8px 10px;
      border: 1px solid var(--border-strong);
      border-radius: 8px;
      background: rgba(12, 15, 22, .94);
      box-shadow: 0 12px 32px rgba(0, 0, 0, .38);
      pointer-events: none;
      backdrop-filter: blur(16px);
    }
    .hover-card.visible { display: block; }
    .hover-kind { color: #aeb7ff; font-size: 8px; font-weight: 680; letter-spacing: .08em; text-transform: uppercase; }
    .hover-title, .hover-path { display: block; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
    .hover-title { margin-top: 3px; color: #f0f3f8; font-size: 10px; font-weight: 590; }
    .hover-path { margin-top: 2px; color: var(--text-tertiary); font: 8px/1.45 ui-monospace, SFMono-Regular, Menlo, monospace; }
    button, input { font: inherit; }
    button { border: 0; }

    .topbar {
      position: fixed;
      z-index: 6;
      top: 12px;
      left: 50%;
      display: grid;
      grid-template-columns: minmax(210px, auto) minmax(320px, 1fr) auto;
      align-items: center;
      gap: 10px;
      width: min(1200px, calc(100vw - 32px));
      min-height: 50px;
      padding: 5px 6px;
      border-radius: 8px;
      transform: translateX(-50%);
    }
    .topbar, .filterbar, .modal-dialog, .statusbar {
      pointer-events: auto;
      border: 1px solid var(--border);
      background: var(--surface);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }
    .brand {
      display: flex;
      align-items: center;
      min-width: 210px;
      padding: 2px 16px 2px 10px;
      border-right: 1px solid var(--border);
    }
    .brand-copy { min-width: 0; }
    .brand-eyebrow { color: var(--text-tertiary); font-size: 9px; font-weight: 520; letter-spacing: .02em; }
    .brand-title { margin-top: 1px; color: #ececee; font-size: 12px; font-weight: 560; letter-spacing: -.01em; white-space: nowrap; }
    .local-status {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #898a90;
      font-size: 9px;
      font-weight: 520;
    }
    .local-status::before { content: ""; width: 5px; height: 5px; border-radius: 50%; background: var(--green); }
    .search-wrap { position: relative; width: 100%; border: 1px solid transparent; border-radius: 6px; background: #111214; }
    .search-icon { position: absolute; z-index: 1; top: 50%; left: 12px; width: 13px; height: 13px; margin-top: -7px; border: 1.5px solid #6e7077; border-radius: 50%; pointer-events: none; }
    .search-icon::after { content: ""; position: absolute; right: -4px; bottom: -2px; width: 6px; height: 1.5px; background: #737e92; transform: rotate(45deg); transform-origin: left center; }
    #search { width: 100%; height: 38px; padding: 0 62px 0 36px; border: 0; outline: 0; color: var(--text); background: transparent; font-size: 12px; }
    #search::placeholder { color: #65666d; }
    .search-wrap:focus-within { border-color: #42444b; background: #121315; }
    .keycap { position: absolute; top: 50%; right: 11px; transform: translateY(-50%); color: #5f6067; font: 9px ui-monospace, monospace; }
    .results { display: none; position: absolute; top: calc(100% + 8px); left: 0; right: 0; max-height: 390px; overflow: auto; padding: 5px; border: 1px solid var(--border-strong); border-radius: var(--radius); background: var(--surface-raised); box-shadow: var(--shadow); }
    .result { padding: 9px 10px; border-radius: 5px; cursor: pointer; }
    .result + .result { margin-top: 2px; }
    .result:hover { background: var(--accent-soft); }
    .result b, .result small { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .result b { color: #e9edf6; font-size: 11px; font-weight: 580; }
    .result small { margin-top: 2px; color: var(--text-tertiary); font-size: 9px; }
    .header-meta { display: flex; align-items: center; gap: 14px; padding: 0 9px 0 4px; }
    .header-stat { min-width: 112px; text-align: right; }
    .header-stat b, .header-stat span { display: block; }
    .header-stat b { color: #b8b9be; font-size: 9px; font-weight: 540; }
    .header-stat span { margin-top: 1px; color: #5f6067; font-size: 8px; }
    .filterbar {
      position: fixed;
      z-index: 4;
      top: 70px;
      left: 50%;
      display: flex;
      align-items: center;
      width: min(1100px, calc(100vw - 48px));
      min-height: 38px;
      padding: 4px 5px 4px 10px;
      border-radius: 7px;
      transform: translateX(-50%);
    }
    .filter-label { flex: 0 0 auto; margin-right: 7px; color: #606168; font-size: 8px; font-weight: 540; }
    .filter-controls { display: flex; min-width: 0; gap: 2px; overflow-x: auto; scrollbar-width: none; }
    .filter-controls::-webkit-scrollbar { display: none; }
    .filter-divider { flex: 0 0 auto; width: 1px; height: 22px; margin: 0 5px; background: var(--border); }
    .control-button { display: inline-flex; flex: 0 0 auto; align-items: center; gap: 6px; height: 28px; padding: 0 8px; border: 1px solid transparent; border-radius: 5px; color: #98999f; background: transparent; cursor: pointer; white-space: nowrap; transition: color .12s ease, background .12s ease, border-color .12s ease; }
    .control-button:hover, .control-button:focus-visible { color: #ececee; border-color: #303136; background: #202124; outline: none; }
    .control-button.off { color: #56575d; opacity: .65; }
    .control-button .count { color: #5f6067; font: 8px ui-monospace, monospace; }
    .control-button.icon { min-width: 28px; justify-content: center; padding: 0 6px; font-size: 13px; }
    .control-button.fit { color: #a8a9af; font-size: 9px; }

    .modal-backdrop {
      position: fixed;
      z-index: 20;
      inset: 0;
      display: grid;
      place-items: center;
      padding: 40px;
      visibility: hidden;
      opacity: 0;
      background: rgba(3, 5, 9, .7);
      backdrop-filter: blur(8px) saturate(85%);
      transition: opacity .18s ease, visibility .18s ease;
    }
    .modal-backdrop.open { visibility: visible; opacity: 1; }
    .modal-dialog {
      display: flex;
      flex-direction: column;
      width: min(900px, 100%);
      height: min(720px, 100%);
      overflow: hidden;
      border-radius: 9px;
      transform: translateY(12px) scale(.985);
      transition: transform .2s ease;
    }
    .modal-backdrop.open .modal-dialog { transform: translateY(0) scale(1); }
    .panel-header { position: relative; flex: 0 0 auto; padding: 22px 68px 18px 24px; }
    .modal-close { position: absolute; top: 14px; right: 15px; display: grid; place-items: center; width: 32px; height: 32px; border: 1px solid transparent; border-radius: 5px; color: var(--text-secondary); background: transparent; cursor: pointer; font-size: 18px; line-height: 1; transition: .12s ease; }
    .modal-close:hover, .modal-close:focus-visible { color: #fff; border-color: var(--border); background: #222326; outline: none; }
    .panel-kicker { color: #777980; font-size: 9px; font-weight: 540; letter-spacing: .02em; text-transform: capitalize; }
    .panel-header h1 { margin: 5px 0 5px; overflow: hidden; color: #f1f1f2; font-size: 20px; font-weight: 610; letter-spacing: -.02em; white-space: nowrap; text-overflow: ellipsis; }
    .panel-subtitle { overflow: hidden; color: #777980; font: 9px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; white-space: nowrap; text-overflow: ellipsis; }
    .tabs { display: flex; gap: 20px; min-height: 44px; margin: 0; padding: 0 22px; border-bottom: 1px solid var(--border); background: #131416; }
    .tab { position: relative; height: 44px; padding: 0 1px; border-radius: 0; color: var(--text-tertiary); background: transparent; cursor: pointer; font-size: 10px; font-weight: 540; transition: .12s ease; }
    .tab:hover { color: var(--text-secondary); }
    .tab.active { color: #ececee; }
    .tab.active::after { content: ""; position: absolute; right: 0; bottom: -1px; left: 0; height: 1px; background: #818cf8; }
    .tab-meta { margin-left: 5px; color: #62636a; font: 8px ui-monospace, monospace; }
    .panel-body { min-height: 0; flex: 1; overflow: auto; padding: 24px; }
    .modal-footer { display: flex; flex: 0 0 auto; align-items: center; gap: 18px; min-height: 38px; padding: 0 20px; border-top: 1px solid var(--border); color: var(--text-tertiary); font-size: 8px; }
    .modal-footer b { margin-right: 4px; color: #aeb6c6; font-weight: 620; }
    .modal-footer .footer-note { margin-left: auto; color: #788397; }
    .pane { display: none; }
    .pane.active { display: block; }
    .modal-dialog .sub { color: var(--text-tertiary); font-size: 10px; line-height: 1.55; }
    .pane-heading { margin: 0 0 18px; }
    .pane-heading h2 { margin: 0; color: #e6e6e8; font-size: 12px; font-weight: 570; }
    .pane-heading p { margin: 4px 0 0; color: #65666d; font-size: 9px; }
    .detail-layout { display: grid; grid-template-columns: minmax(0, 1fr) 220px; gap: 38px; }
    .detail-section h2, .context-section h2 { margin: 0 0 12px; color: #85868c; font-size: 9px; font-weight: 560; }
    .property-list { border-top: 1px solid var(--border); word-break: break-word; }
    .property-row { display: grid; grid-template-columns: 104px minmax(0, 1fr); gap: 18px; align-items: start; padding: 12px 0; border-bottom: 1px solid var(--border); }
    .property-row span { color: #66676e; font-size: 9px; }
    .property-row code { overflow: hidden; color: #c9c9cd; font: 9px/1.55 ui-monospace, SFMono-Regular, Menlo, monospace; text-overflow: ellipsis; }
    .context-section { min-width: 0; }
    .context-list { border-top: 1px solid var(--border); }
    .context-row { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; min-height: 39px; padding: 10px 0; border-bottom: 1px solid var(--border); }
    .context-row span { color: #66676e; font-size: 9px; }
    .context-row strong { color: #d7d7da; font-size: 11px; font-weight: 560; }
    .context-note { margin: 14px 0 0; color: #5f6067; font-size: 9px; line-height: 1.55; }
    .dot { flex: 0 0 auto; width: 6px; height: 6px; border-radius: 2px; }
    .connection-summary { margin-bottom: 12px; padding: 0 0 12px; border-bottom: 1px solid var(--border); color: var(--text-tertiary); background: transparent; font-size: 9px; line-height: 1.5; }
    .connections { overflow: hidden; border: 1px solid var(--border); border-radius: 7px; background: #111214; }
    .connection { display: grid; width: 100%; grid-template-columns: 24px minmax(0, 1fr) 18px; gap: 9px; align-items: center; min-height: 54px; padding: 8px 12px; border-bottom: 1px solid rgba(255,255,255,.05); color: inherit; background: transparent; text-align: left; cursor: pointer; transition: .12s ease; }
    .connection:last-child { border-bottom: 0; }
    .connection:hover { background: var(--accent-soft); }
    .connection .direction { color: #65666d; text-align: center; }
    .connection .edge-kind { overflow: hidden; color: #777980; font-size: 8px; font-weight: 560; text-overflow: ellipsis; text-transform: uppercase; letter-spacing: .03em; }
    .connection .relation-calls { color: #d9a568; }
    .connection .relation-imports, .connection .relation-import { color: #67c7c1; }
    .connection .relation-references, .connection .relation-path-reference { color: #929bf0; }
    .connection .relation-defines { color: #bd91e8; }
    .connection .relation-test-target { color: #dc8796; }
    .connection .relation-spec-trace { color: #78c89d; }
    .connection .target { min-width: 0; }
    .connection .target b, .connection .target small { display: block; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
    .connection .target b { color: #dce1eb; font-size: 10px; font-weight: 560; }
    .connection .target small { margin-top: 4px; color: #606168; font-size: 8px; }
    .connection .edge-kind { margin-right: 5px; }
    .connection .chevron { color: #4f5056; font-size: 15px; text-align: right; }
    .code-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 7px; margin-bottom: 10px; color: var(--text-tertiary); font: 9px/1.45 ui-monospace, SFMono-Regular, Menlo, monospace; }
    .fresh, .stale { display: inline-flex; align-items: center; gap: 5px; font-family: Inter, ui-sans-serif, system-ui, sans-serif; font-size: 8px; font-weight: 540; }
    .fresh::before, .stale::before { content: ""; width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
    .fresh { color: #78c89d; }
    .stale { color: #d9a568; }
    .code-view { overflow: auto; min-height: 180px; max-height: calc(100vh - 240px); border: 1px solid var(--border); border-radius: 10px; background: #090b10; font: 10px/1.65 "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; tab-size: 2; }
    .code-line { display: grid; grid-template-columns: 48px 1fr; min-width: max-content; }
    .code-line .ln { position: sticky; left: 0; padding: 0 10px 0 6px; border-right: 1px solid rgba(255,255,255,.04); color: #424b5b; background: #090b10; text-align: right; user-select: none; }
    .code-line .src { padding: 0 12px; color: #b7c0cf; white-space: pre; }
    .code-line:hover { background: rgba(255,255,255,.025); }
    .code-line.active { background: rgba(124,140,255,.115); }
    .code-line.active .ln { color: #9eabff; background: #151827; }
    .code-line.active .src { color: #edf0ff; }
    .tok-comment { color: #667085; font-style: italic; }
    .tok-string { color: #a7d58c; }
    .tok-number { color: #e8b76b; }
    .tok-keyword { color: #b6a0ff; font-weight: 560; }
    .tok-type { color: #70d7d0; }
    .tok-function { color: #83aaf2; }
    .tok-operator { color: #8993a6; }
    .summary-main { display: block; margin-bottom: 7px; color: #a9aaaf; font-weight: 540; }
    .summary-token { display: inline-flex; margin: 2px 12px 2px 0; color: #777980; font-size: 8px; }
    .summary-token::before { content: "·"; margin-right: 6px; color: #47484e; }
    .empty { padding: 18px; color: var(--text-tertiary); font-size: 10px; text-align: center; }
    .statusbar { position: fixed; z-index: 4; right: 20px; bottom: 14px; left: 20px; display: flex; align-items: center; height: 30px; padding: 0 11px; border-radius: 9px; color: var(--text-tertiary); font-size: 9px; }
    .statusbar .shortcut { margin-right: 15px; }
    .statusbar b { margin-right: 4px; color: #aeb6c6; font-weight: 580; }
    .statusbar .status-right { margin-left: auto; display: flex; gap: 14px; }
    .status-dot { display: inline-block; width: 5px; height: 5px; margin-right: 5px; border-radius: 50%; background: var(--green); }
    @media (max-width: 1050px) {
      .topbar { grid-template-columns: auto minmax(280px, 1fr); }
      .brand { min-width: 0; }
      .brand-eyebrow { display: none; }
      .header-meta { display: none; }
      .modal-backdrop { padding: 24px; }
      .filterbar { width: calc(100vw - 40px); }
    }
    @media (max-width: 720px) {
      .topbar { top: 8px; grid-template-columns: auto minmax(0, 1fr); width: calc(100vw - 20px); gap: 6px; padding: 5px; }
      .brand { min-width: 0; padding-right: 8px; }
      .search-wrap { grid-column: 2; }
      .filterbar { top: 66px; width: calc(100vw - 20px); padding-left: 8px; }
      .filter-label { display: none; }
      .modal-backdrop { padding: 10px; align-items: end; }
      .modal-dialog { width: 100%; height: min(86vh, 760px); border-radius: 9px 9px 7px 7px; }
      .panel-header { padding: 12px 54px 9px 14px; }
      .panel-header h1 { margin-top: 2px; font-size: 14px; }
      .panel-subtitle { display: none; }
      .modal-close { top: 9px; right: 10px; }
      .tabs { margin: 0; padding: 0 14px; }
      .panel-body { padding: 12px; }
      .modal-footer { padding: 0 12px; gap: 10px; }
      .modal-footer .footer-note { display: none; }
      .statusbar { right: 10px; bottom: 8px; left: 10px; }
      .statusbar .shortcut { display: none; }
      .statusbar .status-right { width: 100%; justify-content: space-between; margin-left: 0; }
      .statusbar .status-right span:nth-child(2) { display: none; }
      .detail-layout { grid-template-columns: 1fr; gap: 24px; }
      .property-row { grid-template-columns: 82px minmax(0, 1fr); }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
    }
  </style>
</head>
<body class="linear-shell">
  <canvas id="graph" role="application" aria-label="Interactive repository context graph" tabindex="0"></canvas>
  <div id="hoverCard" class="hover-card" aria-hidden="true">
    <span id="hoverKind" class="hover-kind"></span>
    <strong id="hoverTitle" class="hover-title"></strong>
    <code id="hoverPath" class="hover-path"></code>
  </div>
  <header class="topbar" role="banner">
    <div class="brand">
      <div class="brand-copy"><div class="brand-title">Context Graph</div><div class="brand-eyebrow">AI SDLC Harness</div></div>
    </div>
    <div class="search-wrap">
      <span class="search-icon"></span>
      <input id="search" autocomplete="off" placeholder="Search paths, symbols, calls…">
      <span class="keycap">⌘ F</span>
      <div class="results" id="results"></div>
    </div>
    <div class="header-meta"><div class="header-stat"><b id="headerGraphCount">Complete graph</b><span>Offline repository snapshot</span></div><div class="local-status">Local</div></div>
  </header>
  <div class="filterbar" role="toolbar" aria-label="Graph filters and view settings">
    <span class="filter-label">Layers</span>
    <div id="nodeToggles" class="filter-controls"></div>
    <span class="filter-divider" aria-hidden="true"></span>
    <span class="filter-label">View</span>
    <button class="control-button" id="edgeToggle" type="button" aria-pressed="true"><span class="dot" style="color:#71809d;background:#71809d"></span><span>Connections</span><span class="count">''' + "{{EDGE_TOTAL}}" + r'''</span></button>
    <button id="minus" class="control-button icon" type="button" title="Zoom out" aria-label="Zoom out">−</button>
    <button id="reset" class="control-button fit" type="button">Fit graph</button>
    <button id="plus" class="control-button icon" type="button" title="Zoom in" aria-label="Zoom in">＋</button>
  </div>
  <div id="modalBackdrop" class="modal-backdrop" aria-hidden="true">
  <section id="inspectorModal" class="modal-dialog" role="dialog" aria-modal="true" aria-labelledby="inspectorTitle" tabindex="-1">
    <header class="panel-header">
      <div id="inspectorKind" class="panel-kicker">Node inspector</div>
      <h1 id="inspectorTitle">Explore repository context</h1>
      <div id="inspectorPath" class="panel-subtitle">Select a node to inspect its repository context.</div>
      <button id="modalClose" class="modal-close" type="button" aria-label="Close node inspector">×</button>
    </header>
    <nav class="tabs" aria-label="Inspector views">
      <button class="tab active" data-tab="overview">Details</button>
      <button class="tab" data-tab="relations">Relations <span class="tab-meta" id="relationCount">0</span></button>
      <button class="tab" data-tab="source">Source <span class="tab-meta" id="sourceCount">off</span></button>
    </nav>
    <div class="panel-body">
      <section class="pane active" data-pane="overview">
        <div class="detail-layout">
          <section class="detail-section" aria-labelledby="propertiesTitle">
            <h2 id="propertiesTitle">Properties</h2>
            <div id="selection" class="property-list sub">Select any node in the graph</div>
          </section>
          <aside class="context-section" aria-labelledby="contextTitle">
            <h2 id="contextTitle">Direct context</h2>
            <div class="context-list">
              <div class="context-row"><span>Incoming</span><strong id="incomingTotal">0</strong></div>
              <div class="context-row"><span>Outgoing</span><strong id="outgoingTotal">0</strong></div>
              <div class="context-row"><span>Source</span><strong id="sourceState">—</strong></div>
            </div>
            <p class="context-note">Counts describe direct accepted graph edges for this node.</p>
          </aside>
        </div>
      </section>
      <section class="pane" data-pane="relations">
        <header class="pane-heading">
          <h2>Direct relations</h2>
          <p>Open a connected node without leaving the inspector.</p>
        </header>
        <div id="connectionSummary" class="connection-summary">Select a node to inspect its relations.</div>
        <div id="connections" class="connections"><div class="empty">No node selected</div></div>
      </section>
      <section class="pane source-pane" data-pane="source">
        <header class="pane-heading">
          <h2>Indexed source</h2>
          <p id="codeMeta" class="code-meta">Select a code-backed node.</p>
        </header>
        <div id="codeView" class="code-view"><div class="empty">Source preview will appear here</div></div>
      </section>
    </div>
    <footer class="modal-footer">
      <span><b>Esc</b>Close</span>
      <span><b>Tab</b>Move focus</span>
      <span class="footer-note">Selection stays visible on the graph</span>
    </footer>
  </section>
  </div>
  <footer class="statusbar">
    <span class="shortcut"><b>Scroll</b>Zoom</span><span class="shortcut"><b>Drag</b>Pan</span><span class="shortcut"><b>Click</b>Inspect</span><span class="shortcut"><b>Double click</b>Focus</span>
    <span class="status-right"><span><span class="status-dot"></span>Local snapshot</span><span>Zoom <b id="zoomValue">—</b></span><span>No network</span></span>
  </footer>
  <script>
  const NODES = {{NODES}};
  const EDGES = {{EDGES}};
  const NODE_COUNTS = {{NODE_COUNTS}};
  const EDGE_COUNTS = {{EDGE_COUNTS}};
  const ROOTS = {{ROOTS}};
  const SOURCES = {{SOURCES}};
  const COLORS = {file:'#53e0dc','chunk':'#7096ff','symbol':'#be86ff','call':'#ffb45e','occurrence':'#71809d','trace-hub':'#73e39f'};
  const SIZES = {file:3.9,chunk:2.15,symbol:2.65,call:1.25,occurrence:.72,'trace-hub':3.4};
  const canvas = document.getElementById('graph');
  const ctx = canvas.getContext('2d', {alpha:true});
  const hoverCard = document.getElementById('hoverCard');
  const modalBackdrop = document.getElementById('modalBackdrop');
  const inspectorModal = document.getElementById('inspectorModal');
  const modalClose = document.getElementById('modalClose');
  let dpr = Math.min(devicePixelRatio || 1, 2), width = 0, height = 0;
  let view = {x:0,y:0,scale:1}, bounds, dragging = false, moved = false, lastX = 0, lastY = 0;
  let selected = -1, hovered = -1, edgesVisible = true, dirty = true, hoverFrame = 0, hoverX = 0, hoverY = 0, modalOpen = false, previousFocus = null;
  const visibleKinds = new Set(Object.keys(NODE_COUNTS));
  const fmt = n => new Intl.NumberFormat('en').format(n);
  const sourceTotal = Object.keys(SOURCES).length;
  document.getElementById('sourceCount').textContent = sourceTotal ? fmt(sourceTotal) : 'off';
  const HASH_COMMENT_LANGUAGES = new Set(['python','shell','yaml','toon','ruby','toml']);
  const KEYWORDS = new Set(('as async await break case catch class const continue def default delete do elif else enum except export extends false finally for from function go if implements import in instanceof interface lambda let match new nil none null of package pass private protected public raise return self static struct super switch this throw trait true try type typeof undefined use var while with yield').split(' '));
  const EXTENSIONS = {py:'python',sh:'shell',bash:'shell',zsh:'shell',rb:'ruby',yaml:'yaml',yml:'yaml',toon:'toon',toml:'toml',js:'javascript',jsx:'javascript',ts:'typescript',tsx:'typescript',java:'java',kt:'kotlin',kts:'kotlin',swift:'swift',go:'go',rs:'rust',php:'php',cs:'csharp',c:'cpp',cc:'cpp',cpp:'cpp',cxx:'cpp',h:'cpp',hpp:'cpp',sql:'sql'};
  function languageForPath(path){const name=(path||'').split('/').pop()||'',dot=name.lastIndexOf('.');return dot>=0?(EXTENSIONS[name.slice(dot+1).toLowerCase()]||'text'):'text';}
  function appendToken(target,text,className=''){if(!text)return;if(!className){target.append(document.createTextNode(text));return;}const token=document.createElement('span');token.className=className;token.textContent=text;target.append(token);}
  function highlightLine(target,line,language){
    const pattern=/("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`|\/\/.*$|#.*$|\b(?:0x[\da-fA-F]+|\d+(?:\.\d+)?)\b|\b[A-Za-z_$][\w$]*\b|[{}\[\]().,:;+\-*\/%=<>!&|?]+)/g;
    let cursor=0,match;
    while((match=pattern.exec(line))!==null){if(match.index>cursor)appendToken(target,line.slice(cursor,match.index));const value=match[0];let cls='';
      if(value.startsWith('//')||(value.startsWith('#')&&HASH_COMMENT_LANGUAGES.has(language)))cls='tok-comment';
      else if(/^['"`]/.test(value))cls='tok-string';
      else if(/^(?:0x[\da-fA-F]+|\d)/.test(value))cls='tok-number';
      else if(KEYWORDS.has(value.toLowerCase()))cls='tok-keyword';
      else if(/^[A-Z][\w$]*$/.test(value))cls='tok-type';
      else if(/^[A-Za-z_$]/.test(value)&&line.slice(match.index+value.length).trimStart().startsWith('('))cls='tok-function';
      else if(/^[{}\[\]().,:;+\-*\/%=<>!&|?]+$/.test(value))cls='tok-operator';
      appendToken(target,value,cls);cursor=match.index+value.length;if(cls==='tok-comment'){cursor=line.length;break;}
    }
    if(cursor<line.length)appendToken(target,line.slice(cursor));if(!line.length)appendToken(target,' ');
  }
  document.getElementById('headerGraphCount').textContent = fmt(NODES.length)+' nodes · '+fmt(EDGES.length)+' edges';
  function switchTab(name){
    document.querySelectorAll('.tab').forEach(tab=>tab.classList.toggle('active',tab.dataset.tab===name));
    document.querySelectorAll('.pane').forEach(pane=>pane.classList.toggle('active',pane.dataset.pane===name));
  }
  document.querySelectorAll('.tab').forEach(tab=>tab.onclick=()=>switchTab(tab.dataset.tab));
  function openModal(){
    if(modalOpen)return;modalOpen=true;previousFocus=document.activeElement;modalBackdrop.classList.add('open');modalBackdrop.setAttribute('aria-hidden','false');requestAnimationFrame(()=>modalClose.focus());
  }
  function closeModal(){
    if(!modalOpen)return;modalOpen=false;modalBackdrop.classList.remove('open');modalBackdrop.setAttribute('aria-hidden','true');const target=previousFocus&&previousFocus.isConnected?previousFocus:canvas;requestAnimationFrame(()=>target.focus());
  }
  modalClose.onclick=closeModal;
  modalBackdrop.addEventListener('mousedown',event=>{if(event.target===modalBackdrop)closeModal();});
  const ADJ = new Map();
  const addAdj = (node, value) => { const rows=ADJ.get(node); rows ? rows.push(value) : ADJ.set(node,[value]); };
  EDGES.forEach((edge,index)=>{ addAdj(edge[0],[index,edge[1],1]); addAdj(edge[1],[index,edge[0],-1]); });
  let selectedLinks = [], selectedNeighbors = new Set();
  const GRID_SIZE = 96, SPATIAL = new Map(), NODES_BY_KIND = new Map();
  const cellKey = (x,y) => `${Math.floor(x/GRID_SIZE)},${Math.floor(y/GRID_SIZE)}`;
  NODES.forEach((node,index)=>{const key=cellKey(node[4],node[5]),cell=SPATIAL.get(key);cell?cell.push(index):SPATIAL.set(key,[index]);const group=NODES_BY_KIND.get(node[1]);group?group.push(index):NODES_BY_KIND.set(node[1],[index]);});

  function computeBounds() {
    let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
    for (const n of NODES) { minX=Math.min(minX,n[4]); minY=Math.min(minY,n[5]); maxX=Math.max(maxX,n[4]); maxY=Math.max(maxY,n[5]); }
    if(!NODES.length){minX=-1;minY=-1;maxX=1;maxY=1;}
    bounds={minX,minY,maxX,maxY};
  }
  function resize() {
    width=innerWidth; height=innerHeight; canvas.width=Math.round(width*dpr); canvas.height=Math.round(height*dpr); canvas.style.width=width+'px'; canvas.style.height=height+'px'; fit();
  }
  function fit() {
    const margin=Math.min(105,Math.max(24,Math.min(width,height)*.12)), usableWidth=Math.max(240,width), graphW=Math.max(1,bounds.maxX-bounds.minX), graphH=Math.max(1,bounds.maxY-bounds.minY);
    view.scale=Math.max(.006,Math.min(8,Math.min(Math.max(40,usableWidth-margin*2)/graphW,Math.max(40,height-margin*2)/graphH)));
    view.x=usableWidth/2-(bounds.minX+bounds.maxX)/2*view.scale;
    view.y=height/2-(bounds.minY+bounds.maxY)/2*view.scale; dirty=true;
  }
  function screen(n) { return [n[4]*view.scale+view.x,n[5]*view.scale+view.y]; }
  function world(sx,sy) { return [(sx-view.x)/view.scale,(sy-view.y)/view.scale]; }
  function zoomAt(factor,sx=width/2,sy=height/2) {
    const [wx,wy]=world(sx,sy); view.scale=Math.max(.006,Math.min(8,view.scale*factor)); view.x=sx-wx*view.scale; view.y=sy-wy*view.scale; dirty=true;
  }
  function draw() {
    if (!dirty) { requestAnimationFrame(draw); return; }
    dirty=false; ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,width,height);
    const minX=(0-view.x)/view.scale, maxX=(width-view.x)/view.scale, minY=(0-view.y)/view.scale, maxY=(height-view.y)/view.scale;
    ctx.save(); ctx.translate(view.x,view.y); ctx.scale(view.scale,view.scale);
    if (edgesVisible) {
      ctx.lineWidth=Math.max(.18/view.scale,.45); ctx.strokeStyle=selected>=0?'rgba(120,139,180,.025)':'rgba(120,139,180,.105)'; ctx.beginPath();
      for (const e of EDGES) { const a=NODES[e[0]],b=NODES[e[1]]; if(!visibleKinds.has(a[1])||!visibleKinds.has(b[1]))continue; if((a[4]<minX&&b[4]<minX)||(a[4]>maxX&&b[4]>maxX)||(a[5]<minY&&b[5]<minY)||(a[5]>maxY&&b[5]>maxY))continue; ctx.moveTo(a[4],a[5]);ctx.lineTo(b[4],b[5]); }
      ctx.stroke();
      if(selected>=0){
        ctx.lineWidth=1.5/view.scale;
        for(const link of selectedLinks){const edge=EDGES[link[0]],a=NODES[edge[0]],b=NODES[edge[1]];if(!visibleKinds.has(a[1])||!visibleKinds.has(b[1]))continue;ctx.strokeStyle=link[2]>0?'rgba(83,224,220,.9)':'rgba(190,134,255,.9)';ctx.beginPath();ctx.moveTo(a[4],a[5]);ctx.lineTo(b[4],b[5]);ctx.stroke();}
      }
    }
    for (const kind of Object.keys(NODE_COUNTS)) {
      if(!visibleKinds.has(kind))continue; const radius=Math.max(SIZES[kind]/view.scale,.5); ctx.fillStyle=COLORS[kind]||'#fff'; ctx.globalAlpha=selected>=0?.075:(kind==='occurrence'?.48:kind==='call'?.68:.9); ctx.beginPath();
      for (const index of NODES_BY_KIND.get(kind)||[]) { const n=NODES[index];if(n[4]<minX||n[4]>maxX||n[5]<minY||n[5]>maxY)continue; ctx.moveTo(n[4]+radius,n[5]);ctx.arc(n[4],n[5],radius,0,Math.PI*2); }
      ctx.fill();
    }
    ctx.globalAlpha=1;
    if(selected>=0){
      for(const index of selectedNeighbors){const n=NODES[index];if(!visibleKinds.has(n[1]))continue;const radius=Math.max((SIZES[n[1]]+1.5)/view.scale,.8);ctx.fillStyle=COLORS[n[1]]||'#fff';ctx.beginPath();ctx.arc(n[4],n[5],radius,0,Math.PI*2);ctx.fill();}
    }
    if(view.scale>.18) {
      ctx.font=`${Math.max(9/view.scale,10)}px ui-sans-serif,system-ui`; ctx.fillStyle='rgba(205,218,243,.72)'; let labels=0;
      for(const n of NODES){ if(labels>1100)break; if(!visibleKinds.has(n[1])||!['file','symbol','trace-hub'].includes(n[1])||n[4]<minX||n[4]>maxX||n[5]<minY||n[5]>maxY)continue; const label=n[1]==='file'?(n[2]||n[3]):n[3]; ctx.fillText(label.slice(0,70),n[4]+7/view.scale,n[5]-5/view.scale); labels++; }
    } else if(view.scale>.035) {
      ctx.font=`${11/view.scale}px ui-sans-serif,system-ui`; ctx.fillStyle='rgba(176,194,228,.34)';
      for(const r of ROOTS){ if(r[1]>=minX&&r[1]<=maxX&&r[2]>=minY&&r[2]<=maxY)ctx.fillText(r[0].toUpperCase(),r[1],r[2]); }
    }
    if(selected>=0){ const n=NODES[selected],radius=10/view.scale; ctx.fillStyle=COLORS[n[1]]||'#fff';ctx.beginPath();ctx.arc(n[4],n[5],Math.max((SIZES[n[1]]+2)/view.scale,1),0,Math.PI*2);ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=2/view.scale;ctx.beginPath();ctx.arc(n[4],n[5],radius,0,Math.PI*2);ctx.stroke(); }
    if(hovered>=0&&hovered!==selected){ const n=NODES[hovered],radius=7/view.scale;ctx.strokeStyle='rgba(255,255,255,.75)';ctx.lineWidth=1/view.scale;ctx.beginPath();ctx.arc(n[4],n[5],radius,0,Math.PI*2);ctx.stroke(); }
    ctx.restore(); document.getElementById('zoomValue').textContent=(view.scale*100).toFixed(view.scale<.1?1:0)+'%'; requestAnimationFrame(draw);
  }
  function nearest(sx,sy,maxPx=16){
    const [wx,wy]=world(sx,sy),limit=maxPx/view.scale,limit2=limit*limit,cellRadius=Math.min(32,Math.ceil(limit/GRID_SIZE));let best=-1,best2=limit2;
    const centerX=Math.floor(wx/GRID_SIZE),centerY=Math.floor(wy/GRID_SIZE);
    for(let gx=centerX-cellRadius;gx<=centerX+cellRadius;gx++)for(let gy=centerY-cellRadius;gy<=centerY+cellRadius;gy++)for(const i of SPATIAL.get(`${gx},${gy}`)||[]){const n=NODES[i];if(!visibleKinds.has(n[1]))continue;const dx=n[4]-wx,dy=n[5]-wy,d=dx*dx+dy*dy;if(d<best2){best=i;best2=d;}}
    return best;
  }
  function showHover(index,sx,sy){
    if(index<0||dragging){hoverCard.classList.remove('visible');hoverCard.setAttribute('aria-hidden','true');return;}
    const node=NODES[index];document.getElementById('hoverKind').textContent=node[1];document.getElementById('hoverTitle').textContent=node[3]||node[2]||node[0];document.getElementById('hoverPath').textContent=node[2]||'repository-level node';
    hoverCard.style.left=Math.max(8,Math.min(width-326,sx+14))+'px';hoverCard.style.top=Math.max(8,Math.min(height-86,sy+14))+'px';hoverCard.classList.add('visible');hoverCard.setAttribute('aria-hidden','false');
  }
  function renderConnections(index){
    const summary=document.getElementById('connectionSummary'),out=document.getElementById('connections');out.textContent='';
    const links=[...(ADJ.get(index)||[])].sort((a,b)=>{const ea=EDGES[a[0]],eb=EDGES[b[0]],na=NODES[a[1]],nb=NODES[b[1]];return ea[2].localeCompare(eb[2])||(na[3]||na[2]).localeCompare(nb[3]||nb[2]);});
    const incoming=links.filter(row=>row[2]<0).length,outgoing=links.length-incoming,byKind={};for(const row of links){const kind=EDGES[row[0]][2];byKind[kind]=(byKind[kind]||0)+1;}
    document.getElementById('relationCount').textContent=fmt(links.length);
    document.getElementById('incomingTotal').textContent=fmt(incoming);
    document.getElementById('outgoingTotal').textContent=fmt(outgoing);
    summary.textContent='';const main=document.createElement('span');main.className='summary-main';main.textContent=`${fmt(links.length)} direct relations · ${fmt(outgoing)} outgoing · ${fmt(incoming)} incoming`;summary.append(main);for(const [kind,count] of Object.entries(byKind)){const token=document.createElement('span');token.className='summary-token';token.textContent=`${kind} ${count}`;summary.append(token);}
    if(!links.length){const empty=document.createElement('div');empty.className='empty';empty.textContent='This node has no direct graph edges';out.append(empty);return;}
    const fragment=document.createDocumentFragment();
    for(const row of links){const edge=EDGES[row[0]],node=NODES[row[1]],item=document.createElement('button');item.type='button';item.className='connection';const direction=document.createElement('span');direction.className='direction';direction.textContent=row[2]>0?'→':'←';direction.title=row[2]>0?'Outgoing relation':'Incoming relation';const edgeKind=document.createElement('span');edgeKind.className='edge-kind relation-'+edge[2].replace(/[^a-z0-9-]/gi,'-').toLowerCase();edgeKind.textContent=edge[2];edgeKind.title=edge[3]||edge[2];const target=document.createElement('span');target.className='target';const title=document.createElement('b');title.textContent=node[3]||node[2]||node[0];const path=document.createElement('small');path.append(edgeKind,document.createTextNode(' · '+node[1]+' · '+(node[2]||'repository')));target.append(title,path);const chevron=document.createElement('span');chevron.className='chevron';chevron.textContent='›';chevron.setAttribute('aria-hidden','true');item.append(direction,target,chevron);item.setAttribute('aria-label',(row[2]>0?'Outgoing ':'Incoming ')+edge[2]+' relation to '+title.textContent);item.onclick=()=>setSelection(row[1],true);fragment.append(item);}
    out.append(fragment);
  }
  function renderCode(node){
    const meta=document.getElementById('codeMeta'),out=document.getElementById('codeView');meta.textContent='';out.textContent='';const source=SOURCES[node[2]];
    if(!source){document.getElementById('sourceState').textContent=sourceTotal?'Unavailable':'Not embedded';meta.textContent=sourceTotal?'No indexed source file for this node':'Source content was not embedded';const empty=document.createElement('div');empty.className='empty';empty.textContent=node[1]==='trace-hub'?'Trace hubs connect evidence but do not own source code.':sourceTotal?'Source is unavailable in this graph snapshot.':'Generate again with visualize --include-source to inspect code locally.';out.append(empty);return;}
    const lines=source[0].replace(/\r\n?/g,'\n').split('\n'),fresh=source[1],rawStart=Number(node[6]||1),rawEnd=Number(node[7]||rawStart),rangeStart=Math.max(1,rawStart),rangeEnd=Math.max(rangeStart,Math.min(lines.length,rawEnd));
    const shownStart=node[1]==='file'?1:Math.max(1,rangeStart-20),shownEnd=node[1]==='file'?lines.length:Math.min(lines.length,rangeEnd+20);
    document.getElementById('sourceState').textContent=fresh?'Fresh':'Drifted';const language=languageForPath(node[2]),location=document.createElement('span');location.textContent=`${language} · ${node[2]}:${rangeStart}–${rangeEnd} · showing ${shownStart}–${shownEnd}`;const status=document.createElement('span');status.className=fresh?'fresh':'stale';status.textContent=fresh?'source hash matches':'current source differs from snapshot';meta.append(status,location);
    const fragment=document.createDocumentFragment();for(let line=shownStart;line<=shownEnd;line++){const row=document.createElement('div');row.className='code-line'+(line>=rangeStart&&line<=rangeEnd?' active':'');const number=document.createElement('span');number.className='ln';number.textContent=line;const code=document.createElement('span');code.className='src';highlightLine(code,lines[line-1]||'',language);row.append(number,code);fragment.append(row);}out.append(fragment);const active=out.querySelector('.active');if(active)requestAnimationFrame(()=>active.scrollIntoView({block:'center'}));
  }
  function setSelection(index,focus=false){
    selected=index;selectedLinks=index>=0?[...(ADJ.get(index)||[])]:[];selectedNeighbors=new Set(selectedLinks.map(row=>row[1]));const out=document.getElementById('selection');
    if(index<0){closeModal();document.getElementById('inspectorKind').textContent='Node inspector';document.getElementById('inspectorTitle').textContent='Explore repository context';document.getElementById('inspectorPath').textContent='Select a node to inspect its repository context.';out.textContent='Select any node in the graph';document.getElementById('relationCount').textContent='0';document.getElementById('incomingTotal').textContent='0';document.getElementById('outgoingTotal').textContent='0';document.getElementById('sourceState').textContent='—';document.getElementById('connectionSummary').textContent='Select a node to inspect its relations.';const relationEmpty=document.createElement('div');relationEmpty.className='empty';relationEmpty.textContent='No node selected';document.getElementById('connections').replaceChildren(relationEmpty);document.getElementById('codeMeta').textContent='Select a code-backed node.';const codeEmpty=document.createElement('div');codeEmpty.className='empty';codeEmpty.textContent='Source preview will appear here';document.getElementById('codeView').replaceChildren(codeEmpty);dirty=true;return;}
    const wasOpen=modalOpen,n=NODES[index],nodeTitle=n[3]||n[2]||n[0],nodePath=n[2]||'repository-level node';document.getElementById('inspectorKind').textContent=n[1]+' node';document.getElementById('inspectorTitle').textContent=nodeTitle;document.getElementById('inspectorPath').textContent=nodePath;out.textContent='';for(const [label,value] of [['Node ID',n[0]],['Type',n[1]],['Path',nodePath],['Lines',(n[6]||'—')+'–'+(n[7]||'—')]]){const item=document.createElement('div');item.className='property-row';const key=document.createElement('span');key.textContent=label;const data=document.createElement('code');data.textContent=value;data.title=value;item.append(key,data);out.append(item);}renderConnections(index);renderCode(n);if(focus){view.scale=Math.max(view.scale,.85);view.x=width*.5-n[4]*view.scale;view.y=height*.5-n[5]*view.scale;}if(!wasOpen)switchTab('overview');openModal();dirty=true;
  }
  canvas.addEventListener('wheel',e=>{e.preventDefault();zoomAt(Math.exp(-e.deltaY*.0015),e.clientX,e.clientY);},{passive:false});
  canvas.addEventListener('mousedown',e=>{dragging=true;moved=false;lastX=e.clientX;lastY=e.clientY;hoverCard.classList.remove('visible');canvas.classList.add('dragging');});
  addEventListener('mousemove',e=>{if(dragging){const dx=e.clientX-lastX,dy=e.clientY-lastY;if(Math.abs(dx)+Math.abs(dy)>2)moved=true;view.x+=dx;view.y+=dy;lastX=e.clientX;lastY=e.clientY;dirty=true;}else{hoverX=e.clientX;hoverY=e.clientY;if(!hoverFrame)hoverFrame=requestAnimationFrame(()=>{hoverFrame=0;const next=nearest(hoverX,hoverY,10);if(next!==hovered){hovered=next;dirty=true;}showHover(next,hoverX,hoverY);});}});
  addEventListener('mouseup',e=>{if(dragging&&!moved)setSelection(nearest(e.clientX,e.clientY));dragging=false;canvas.classList.remove('dragging');showHover(hovered,e.clientX,e.clientY);});
  canvas.addEventListener('dblclick',e=>setSelection(nearest(e.clientX,e.clientY),true));
  document.getElementById('plus').onclick=()=>zoomAt(1.5);document.getElementById('minus').onclick=()=>zoomAt(1/1.5);document.getElementById('reset').onclick=fit;
  const toggles=document.getElementById('nodeToggles');
  for(const kind of Object.keys(NODE_COUNTS)){const row=document.createElement('button');row.type='button';row.className='control-button';row.setAttribute('aria-pressed','true');const dot=document.createElement('span');dot.className='dot';dot.style.color=COLORS[kind]||'#fff';dot.style.background=COLORS[kind]||'#fff';const label=document.createElement('span');label.textContent=kind;const count=document.createElement('span');count.className='count';count.textContent=fmt(NODE_COUNTS[kind]);row.append(dot,label,count);row.onclick=()=>{visibleKinds.has(kind)?visibleKinds.delete(kind):visibleKinds.add(kind);const enabled=visibleKinds.has(kind);row.classList.toggle('off',!enabled);row.setAttribute('aria-pressed',String(enabled));dirty=true;};toggles.append(row);}
  document.getElementById('edgeToggle').onclick=function(){edgesVisible=!edgesVisible;this.classList.toggle('off',!edgesVisible);this.setAttribute('aria-pressed',String(edgesVisible));dirty=true;};
  const search=document.getElementById('search'),results=document.getElementById('results');let timer;
  search.oninput=()=>{clearTimeout(timer);timer=setTimeout(()=>{const q=search.value.trim().toLowerCase();results.textContent='';if(!q){results.style.display='none';return;}const hits=[];for(let i=0;i<NODES.length&&hits.length<30;i++){const n=NODES[i];if((n[2]+' '+n[3]).toLowerCase().includes(q))hits.push(i);}for(const i of hits){const n=NODES[i],row=document.createElement('div');row.className='result';const b=document.createElement('b');b.textContent=n[3]||n[2];const s=document.createElement('small');s.textContent=n[1]+' · '+(n[2]||'repository');row.append(b,s);row.onclick=()=>{setSelection(i,true);results.style.display='none';};results.append(row);}results.style.display=hits.length?'block':'none';},90);};
  addEventListener('keydown',e=>{if(e.key==='Tab'&&modalOpen){const focusable=[...inspectorModal.querySelectorAll('button:not([disabled]),input:not([disabled]),[tabindex]:not([tabindex="-1"])')];if(focusable.length){const first=focusable[0],last=focusable[focusable.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}}if(e.key==='Escape'){results.style.display='none';search.blur();closeModal();}if((e.metaKey||e.ctrlKey)&&e.key==='f'&&!modalOpen){e.preventDefault();search.focus();}});
  computeBounds();addEventListener('resize',resize);resize();requestAnimationFrame(draw);
  </script>
</body>
</html>'''


def render(
    root: Path,
    database: Path,
    output: Path,
    *,
    include_source: bool = False,
) -> dict[str, object]:
    """Render one deterministic self-contained graph viewer atomically."""
    nodes, edges, node_counts, edge_counts, root_labels, sources = load_graph(
        database, root, include_source=include_source
    )
    html = (
        HTML.replace("{{NODES}}", safe_json(nodes))
        .replace("{{EDGES}}", safe_json(edges))
        .replace("{{NODE_COUNTS}}", safe_json(node_counts))
        .replace("{{EDGE_COUNTS}}", safe_json(edge_counts))
        .replace("{{ROOTS}}", safe_json(root_labels))
        .replace("{{SOURCES}}", safe_json(sources))
        .replace("{{EDGE_TOTAL}}", f"{len(edges):,}")
    )
    data = html.encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=output.parent, prefix=".context-graph-", suffix=".html"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(0o600)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()
    return {
        "schema": VIEW_SCHEMA,
        "nodes": len(nodes),
        "edges": len(edges),
        "paths": len({str(node[2]) for node in nodes if node[2]}),
        "source_files": len(sources),
        "stale_source_files": sum(1 for value in sources.values() if not value[1]),
        "include_source": include_source,
        "bytes": len(data),
        "content_sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Imported helper; use context_cache.py visualize."
    )
    parser.parse_args()
    print("Use context_cache.py visualize to generate a graph viewer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
