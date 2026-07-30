#!/usr/bin/env python3
"""Verify TOON contracts against the executable v4 harness fields."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[3]
SHARED = REPO_ROOT / "skills" / "ai-sdlc-shared-runtime" / "scripts"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from ai_sdlc_step_context import StepContextPack  # noqa: E402
import ai_sdlc_steps as steps_runtime  # noqa: E402
from ai_sdlc_toon import decode_toon  # noqa: E402


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runtime = load_module(
    "v4_runtime_contract",
    REPO_ROOT / "skills" / "ai-sdlc-runtime" / "scripts" / "runtime.py",
)
workflow = load_module(
    "v4_workflow_contract",
    REPO_ROOT / "skills" / "ai-sdlc-workflow" / "scripts" / "workflow.py",
)
adapter = load_module(
    "v4_adapter_contract",
    REPO_ROOT / "skills" / "ai-sdlc-host-adapter" / "scripts" / "adapter.py",
)


def contract(relative: str) -> dict[str, object]:
    value = decode_toon((REPO_ROOT / relative).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class V4ContractTests(unittest.TestCase):
    def test_every_reference_contract_is_decodable_toon(self) -> None:
        paths = sorted(
            (REPO_ROOT / "skills").glob("*/references/*.schema.toon")
        )
        self.assertGreater(len(paths), 20)
        for path in paths:
            with self.subTest(path=path):
                value = decode_toon(path.read_text(encoding="utf-8"))
                self.assertIsInstance(value, dict)
                self.assertEqual(
                    value.get("$schema"),
                    "ai-sdlc-toon-contract/v1",
                )

    def test_runtime_contract_fields_match_executable_runtime(self) -> None:
        plan = contract(
            "skills/ai-sdlc-runtime/references/run-plan.schema.toon"
        )
        event = contract(
            "skills/ai-sdlc-runtime/references/run-event.schema.toon"
        )
        self.assertEqual(set(plan["required"]), runtime.PLAN_FIELDS)
        self.assertEqual(set(event["required"]), runtime.EVENT_FIELDS)
        self.assertEqual(
            set(event["properties"]["type"]["enum"]),
            runtime.EVENT_TYPES,
        )

    def test_graph_stepcard_and_context_contract_fields_match(self) -> None:
        graph = contract(
            "skills/ai-sdlc-shared-runtime/references/skill-steps.schema.toon"
        )
        card = contract(
            "skills/ai-sdlc-shared-runtime/references/step-card.schema.toon"
        )
        context = contract(
            "skills/ai-sdlc-shared-runtime/references/"
            "step-context-pack.schema.toon"
        )
        self.assertEqual(set(graph["required"]), steps_runtime.TOP_FIELDS)
        self.assertEqual(set(card["required"]), adapter.STEP_CARD_FIELDS)
        self.assertEqual(
            set(context["required"]),
            set(StepContextPack.__dataclass_fields__),
        )

    def test_workflow_and_adapter_request_contract_fields_match(self) -> None:
        workflow_contract = contract(
            "skills/ai-sdlc-workflow/references/workflow.schema.toon"
        )
        request = contract(
            "skills/ai-sdlc-host-adapter/references/"
            "capability-request.schema.toon"
        )
        self.assertEqual(
            set(workflow_contract["required"]),
            workflow.WORKFLOW_FIELDS,
        )
        self.assertEqual(set(request["required"]), adapter.REQUEST_FIELDS)


if __name__ == "__main__":
    unittest.main()
