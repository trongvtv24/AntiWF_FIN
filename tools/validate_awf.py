#!/usr/bin/env python3
"""Validate AWF repositories with AWF extended metadata."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("Missing dependency: PyYAML is required to parse AWF YAML.") from exc

try:
    import jsonschema
except ImportError:  # pragma: no cover - optional dependency
    jsonschema = None


RISK_LEVELS = {"low", "medium", "high", "critical"}
PRIORITIES = {"low", "medium", "high"}
ACTIVATIONS = {
    "advisory",
    "automatic",
    "automatic_or_explicit",
    "conditional",
    "explicit",
    "explicit_or_confirmed",
    "explicit_or_intent",
    "intent",
    "required_for_ui",
}

WORKFLOW_REQUIRED_KEYS = {
    "command",
    "name",
    "path",
    "category",
    "priority",
    "risk_level",
    "triggers",
    "next_workflows",
    "required_gates",
    "required_skills",
    "conditional_skills",
}

SKILL_REQUIRED_KEYS = {
    "name",
    "path",
    "category",
    "activation",
    "priority",
    "risk_level",
    "related_workflows",
    "allowed_side_effects",
    "requires_confirmation",
}

VISUAL_JSON_EXAMPLE_FILES = (
    "skills/timestamp-to-visual-prompt/SKILL.md",
    "skills/squirrel-video-director/SKILL.md",
)


@dataclass(frozen=True)
class Issue:
    path: str
    message: str


class AwfValidator:
    def __init__(self, root: Path, strict: bool = False) -> None:
        self.root = root
        self.strict = strict
        self.errors: list[Issue] = []
        self.warnings: list[Issue] = []
        self.counts: dict[str, int] = {
            "workflows": 0,
            "skills": 0,
            "paths": 0,
            "frontmatters": 0,
            "json_files": 0,
            "schema_templates": 0,
            "json_examples": 0,
        }

    def error(self, path: str | Path, message: str) -> None:
        self.errors.append(Issue(str(path), message))

    def warn(self, path: str | Path, message: str) -> None:
        self.warnings.append(Issue(str(path), message))

    def rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    def load_yaml(self, path: Path) -> Any:
        try:
            return yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.error(self.rel(path), f"YAML parse failed: {exc}")
            return None

    def extract_frontmatter(self, path: Path) -> dict[str, Any] | None:
        rel_path = self.rel(path)
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:
            self.error(rel_path, f"Cannot read file: {exc}")
            return None

        if not text.startswith("---"):
            self.error(rel_path, "Missing YAML frontmatter delimiter at file start.")
            return None

        end = text.find("\n---", 3)
        if end == -1:
            self.error(rel_path, "Missing YAML frontmatter closing delimiter.")
            return None

        try:
            data = yaml.safe_load(text[3:end].strip()) or {}
        except Exception as exc:
            self.error(rel_path, f"Frontmatter YAML parse failed: {exc}")
            return None

        if not isinstance(data, dict):
            self.error(rel_path, "Frontmatter must parse to a mapping/object.")
            return None

        self.counts["frontmatters"] += 1
        return data

    def check_path_exists(self, value: str, owner: str) -> Path | None:
        path = self.root / value
        self.counts["paths"] += 1
        if not path.exists():
            self.error(owner, f"Referenced path does not exist: {value}")
            return None
        return path

    def check_missing_keys(self, item: dict[str, Any], required: set[str], owner: str) -> None:
        missing = sorted(required - set(item))
        if missing:
            self.error(owner, f"Missing required key(s): {', '.join(missing)}")

    def check_list(self, item: dict[str, Any], key: str, owner: str, allow_empty: bool = True) -> None:
        value = item.get(key)
        if not isinstance(value, list):
            self.error(owner, f"`{key}` must be a list.")
        elif not allow_empty and not value:
            self.error(owner, f"`{key}` must not be empty.")

    def check_enum(self, item: dict[str, Any], key: str, allowed: set[str], owner: str) -> None:
        value = item.get(key)
        if value not in allowed:
            self.error(owner, f"`{key}` has unsupported value `{value}`.")

    def check_duplicates(self, values: list[str], owner: str) -> None:
        seen: set[str] = set()
        for value in values:
            if value in seen:
                self.error(owner, f"Duplicate value: {value}")
            seen.add(value)

    def validate_manifest(self) -> dict[str, Any] | None:
        manifest_path = self.root / "awf_manifest.yaml"
        manifest = self.load_yaml(manifest_path)
        if not isinstance(manifest, dict):
            self.error("awf_manifest.yaml", "Manifest must parse to a mapping/object.")
            return None

        for key in ("awf_version", "gates", "workflows", "skills"):
            if key not in manifest:
                self.error("awf_manifest.yaml", f"Missing top-level key `{key}`.")

        if "risk_levels" in manifest:
            extra = set(manifest.get("risk_levels", {})) - RISK_LEVELS
            if extra:
                self.warn("awf_manifest.yaml", f"Unknown risk level definitions: {sorted(extra)}")

        workflows = manifest.get("workflows") or []
        skills = manifest.get("skills") or []
        gates = manifest.get("gates") or {}

        if not isinstance(workflows, list):
            self.error("awf_manifest.yaml", "`workflows` must be a list.")
            workflows = []
        if not isinstance(skills, list):
            self.error("awf_manifest.yaml", "`skills` must be a list.")
            skills = []
        if not isinstance(gates, dict):
            self.error("awf_manifest.yaml", "`gates` must be a mapping.")
            gates = {}

        self.counts["workflows"] = len(workflows)
        self.counts["skills"] = len(skills)

        skill_names = {s.get("name") for s in skills if isinstance(s, dict)}
        workflow_commands = {w.get("command") for w in workflows if isinstance(w, dict) and w.get("command")}
        gate_names = set(gates)

        self.check_duplicates([str(s.get("name")) for s in skills if isinstance(s, dict)], "skills")
        self.check_duplicates([str(w.get("name")) for w in workflows if isinstance(w, dict)], "workflows")
        self.check_duplicates([str(w.get("command")) for w in workflows if isinstance(w, dict) and w.get("command")], "workflows")

        for gate_name, gate in gates.items():
            if not isinstance(gate, dict):
                self.error(f"gates.{gate_name}", "Gate entry must be a mapping.")
                continue
            path_value = gate.get("path")
            if isinstance(path_value, str):
                self.check_path_exists(path_value, f"gates.{gate_name}")
            else:
                self.error(f"gates.{gate_name}", "Gate must define string `path`.")

        self.validate_workflows(workflows, skill_names, workflow_commands, gate_names)
        self.validate_skills(skills, workflow_commands, gate_names)
        self.validate_manifest_coverage(workflows, skills)
        return manifest

    def validate_workflows(
        self,
        workflows: list[Any],
        skill_names: set[Any],
        workflow_commands: set[str],
        gate_names: set[str],
    ) -> None:
        for workflow in workflows:
            if not isinstance(workflow, dict):
                self.error("workflows", "Workflow entry must be a mapping.")
                continue

            owner = f"workflow:{workflow.get('name', '<unnamed>')}"
            self.check_missing_keys(workflow, WORKFLOW_REQUIRED_KEYS, owner)
            self.check_enum(workflow, "risk_level", RISK_LEVELS, owner)
            self.check_enum(workflow, "priority", PRIORITIES, owner)
            self.check_list(workflow, "triggers", owner, allow_empty=False)
            self.check_list(workflow, "next_workflows", owner)
            self.check_list(workflow, "required_gates", owner)
            self.check_list(workflow, "required_skills", owner)
            self.check_list(workflow, "conditional_skills", owner)

            for gate in workflow.get("required_gates", []) or []:
                if gate not in gate_names:
                    self.error(owner, f"Unknown required gate: {gate}")

            for skill in (workflow.get("required_skills", []) or []) + (workflow.get("conditional_skills", []) or []):
                if skill not in skill_names:
                    self.error(owner, f"Unknown skill reference: {skill}")

            for command in workflow.get("next_workflows", []) or []:
                if command not in workflow_commands:
                    self.error(owner, f"Unknown next workflow command: {command}")

            path_value = workflow.get("path")
            if not isinstance(path_value, str):
                self.error(owner, "`path` must be a string.")
                continue

            path = self.check_path_exists(path_value, owner)
            if not path:
                continue

            fm = self.extract_frontmatter(path)
            if not fm:
                continue

            for key in ("name", "command", "category", "risk_level"):
                if key in fm and workflow.get(key) != fm.get(key):
                    self.error(self.rel(path), f"Frontmatter `{key}` does not match manifest.")

            if fm.get("type") != "workflow":
                self.error(self.rel(path), "Frontmatter `type` must be `workflow`.")

            self.validate_frontmatter_refs(fm, self.rel(path), workflow_commands, skill_names, gate_names)

    def validate_skills(
        self,
        skills: list[Any],
        workflow_commands: set[str],
        gate_names: set[str],
    ) -> None:
        for skill in skills:
            if not isinstance(skill, dict):
                self.error("skills", "Skill entry must be a mapping.")
                continue

            owner = f"skill:{skill.get('name', '<unnamed>')}"
            self.check_missing_keys(skill, SKILL_REQUIRED_KEYS, owner)
            self.check_enum(skill, "risk_level", RISK_LEVELS, owner)
            self.check_enum(skill, "priority", PRIORITIES, owner)
            self.check_enum(skill, "activation", ACTIVATIONS, owner)
            self.check_list(skill, "related_workflows", owner)
            self.check_list(skill, "allowed_side_effects", owner)

            if not isinstance(skill.get("requires_confirmation"), bool):
                self.error(owner, "`requires_confirmation` must be boolean.")

            for command in skill.get("related_workflows", []) or []:
                if command != "all" and command not in workflow_commands:
                    self.error(owner, f"Unknown related workflow command: {command}")

            if skill.get("risk_level") in {"high", "critical"} and skill.get("requires_confirmation") is not True:
                self.warn(owner, "High/critical risk skill should require confirmation.")

            path_value = skill.get("path")
            if not isinstance(path_value, str):
                self.error(owner, "`path` must be a string.")
                continue

            path = self.check_path_exists(path_value, owner)
            if not path:
                continue

            fm = self.extract_frontmatter(path)
            if not fm:
                continue

            for key in ("name", "category", "activation", "priority", "risk_level", "requires_confirmation"):
                if key in fm and skill.get(key) != fm.get(key):
                    self.error(self.rel(path), f"Frontmatter `{key}` does not match manifest.")

            if fm.get("type") != "skill":
                self.error(self.rel(path), "Frontmatter `type` must be `skill`.")

            self.validate_frontmatter_refs(fm, self.rel(path), workflow_commands, set(), gate_names)

    def validate_frontmatter_refs(
        self,
        fm: dict[str, Any],
        owner: str,
        workflow_commands: set[str],
        skill_names: set[Any],
        gate_names: set[str],
    ) -> None:
        for gate in fm.get("required_gates", []) or []:
            if gate not in gate_names:
                self.error(owner, f"Unknown required gate in frontmatter: {gate}")

        for command in fm.get("related_workflows", []) or []:
            if command != "all" and command not in workflow_commands:
                self.error(owner, f"Unknown related workflow in frontmatter: {command}")

        handoff = fm.get("handoff")
        if isinstance(handoff, dict):
            for command in handoff.get("next_workflows", []) or []:
                if command not in workflow_commands:
                    self.error(owner, f"Unknown handoff next workflow: {command}")

        hooks = fm.get("skill_hooks")
        if isinstance(hooks, dict) and skill_names:
            for key in ("required", "conditional"):
                for skill in hooks.get(key, []) or []:
                    if skill not in skill_names:
                        self.error(owner, f"Unknown `{key}` skill hook: {skill}")

    def validate_manifest_coverage(self, workflows: list[Any], skills: list[Any]) -> None:
        manifest_workflow_paths = {str(w.get("path")).replace("\\", "/") for w in workflows if isinstance(w, dict)}
        manifest_skill_paths = {str(s.get("path")).replace("\\", "/") for s in skills if isinstance(s, dict)}

        for path in (self.root / "global_workflows").glob("*.md"):
            rel = self.rel(path)
            if path.name in {"CONTEXT_SYSTEM.md", "GLOBAL_SAFETY_TRUTHFULNESS_GATE.md"}:
                continue
            if rel not in manifest_workflow_paths:
                self.warn(rel, "Workflow markdown file is not listed in awf_manifest.yaml.")

        for path in (self.root / "skills").rglob("SKILL.md"):
            rel = self.rel(path)
            if rel not in manifest_skill_paths:
                self.warn(rel, "Skill file is not listed in awf_manifest.yaml.")

    def tracked_json_files(self) -> list[Path]:
        try:
            proc = subprocess.run(
                ["git", "ls-files", "*.json"],
                cwd=self.root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return [self.root / line for line in proc.stdout.splitlines() if line.strip()]
        except Exception:
            return sorted(p for p in self.root.rglob("*.json") if ".git" not in p.parts)

    def validate_json_files(self) -> None:
        for path in self.tracked_json_files():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                self.error(self.rel(path), f"JSON parse failed: {exc}")
            else:
                self.counts["json_files"] += 1

    def validate_schema_templates(self) -> None:
        templates_dir = self.root / "templates"
        schemas_dir = self.root / "schemas"
        if not templates_dir.exists() or not schemas_dir.exists():
            return

        for template in sorted(templates_dir.glob("*.example.json")):
            base = template.name.replace(".example.json", "")
            schema = schemas_dir / f"{base}.schema.json"
            if not schema.exists():
                self.warn(self.rel(template), f"No matching schema found at schemas/{base}.schema.json.")
                continue

            try:
                instance = json.loads(template.read_text(encoding="utf-8"))
                schema_data = json.loads(schema.read_text(encoding="utf-8"))
            except Exception as exc:
                self.error(self.rel(template), f"Cannot load template/schema JSON: {exc}")
                continue

            if jsonschema is None:
                self.warn(self.rel(template), "jsonschema not installed; skipped schema validation.")
                continue

            try:
                jsonschema.validate(instance=instance, schema=schema_data)
            except Exception as exc:
                self.error(self.rel(template), f"Template does not validate against schema: {exc}")
            else:
                self.counts["schema_templates"] += 1

    def validate_visual_json_examples(self) -> None:
        pattern = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)
        for rel_path in VISUAL_JSON_EXAMPLE_FILES:
            path = self.root / rel_path
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            for index, block in enumerate(pattern.findall(text), start=1):
                try:
                    json.loads(block)
                except Exception as exc:
                    self.error(rel_path, f"JSON fenced example #{index} is invalid: {exc}")
                else:
                    self.counts["json_examples"] += 1

    def run(self) -> int:
        self.validate_manifest()
        self.validate_json_files()
        self.validate_schema_templates()
        self.validate_visual_json_examples()

        if self.strict and self.warnings:
            for issue in self.warnings:
                self.errors.append(Issue(issue.path, f"Strict warning: {issue.message}"))
            self.warnings = []

        return 1 if self.errors else 0

    def print_report(self) -> None:
        print("AWF validation report")
        print(f"Root: {self.root}")
        print("")
        print("Checks:")
        for key, value in self.counts.items():
            print(f"  {key}: {value}")
        print("")

        if self.errors:
            print("Errors:")
            for issue in self.errors:
                print(f"  - {issue.path}: {issue.message}")
            print("")

        if self.warnings:
            print("Warnings:")
            for issue in self.warnings:
                print(f"  - {issue.path}: {issue.message}")
            print("")

        if not self.errors:
            status = "PASS"
            if self.warnings:
                status += " with warnings"
            print(f"Result: {status}")
        else:
            print("Result: FAIL")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate AWF extended metadata and artifacts.")
    parser.add_argument(
        "--root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Repository root. Defaults to the parent of the tools directory.",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = AwfValidator(args.root.resolve(), strict=args.strict)
    code = validator.run()
    validator.print_report()
    return code


if __name__ == "__main__":
    sys.exit(main())
