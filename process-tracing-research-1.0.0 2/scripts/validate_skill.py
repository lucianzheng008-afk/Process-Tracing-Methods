#!/usr/bin/env python3
"""Validate the structure and internal consistency of this Skill package."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = {
    "SKILL.md", "README.md", "USAGE-AND-ACCEPTANCE.md", "LICENSE",
    "THIRD-PARTY-NOTICES.md", "VERSION", "CHANGELOG.md", "CITATION.cff",
    ".gitignore", ".gitattributes", "CONTRIBUTING.md", "MANIFEST.sha256",
    "references/method-foundations.md", "references/research-design.md",
    "references/mechanism-and-observables.md",
    "references/evidence-and-bayesian-updating.md",
    "references/sources-and-triangulation.md",
    "references/alternatives-counterfactuals-sequences.md",
    "references/literature-and-case-search.md",
    "references/writing-and-visuals.md", "references/quality-gates.md",
    "references/bibliography.md", "templates/project-metadata.json",
    "templates/research-ledger.md", "templates/manuscript-outline.md", "templates/SCHEMA.md",
    "examples/full-worked-example-tannenwald.md",
    "examples/empirical-case-cards.md", "examples/failure-and-repair.md",
    "scripts/validate_skill.py", "scripts/audit_project.py",
}

SCHEMAS = {
    "mechanism-evidence-matrix.csv": {
        "mechanism_id", "step_id", "sequence", "entity", "activity", "input",
        "change_object", "state_before", "state_after", "output",
        "context_conditions", "expected_timing", "proposition_id",
        "predicted_fingerprint", "theoretical_certainty", "theoretical_uniqueness",
        "alternative_generators", "disconfirming_observation", "source_target", "status",
    },
    "evidence-register.csv": {
        "evidence_id", "proposition_id", "case_id", "observation", "evidence_type",
        "found_status", "source_ids", "source_family_ids", "access_probability",
        "empirical_certainty", "empirical_uniqueness", "reliability", "independence",
        "direction", "diagnostic_weight", "supports_explanations",
        "challenges_explanations", "locator",
    },
    "source-register.csv": {
        "source_id", "source_family_id", "citation_key", "source_type", "title",
        "creator", "date", "locator", "url_or_path", "access_status", "proximity",
        "competence", "motive_risk", "authenticity", "independence_notes",
        "permitted_claims",
    },
    "source-dependence-matrix.csv": {
        "proposition_id", "source_id_a", "source_id_b", "dependence_level",
        "shared_channel", "justification",
    },
    "timeline.csv": {
        "event_id", "case_id", "date_start", "date_end", "event", "actor",
        "step_ids", "evidence_ids", "source_ids", "analytic_role",
    },
    "competing-explanations.csv": {
        "explanation_id", "claim", "mechanism_summary", "scope_conditions",
        "expected_fingerprints", "unfriendly_evidence", "status",
    },
    "bayesian-update.csv": {
        "update_id", "explanation_id", "evidence_id", "prior_level",
        "likelihood_under_explanation", "likelihood_under_best_alternative",
        "source_adjustment", "dependence_adjustment", "update_direction",
        "posterior_level", "justification",
    },
    "case-comparison.csv": {
        "case_id", "case_name", "case_type", "cause_status", "outcome_status",
        "context_conditions", "mechanism_status", "access_profile", "selection_role",
        "comparability_limits",
    },
    "claim-register.csv": {
        "claim_id", "claim_text", "claim_type", "case_id", "step_ids",
        "evidence_ids", "source_ids", "confidence", "scope", "status",
    },
    "visual-register.csv": {
        "visual_id", "visual_type", "title", "source_tables", "included_ids",
        "caption_claim", "output_path", "status",
    },
    "revision-register.csv": {
        "revision_id", "timestamp", "object_ids", "change_type", "prior_state",
        "new_state", "reason", "evidence_ids", "supersedes", "status",
    },
}

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b", re.IGNORECASE)


def issue(code: str, severity: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": severity, "file": path, "message": message}


def validate(root: Path) -> dict[str, object]:
    issues: list[dict[str, str]] = []
    for relative in sorted(REQUIRED_FILES):
        target = root / relative
        if not target.is_file():
            issues.append(issue("MISSING_FILE", "error", relative, "required file is missing"))
        elif target.stat().st_size == 0:
            issues.append(issue("EMPTY_FILE", "error", relative, "required file is empty"))

    skill = root / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        parts = text.split("---\n", 2)
        if not text.startswith("---\n") or len(parts) < 3:
            issues.append(issue("FRONTMATTER", "error", "SKILL.md", "missing fenced frontmatter"))
        else:
            lines = [line for line in parts[1].splitlines() if line.strip()]
            pairs = {}
            malformed = False
            for line in lines:
                if ":" not in line:
                    malformed = True
                    continue
                key, value = line.split(":", 1)
                pairs[key.strip()] = value.strip()
            if malformed or set(pairs) != {"name", "description"}:
                issues.append(issue("FRONTMATTER", "error", "SKILL.md", "frontmatter must contain only name and description"))
            if pairs.get("name") != "process-tracing-research":
                issues.append(issue("SKILL_NAME", "error", "SKILL.md", "name must be process-tracing-research"))
            if not pairs.get("description", "").startswith("Use when"):
                issues.append(issue("TRIGGER_DESCRIPTION", "error", "SKILL.md", "description must state when to use the Skill"))
        if len(text.splitlines()) > 500:
            issues.append(issue("SKILL_LENGTH", "warning", "SKILL.md", "router exceeds 500 lines; move detail to references"))

    for filename, required in SCHEMAS.items():
        path = root / "templates" / filename
        if not path.is_file():
            issues.append(issue("MISSING_TEMPLATE", "error", f"templates/{filename}", "CSV template is missing"))
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
        if not rows:
            issues.append(issue("EMPTY_TEMPLATE", "error", f"templates/{filename}", "CSV has no header"))
            continue
        header = rows[0]
        if len(header) != len(set(header)):
            issues.append(issue("DUPLICATE_HEADER", "error", f"templates/{filename}", "CSV header contains duplicates"))
        missing = sorted(required - set(header))
        if missing:
            issues.append(issue("SCHEMA", "error", f"templates/{filename}", f"missing columns: {', '.join(missing)}"))

    metadata = root / "templates" / "project-metadata.json"
    if metadata.is_file():
        try:
            payload = json.loads(metadata.read_text(encoding="utf-8"))
            for key in ("project_id", "title", "design_variant", "inference_mode", "main_explanation_id"):
                if key not in payload:
                    issues.append(issue("METADATA_SCHEMA", "error", "templates/project-metadata.json", f"missing key: {key}"))
        except json.JSONDecodeError as exc:
            issues.append(issue("INVALID_JSON", "error", "templates/project-metadata.json", str(exc)))

    for path in root.rglob("*.md"):
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        if not relative.startswith(("tests/", "test-reports/")) and PLACEHOLDER_RE.search(text):
            issues.append(issue("PLACEHOLDER", "error", relative, "unresolved placeholder token found"))
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            target = target.strip("<>")
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                issues.append(issue("OUTSIDE_LINK", "error", relative, f"relative link escapes package: {raw_target}"))
                continue
            if not resolved.exists():
                issues.append(issue("BROKEN_LINK", "error", relative, f"missing link target: {raw_target}"))

    error_count = sum(item["severity"] == "error" for item in issues)
    warning_count = sum(item["severity"] == "warning" for item in issues)
    return {
        "ok": error_count == 0,
        "root": str(root),
        "errors": error_count,
        "warnings": warning_count,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    report = validate(Path(args.root).expanduser().resolve())
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Skill package: {'PASS' if report['ok'] else 'FAIL'}")
        print(f"Errors: {report['errors']}  Warnings: {report['warnings']}")
        for item in report["issues"]:
            print(f"[{item['severity'].upper()}] {item['code']} {item['file']}: {item['message']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
