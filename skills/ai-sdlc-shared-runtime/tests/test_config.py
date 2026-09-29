#!/usr/bin/env python3
"""Tests for deterministic layered AI SDLC configuration."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
import sys
from pathlib import Path

_TOON_RUNTIME = Path(__file__).resolve().parents[2] / "ai-sdlc-shared-runtime" / "scripts"
if str(_TOON_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_TOON_RUNTIME))
import ai_sdlc_toon as toon_codec  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_config.py"
DEFAULTS = ROOT / "skills/ai-sdlc-shared-runtime/references/ai-sdlc.defaults.toon"


def write(path: Path, values: dict[str, object], protected: list[str] | None = None) -> None:
    """Write one configuration layer."""
    payload: dict[str, object] = {"schema": "ai-sdlc-config/v1", "values": values}
    if protected is not None:
        payload["protected"] = protected
    path.write_text(toon_codec.dumps(payload), encoding="utf-8")


class ConfigTests(unittest.TestCase):
    """Precedence, provenance, determinism, and gate safety tests."""

    def run_config(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the resolver with captured output."""
        return subprocess.run(["python3", str(SCRIPT), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_precedence_and_provenance_are_deterministic(self) -> None:
        """User values should win normal settings with exact provenance."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            team, user = root / "team.toon", root / "user.toon"
            write(team, {"output": {"human": "html"}, "modules": {"enabled": ["architecture"]}})
            write(user, {"output": {"human": "markdown"}, "modules": {"enabled": ["research"]}})
            args = ("--base", str(DEFAULTS), "--team", str(team), "--user", str(user), "--format", "toon")
            first, second = self.run_config(*args), self.run_config(*args)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            value = toon_codec.loads(first.stdout)
            self.assertEqual(value["values"]["modules"]["enabled"], ["research"])
            self.assertEqual(value["provenance"]["modules.enabled"], "user")

    def test_protected_boolean_cannot_be_weakened(self) -> None:
        """User configuration must not disable a required gate."""
        with tempfile.TemporaryDirectory() as temp:
            base, user = Path(temp) / "base.toon", Path(temp) / "user.toon"
            write(base, {"gates": {"require_traceability": True}}, ["gates.require_traceability"])
            write(user, {"gates": {"require_traceability": False}})
            result = self.run_config("--base", str(base), "--user", str(user))
            self.assertEqual(result.returncode, 1)
            self.assertIn("weakens protected gate gates.require_traceability", result.stdout)

    def test_protected_rigor_can_strengthen_but_not_downgrade(self) -> None:
        """Strictness order should allow strengthening across layers."""
        with tempfile.TemporaryDirectory() as temp:
            base, team, user = Path(temp) / "base.toon", Path(temp) / "team.toon", Path(temp) / "user.toon"
            write(base, {"rigor": {"minimum_profile": "patch"}}, ["rigor.minimum_profile"])
            write(team, {"rigor": {"minimum_profile": "assured"}})
            write(user, {"rigor": {"minimum_profile": "patch"}})
            blocked = self.run_config("--base", str(base), "--team", str(team), "--user", str(user))
            self.assertEqual(blocked.returncode, 1)
            self.assertIn("assured", blocked.stdout)
            allowed = self.run_config("--base", str(base), "--team", str(team), "--format", "toon")
            self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)
            value = toon_codec.loads(allowed.stdout)
            self.assertEqual(value["values"]["rigor"]["minimum_profile"], "assured")
            self.assertEqual(value["provenance"]["rigor.minimum_profile"], "team")
            self.assertIn("rigor.minimum_profile", value["protected"])

    def test_user_can_set_typed_interaction_preferences(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.toon"
            write(user, {"interaction": {
                "enabled": True,
                "preferred_name": "Mike",
                "language": "en",
                "response_style": "concise",
                "technical_depth": "practitioner",
                "status_updates": "milestones",
            }})
            result = self.run_config("--base", str(DEFAULTS), "--user", str(user), "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            value = toon_codec.loads(result.stdout)
            self.assertEqual(value["values"]["interaction"]["preferred_name"], "Mike")
            self.assertEqual(value["values"]["interaction"]["response_style"], "concise")
            self.assertEqual(value["provenance"]["interaction.preferred_name"], "user")
            self.assertNotIn("interaction.preferred_name", value["protected"])

    def test_packaged_defaults_are_implicit(self) -> None:
        result = self.run_config("--format", "toon")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        value = toon_codec.loads(result.stdout)
        self.assertEqual(value["values"]["interaction"]["response_style"], "balanced")

    def test_invalid_interaction_preference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.toon"
            invalid = [
                ({"response_style": "telepathic"}, "interaction.response_style must be one of"),
                ({"language": " en "}, "interaction.language must be auto or a simple BCP-47 language tag"),
                ({"preferred_name": " " * 81}, "interaction.preferred_name must be a control-free string"),
            ]
            for values, expected in invalid:
                with self.subTest(values=values):
                    write(user, {"interaction": {"enabled": True, **values}})
                    result = self.run_config("--base", str(DEFAULTS), "--user", str(user))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(expected, result.stdout)

    def test_non_base_layer_cannot_redefine_protection(self) -> None:
        """Protection ownership remains in the base contract."""
        with tempfile.TemporaryDirectory() as temp:
            team = Path(temp) / "team.toon"
            write(team, {}, protected=[])
            result = self.run_config("--base", str(DEFAULTS), "--team", str(team))
            self.assertEqual(result.returncode, 1)
            self.assertIn("cannot redefine protected paths", result.stdout)

    def test_flow_configuration_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.toon"
            write(user, {"flow": {
                "role_aliases": {"builder": "software-engineer"},
                "menu_mode": "always",
                "context_selectors": [{
                    "id": "implementation-contract",
                    "roles": ["software-engineer"],
                    "actions": ["implementation", "engineering_quality_gate"],
                    "include": ["references/flow-contract.md"],
                    "priority": 75,
                    "max_tokens": 1200,
                    "reason": "implementation routing contract",
                }],
            }})
            result = self.run_config("--base", str(DEFAULTS), "--user", str(user), "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            values = toon_codec.loads(result.stdout)["values"]["flow"]
            self.assertEqual(values["role_aliases"]["builder"], "software-engineer")

    def test_flow_configuration_rejects_unknown_and_out_of_range_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.toon"
            cases = (
                ({"flow": {"role": "software-engineer"}}, "flow has unknown fields: role"),
                ({"flow": {"menu_mode": "never"}}, "flow.menu_mode must be one of"),
                ({"flow": {"context_selectors": [{
                    "id": "bad", "roles": [], "actions": [], "include": [],
                    "priority": 101, "max_tokens": 4, "reason": "too short",
                }]}}, "priority must be an integer from 0 to 100"),
                ({"flow": {"context_selectors": [{
                    "id": "bad-role", "roles": ["super-user"],
                    "actions": ["implementation"],
                    "include": ["references/flow-contract.md"],
                    "priority": 50, "max_tokens": 200,
                    "reason": "unknown role must fail closed",
                }]}}, "roles has unknown roles: super-user"),
                ({"flow": {"context_selectors": [{
                    "id": "bad-path", "roles": ["software-engineer"],
                    "actions": ["implementation"], "include": ["../secret"],
                    "priority": 50, "max_tokens": 200,
                    "reason": "escaping path must fail closed",
                }]}}, "include has unsafe flow-package path"),
            )
            for values, expected in cases:
                with self.subTest(expected=expected):
                    write(user, values)
                    result = self.run_config("--base", str(DEFAULTS), "--user", str(user))
                    self.assertEqual(result.returncode, 1)
                    self.assertIn(expected, result.stdout)

    def test_explicit_missing_layer_is_not_silently_ignored(self) -> None:
        """A configured layer path must exist so provenance stays honest."""
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "team.toon"
            result = self.run_config("--base", str(DEFAULTS), "--team", str(missing))
            self.assertEqual(result.returncode, 1)
            self.assertIn("team config does not exist", result.stdout)

    def test_user_identity_configuration_resolves(self) -> None:
        """User can specify name, email, role, and git details."""
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.toon"
            write(user, {"user": {
                "name": "Jane Developer",
                "email": "jane@example.com",
                "role": "software-engineer",
                "git": {"name": "Jane D", "email": "janed@example.com"},
            }})
            result = self.run_config("--base", str(DEFAULTS), "--user", str(user), "--format", "toon")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            values = toon_codec.loads(result.stdout)["values"]
            self.assertEqual(values["user"]["name"], "Jane Developer")
            self.assertEqual(values["user"]["email"], "jane@example.com")
            self.assertEqual(values["user"]["role"], "software-engineer")
            self.assertEqual(values["user"]["git"]["name"], "Jane D")

    def test_user_identity_rejects_invalid_roles_and_fields(self) -> None:
        """Invalid user roles and unknown fields fail closed."""
        with tempfile.TemporaryDirectory() as temp:
            user = Path(temp) / "user.toon"
            cases = [
                ({"user": {"role": "invalid-role"}}, "user.role must be one of"),
                ({"user": {"unknown_field": "val"}}, "user has unknown fields: unknown_field"),
                ({"user": {"name": 123}}, "user.name must be a string"),
            ]
            for val, err in cases:
                with self.subTest(err=err):
                    write(user, val)
                    res = self.run_config("--base", str(DEFAULTS), "--user", str(user))
                    self.assertEqual(res.returncode, 1)
                    self.assertIn(err, res.stdout)

    def test_user_configuration_auto_discovery(self) -> None:
        """Resolver auto-discovers .customization.toon when --user is not passed."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            customization = root / ".customization.toon"
            write(customization, {"user": {"name": "Auto Discovered", "role": "product-owner"}})
            # Pass write-root pointing to temp directory where .customization.toon lives
            res = self.run_config("--base", str(DEFAULTS), "--write-root", str(root), "--format", "toon")
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            data = toon_codec.loads(res.stdout)
            self.assertEqual(data["values"]["user"]["name"], "Auto Discovered")
            self.assertEqual(data["values"]["user"]["role"], "product-owner")


if __name__ == "__main__":
    unittest.main()
