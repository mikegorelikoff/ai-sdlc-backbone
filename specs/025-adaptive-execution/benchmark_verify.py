#!/usr/bin/env python3
"""Compare serial/parallel execution of identical real Loop regression checks."""
import shlex
import statistics
import sys
import tempfile
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
LOOP = ROOT / "products/ai-sdlc-loop"
sys.path.insert(0, str(LOOP))
from tests.helpers import init_repo, run_cli, read_toon, create_quality_gate
from toon import encode_toon

rows = []
for jobs in (1, 3):
    samples = []
    for _ in range(3):
        with tempfile.TemporaryDirectory() as tmp:
            repo = init_repo(Path(tmp) / "repo")
            run_cli(repo, "specify", "--feature", "demo", "--request", "Fix a tiny fixture bug", "--allow", "app.txt")
            spec = read_toon(repo / ".ai-sdlc-loop/demo/spec.toon")
            run_cli(repo, "approve", "--feature", "demo", "--action", "implement", "--decision", "approve", "--fingerprint", spec["fingerprint"], "--reviewer", "benchmark fixture")
            (repo / "app.txt").write_text("after\n")
            create_quality_gate(repo)
            args = ["verify", "--feature", "demo", "--jobs", str(jobs)]
            if jobs > 1: args += ["--independent"]
            for module in ["tests.test_toon", "tests.test_skill_graphs", "tests.test_requirements_discovery"]:
                code = "import sys,unittest;sys.path.insert(0," + repr(str(LOOP)) + ");suite=unittest.defaultTestLoader.loadTestsFromName(" + repr(module) + ");result=unittest.TextTestRunner().run(suite);sys.exit(not result.wasSuccessful())"
                args += ["--command", shlex.join([sys.executable, "-c", code])]
            started = time.perf_counter()
            run_cli(repo, *args)
            elapsed = time.perf_counter()-started
            evidence = read_toon(repo / ".ai-sdlc-loop/demo/evidence.toon")
            samples.append({"seconds":elapsed,"exits":[r["exit_code"] for r in evidence["commands"]],"commands":len(evidence["commands"])})
    rows.append({"jobs":jobs,"median_seconds":statistics.median(s["seconds"] for s in samples),"samples":samples})
report = {"schema":"ai-sdlc-adaptive-verification-benchmark/v1", "scope":"serial versus parallel ablation on current runner; identical real tests, fixture source; setup excluded", "model_calls":0,"results":rows}
text=encode_toon(report)
(ROOT / "specs/025-adaptive-execution/_ai_sdlc/verification-benchmark.toon").write_text(text)
print(text,end="")
