#!/usr/bin/env python3
"""Measure actual Explore I/O and elapsed time; not end-to-end model latency."""
import argparse
import statistics
import sys
import time
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/ai-sdlc-shared-runtime/scripts"))
import ai_sdlc_flow as flow
from ai_sdlc_toon import encode_toon, decode_toon


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    if args.repeats < 1: parser.error("repeats must be positive")
    rows = []
    original = Path.read_bytes
    for intent in ["fix a tiny bug", "change documentation", "implement a localized feature", "implement architecture migration"]:
        samples = []
        for _ in range(args.repeats):
            reads = []
            def tracked(path):
                data = original(path); reads.append((str(path), len(data))); return data
            started = time.perf_counter()
            with patch.object(Path, "read_bytes", tracked):
                card = flow.build_card(root=ROOT, intent=intent, feature="025-adaptive-execution", requested_action="implementation")
            samples.append({"seconds": time.perf_counter()-started, "reads":len(reads),
                            "bytes":sum(n for _,n in reads), "duplicate_reads":len(reads)-len(set(p for p,_ in reads)),
                            "stages":len(card.run_plan.get("tasks", [])), "selected_context_tokens":card.context_economics.packed_tokens,
                            "blockers":list(card.blockers)})
            if card.blockers: raise RuntimeError(card.blockers)
        rows.append({"task":intent,"median_seconds":statistics.median(s["seconds"] for s in samples),
                     "sample":samples[len(samples)//2], "model_calls":0, "verification_calls":0})
    report = {"schema":"ai-sdlc-adaptive-benchmark/v1", "scope":"actual Explore helper; no model/provider execution",
              "python":sys.version.split()[0], "repeats":args.repeats, "samples":rows}
    result = encode_toon(report)
    if args.output: args.output.write_text(result)
    print(result, end="")

if __name__ == "__main__": main()
