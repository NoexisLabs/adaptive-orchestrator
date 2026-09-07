#!/usr/bin/env python3
"""Repository validation for Adaptive Orchestrator."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_AGENTS = {
    "orchestrator": {"model": "fable", "effort": "high", "maxTurns": 40},
    "advisor": {"model": "opus", "effort": "high", "maxTurns": 15},
    "domain-logic-auditor": {"model": "fable", "effort": "high", "maxTurns": 18},
    "security-auditor": {"model": "opus", "effort": "high", "maxTurns": 18},
    "backend-engineer": {"model": "sonnet", "effort": "medium", "maxTurns": 30},
    "frontend-engineer": {"model": "sonnet", "effort": "medium", "maxTurns": 30},
    "test-engineer": {"model": "sonnet", "effort": "medium", "maxTurns": 20},
    "repository-explorer": {"model": "haiku", "effort": "low", "maxTurns": 10},
    "isolated-implementer": {"model": "sonnet", "effort": "medium", "maxTurns": 30},
}

READ_ONLY_AGENTS = {
    "advisor",
    "domain-logic-auditor",
    "security-auditor",
    "repository-explorer",
}

EXPECTED_SKILLS = {"orchestrate", "review", "audit"}
ALLOWED_MODELS = {"fable", "opus", "sonnet", "haiku", "inherit"}
ALLOWED_EFFORT = {"low", "medium", "high", "xhigh", "max"}
READ_ONLY_TOOLS = {"Read", "Grep", "Glob"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(errors, f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}


def parse_frontmatter(path: Path, errors: list[str]) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(errors, f"{path.relative_to(ROOT)}: frontmatter must start on line 1")
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(errors, f"{path.relative_to(ROOT)}: missing closing frontmatter marker")
        return {}
    raw = text[4:end]
    try:
        data = yaml.safe_load(raw) or {}
    except Exception as exc:
        fail(errors, f"{path.relative_to(ROOT)}: invalid YAML frontmatter: {exc}")
        return {}
    if not isinstance(data, dict):
        fail(errors, f"{path.relative_to(ROOT)}: frontmatter must be a mapping")
        return {}
    return data


def normalize_tools(value: object) -> set[str]:
    if isinstance(value, list):
        return {str(item).strip() for item in value if str(item).strip()}
    if isinstance(value, str):
        return {item.strip() for item in value.split(",") if item.strip()}
    return set()


def validate_agents(errors: list[str]) -> None:
    agents_dir = ROOT / "agents"
    found: set[str] = set()

    for path in sorted(agents_dir.glob("*.md")):
        fm = parse_frontmatter(path, errors)
        name = fm.get("name")
        if not isinstance(name, str) or not name:
            fail(errors, f"{path.relative_to(ROOT)}: missing agent name")
            continue
        found.add(name)
        if not fm.get("description"):
            fail(errors, f"{path.relative_to(ROOT)}: missing description")

        model = fm.get("model", "inherit")
        if model not in ALLOWED_MODELS:
            fail(errors, f"{path.relative_to(ROOT)}: unsupported model alias {model!r}")

        effort = fm.get("effort")
        if effort not in ALLOWED_EFFORT:
            fail(errors, f"{path.relative_to(ROOT)}: invalid/missing effort {effort!r}")

        max_turns = fm.get("maxTurns")
        if not isinstance(max_turns, int) or max_turns <= 0:
            fail(errors, f"{path.relative_to(ROOT)}: maxTurns must be a positive integer")

        expected = EXPECTED_AGENTS.get(name)
        if expected:
            for key, value in expected.items():
                if fm.get(key) != value:
                    fail(errors, f"{path.relative_to(ROOT)}: {key}={fm.get(key)!r}, expected {value!r}")

        if name in READ_ONLY_AGENTS:
            tools = normalize_tools(fm.get("tools"))
            if tools != READ_ONLY_TOOLS:
                fail(errors, f"{path.relative_to(ROOT)}: read-only tools must be exactly {sorted(READ_ONLY_TOOLS)}")

        if name == "isolated-implementer" and fm.get("isolation") != "worktree":
            fail(errors, f"{path.relative_to(ROOT)}: isolated-implementer must use isolation: worktree")

    missing = set(EXPECTED_AGENTS) - found
    extra = found - set(EXPECTED_AGENTS)
    if missing:
        fail(errors, f"Missing expected agents: {sorted(missing)}")
    if extra:
        fail(errors, f"Unexpected agents not covered by validator: {sorted(extra)}")


def validate_skills(errors: list[str]) -> None:
    skills_dir = ROOT / "skills"
    found: set[str] = set()
    for path in sorted(skills_dir.glob("*/SKILL.md")):
        fm = parse_frontmatter(path, errors)
        name = fm.get("name") or path.parent.name
        if not isinstance(name, str) or not name:
            fail(errors, f"{path.relative_to(ROOT)}: invalid skill name")
            continue
        found.add(name)
        if not fm.get("description"):
            fail(errors, f"{path.relative_to(ROOT)}: missing skill description")

    missing = EXPECTED_SKILLS - found
    if missing:
        fail(errors, f"Missing expected skills: {sorted(missing)}")


def validate_versions(errors: list[str]) -> None:
    plugin = load_json(ROOT / ".claude-plugin" / "plugin.json", errors)
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json", errors)
    plugins = marketplace.get("plugins") if isinstance(marketplace, dict) else None
    entry = plugins[0] if isinstance(plugins, list) and plugins else {}

    if plugin.get("name") != "adaptive-orchestrator":
        fail(errors, "plugin.json: unexpected plugin name")
    if entry.get("name") != plugin.get("name"):
        fail(errors, "marketplace plugin name does not match plugin.json")
    if entry.get("version") != plugin.get("version"):
        fail(errors, f"version mismatch: plugin={plugin.get('version')!r}, marketplace={entry.get('version')!r}")


def validate_readme(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required = [
        "/plugin marketplace add NoexisLabs/adaptive-orchestrator",
        "/plugin install adaptive-orchestrator@adaptive-orchestrator-marketplace",
        "/adaptive-orchestrator:orchestrate",
        "/adaptive-orchestrator:review",
        "/adaptive-orchestrator:audit",
    ]
    for text in required:
        if text not in readme:
            fail(errors, f"README.md: missing required text {text!r}")


def validate_no_dated_model_ids(errors: list[str]) -> None:
    pattern = re.compile(r"claude-(?:fable|opus|sonnet|haiku)-\d", re.IGNORECASE)
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".yml", ".yaml", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if pattern.search(text):
            fail(errors, f"{path.relative_to(ROOT)}: contains a dated/full Claude model ID; use family aliases")


def main() -> int:
    errors: list[str] = []
    validate_versions(errors)
    validate_agents(errors)
    validate_skills(errors)
    validate_readme(errors)
    validate_no_dated_model_ids(errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("Adaptive Orchestrator validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
