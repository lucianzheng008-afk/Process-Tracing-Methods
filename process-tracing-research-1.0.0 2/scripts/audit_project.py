#!/usr/bin/env python3
"""Audit a process-tracing project for structural and inferential red flags."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import date
from itertools import combinations
from pathlib import Path


REQUIRED = {
    "project-metadata.json",
    "mechanism-evidence-matrix.csv",
    "source-register.csv",
    "evidence-register.csv",
    "timeline.csv",
    "competing-explanations.csv",
    "bayesian-update.csv",
    "claim-register.csv",
}

MECHANISM_FIELDS = (
    "mechanism_id", "step_id", "sequence", "entity", "activity", "input",
    "change_object", "state_before", "state_after", "output", "context_conditions",
    "expected_timing", "proposition_id", "predicted_fingerprint",
    "theoretical_certainty", "theoretical_uniqueness", "alternative_generators",
    "disconfirming_observation", "source_target", "status",
)

LEVELS = {"very low", "low", "medium", "high", "very high", "unknown", "unassessed", "not applicable"}


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in value.replace("|", ";").split(";") if item.strip()]


def add(issues: list[dict[str, object]], code: str, severity: str, file: str, row: int, message: str) -> None:
    issues.append({"code": code, "severity": severity, "file": file, "row": row, "message": message})


def read_csv(root: Path, name: str, issues: list[dict[str, object]]) -> list[dict[str, str]]:
    path = root / name
    if not path.is_file():
        add(issues, "MISSING_PROJECT_FILE", "error", name, 0, "required project file is missing")
        return []
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except (csv.Error, UnicodeError) as exc:
        add(issues, "CSV_PARSE", "error", name, 0, str(exc))
        return []


def id_set(rows: list[dict[str, str]], field: str) -> set[str]:
    return {row.get(field, "").strip() for row in rows if row.get(field, "").strip()}


def check_duplicate_ids(rows: list[dict[str, str]], field: str, file: str, issues: list[dict[str, object]]) -> None:
    values = [row.get(field, "").strip() for row in rows if row.get(field, "").strip()]
    for value, count in Counter(values).items():
        if count > 1:
            add(issues, "DUPLICATE_ID", "error", file, 0, f"{field} {value} occurs {count} times")


def parse_date(value: str):
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def audit(root: Path) -> dict[str, object]:
    issues: list[dict[str, object]] = []
    for name in sorted(REQUIRED):
        if not (root / name).is_file():
            add(issues, "MISSING_PROJECT_FILE", "error", name, 0, "required project file is missing")

    metadata_path = root / "project-metadata.json"
    metadata: dict[str, object] = {}
    if metadata_path.is_file():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            add(issues, "INVALID_JSON", "error", "project-metadata.json", 0, str(exc))
        for key in ("project_id", "title", "design_variant", "inference_mode", "cases", "main_explanation_id"):
            if key not in metadata or metadata.get(key) in (None, "", []):
                add(issues, "METADATA_FIELD", "error", "project-metadata.json", 0, f"missing value: {key}")
        if metadata.get("inference_mode") not in {"prospective", "retrospective-prior-reconstruction", "evidence-aware-discovery", "audit"}:
            add(issues, "INVALID_INFERENCE_MODE", "error", "project-metadata.json", 0, f"unrecognized inference_mode: {metadata.get('inference_mode', '')}")

    mech = read_csv(root, "mechanism-evidence-matrix.csv", issues)
    sources = read_csv(root, "source-register.csv", issues)
    evidence = read_csv(root, "evidence-register.csv", issues)
    timeline = read_csv(root, "timeline.csv", issues)
    explanations = read_csv(root, "competing-explanations.csv", issues)
    updates = read_csv(root, "bayesian-update.csv", issues)
    claims = read_csv(root, "claim-register.csv", issues)
    cases = read_csv(root, "case-comparison.csv", issues) if (root / "case-comparison.csv").is_file() else []
    visuals = read_csv(root, "visual-register.csv", issues) if (root / "visual-register.csv").is_file() else []
    dependencies = read_csv(root, "source-dependence-matrix.csv", issues) if (root / "source-dependence-matrix.csv").is_file() else []
    revisions = read_csv(root, "revision-register.csv", issues) if (root / "revision-register.csv").is_file() else []

    for rows, field, name in (
        (mech, "step_id", "mechanism-evidence-matrix.csv"),
        (sources, "source_id", "source-register.csv"),
        (evidence, "evidence_id", "evidence-register.csv"),
        (timeline, "event_id", "timeline.csv"),
        (explanations, "explanation_id", "competing-explanations.csv"),
        (updates, "update_id", "bayesian-update.csv"),
        (claims, "claim_id", "claim-register.csv"),
        (revisions, "revision_id", "revision-register.csv"),
    ):
        check_duplicate_ids(rows, field, name, issues)

    step_ids = id_set(mech, "step_id")
    proposition_ids = id_set(mech, "proposition_id")
    source_ids = id_set(sources, "source_id")
    evidence_ids = id_set(evidence, "evidence_id")
    explanation_ids = id_set(explanations, "explanation_id")
    source_families = {row.get("source_id", "").strip(): row.get("source_family_id", "").strip() for row in sources}
    registered_cases = id_set(cases, "case_id")
    dependency_map: dict[tuple[str, frozenset[str]], str] = {}

    for row_no, row in enumerate(dependencies, 2):
        proposition = row.get("proposition_id", "").strip()
        source_a = row.get("source_id_a", "").strip()
        source_b = row.get("source_id_b", "").strip()
        level = row.get("dependence_level", "").strip().lower()
        if proposition not in proposition_ids:
            add(issues, "UNKNOWN_PROPOSITION_ID", "error", "source-dependence-matrix.csv", row_no, f"unknown proposition: {proposition}")
        for value in (source_a, source_b):
            if value not in source_ids:
                add(issues, "UNKNOWN_SOURCE_ID", "error", "source-dependence-matrix.csv", row_no, f"unknown source: {value}")
        if source_a == source_b:
            add(issues, "INVALID_DEPENDENCE_PAIR", "error", "source-dependence-matrix.csv", row_no, "source pair must contain two different sources")
        if level not in {"dependent", "partly independent", "independent", "unknown"}:
            add(issues, "INVALID_DEPENDENCE_LEVEL", "error", "source-dependence-matrix.csv", row_no, f"unrecognized dependence level: {level}")
        if not row.get("justification", "").strip():
            add(issues, "MISSING_DEPENDENCE_JUSTIFICATION", "error", "source-dependence-matrix.csv", row_no, "dependence assessment needs justification")
        dependency_map[(proposition, frozenset((source_a, source_b)))] = level

    for row_no, row in enumerate(mech, 2):
        missing = [field for field in MECHANISM_FIELDS if not row.get(field, "").strip()]
        if missing:
            add(issues, "MISSING_MECHANISM_FIELD", "error", "mechanism-evidence-matrix.csv", row_no, f"missing: {', '.join(missing)}")
        try:
            int(row.get("sequence", ""))
        except ValueError:
            add(issues, "INVALID_SEQUENCE", "error", "mechanism-evidence-matrix.csv", row_no, "sequence must be an integer")

    for row_no, row in enumerate(evidence, 2):
        if row.get("proposition_id", "").strip() not in proposition_ids:
            add(issues, "UNKNOWN_PROPOSITION_ID", "error", "evidence-register.csv", row_no, f"unknown proposition: {row.get('proposition_id', '')}")
        row_sources = split_ids(row.get("source_ids", ""))
        for value in row_sources:
            if value not in source_ids:
                add(issues, "UNKNOWN_SOURCE_ID", "error", "evidence-register.csv", row_no, f"unknown source: {value}")
        families = split_ids(row.get("source_family_ids", ""))
        if len(families) != len(set(families)):
            add(issues, "DUPLICATE_SOURCE_FAMILY", "error", "evidence-register.csv", row_no, "same source family is counted more than once")
        if len(row_sources) > 1 and row.get("independence", "").strip().lower() == "independent" and len(set(families)) < len(row_sources):
            proposition = row.get("proposition_id", "").strip()
            shared_family_pairs = [
                (a, b) for a, b in combinations(row_sources, 2)
                if source_families.get(a) and source_families.get(a) == source_families.get(b)
            ]
            justified = shared_family_pairs and all(
                dependency_map.get((proposition, frozenset((a, b)))) == "independent"
                for a, b in shared_family_pairs
            )
            if not justified:
                add(issues, "FAMILY_INDEPENDENCE_CONFLICT", "error", "evidence-register.csv", row_no, "sources sharing a baseline family require proposition-level independence justification")
        expected_families = {source_families[value] for value in row_sources if value in source_families and source_families[value]}
        if expected_families and not expected_families.issubset(set(families)):
            add(issues, "SOURCE_FAMILY_MISMATCH", "error", "evidence-register.csv", row_no, "source_family_ids do not cover the registered families of source_ids")
        if row.get("found_status", "").strip().lower() in {"not-found", "absent"} and row.get("access_probability", "").strip().lower() in {"", "low", "very low", "unknown"} and row.get("direction", "").strip().lower() in {"disconfirm", "down", "negative"}:
            add(issues, "ABSENCE_WITH_LOW_ACCESS", "error", "evidence-register.csv", row_no, "absence cannot disconfirm when access/detection is low or unknown")
        if row.get("found_status", "").strip().lower() not in {"found", "not-found", "unavailable", "conflicted", "stipulated"}:
            add(issues, "INVALID_FOUND_STATUS", "error", "evidence-register.csv", row_no, f"unrecognized found_status: {row.get('found_status', '')}")
        if row.get("found_status", "").strip().lower() == "stipulated" and "scenario-stipulated" not in row.get("notes", "").lower():
            add(issues, "STIPULATED_PROVENANCE", "error", "evidence-register.csv", row_no, "stipulated evidence must be marked scenario-stipulated in notes")

    active_explanations = [row for row in explanations if row.get("status", "").strip().lower() not in {"excluded", "inactive"}]
    if len(active_explanations) < 2:
        add(issues, "NO_COMPETING_EXPLANATION", "error", "competing-explanations.csv", 0, "at least one genuine active alternative is required")
    main_id = str(metadata.get("main_explanation_id", ""))
    if main_id and main_id not in explanation_ids:
        add(issues, "UNKNOWN_MAIN_EXPLANATION", "error", "project-metadata.json", 0, f"unknown main explanation: {main_id}")
    metadata_cases = {str(value) for value in metadata.get("cases", [])} if isinstance(metadata.get("cases", []), list) else set()
    if registered_cases and not metadata_cases.issubset(registered_cases):
        add(issues, "UNKNOWN_CASE_ID", "error", "project-metadata.json", 0, "one or more metadata cases are missing from case-comparison.csv")

    for row_no, row in enumerate(updates, 2):
        if row.get("explanation_id", "").strip() not in explanation_ids:
            add(issues, "UNKNOWN_EXPLANATION_ID", "error", "bayesian-update.csv", row_no, f"unknown explanation: {row.get('explanation_id', '')}")
        if row.get("evidence_id", "").strip() not in evidence_ids:
            add(issues, "UNKNOWN_EVIDENCE_ID", "error", "bayesian-update.csv", row_no, f"unknown evidence: {row.get('evidence_id', '')}")
        for field in ("prior_level", "likelihood_under_explanation", "likelihood_under_best_alternative", "posterior_level"):
            value = row.get(field, "").strip().lower()
            if value and value not in LEVELS:
                add(issues, "UNANCHORED_LEVEL", "warning", "bayesian-update.csv", row_no, f"{field} uses unrecognized level: {value}")
        if not row.get("justification", "").strip():
            add(issues, "MISSING_UPDATE_JUSTIFICATION", "error", "bayesian-update.csv", row_no, "likelihood/update requires justification")

    for row_no, row in enumerate(timeline, 2):
        start, end = parse_date(row.get("date_start", "")), parse_date(row.get("date_end", ""))
        if row.get("date_start", "") and start is None:
            add(issues, "INVALID_DATE", "warning", "timeline.csv", row_no, "date_start is not ISO-formatted")
        if start and end and start > end:
            add(issues, "TIMELINE_DATE_ORDER", "error", "timeline.csv", row_no, "date_start occurs after date_end")
        for value in split_ids(row.get("step_ids", "")):
            if value not in step_ids:
                add(issues, "UNKNOWN_STEP_ID", "error", "timeline.csv", row_no, f"unknown step: {value}")
        for value in split_ids(row.get("evidence_ids", "")):
            if value not in evidence_ids:
                add(issues, "UNKNOWN_EVIDENCE_ID", "error", "timeline.csv", row_no, f"unknown evidence: {value}")
        for value in split_ids(row.get("source_ids", "")):
            if value not in source_ids:
                add(issues, "UNKNOWN_SOURCE_ID", "error", "timeline.csv", row_no, f"unknown source: {value}")

    for row_no, row in enumerate(claims, 2):
        claim_evidence = split_ids(row.get("evidence_ids", ""))
        claim_sources = split_ids(row.get("source_ids", ""))
        if row.get("claim_type", "").strip().lower() in {"inference", "causal", "conclusion"} and not claim_evidence:
            add(issues, "UNSUPPORTED_CLAIM", "error", "claim-register.csv", row_no, "causal/inferential claim has no evidence IDs")
        for value in claim_evidence:
            if value not in evidence_ids:
                add(issues, "UNKNOWN_EVIDENCE_ID", "error", "claim-register.csv", row_no, f"unknown evidence: {value}")
        for value in claim_sources:
            if value not in source_ids:
                add(issues, "UNKNOWN_SOURCE_ID", "error", "claim-register.csv", row_no, f"unknown source: {value}")
        for value in split_ids(row.get("step_ids", "")):
            if value not in step_ids:
                add(issues, "UNKNOWN_STEP_ID", "error", "claim-register.csv", row_no, f"unknown step: {value}")

    all_ids = step_ids | proposition_ids | source_ids | evidence_ids | explanation_ids | id_set(timeline, "event_id") | id_set(claims, "claim_id")
    for row_no, row in enumerate(visuals, 2):
        for value in split_ids(row.get("included_ids", "")):
            if value not in all_ids:
                add(issues, "UNKNOWN_VISUAL_ID", "error", "visual-register.csv", row_no, f"unknown included ID: {value}")
        for value in split_ids(row.get("source_tables", "")):
            if not (root / value).is_file():
                add(issues, "UNKNOWN_VISUAL_SOURCE", "error", "visual-register.csv", row_no, f"source table does not exist: {value}")
        output = row.get("output_path", "").strip()
        status = row.get("status", "").strip().lower()
        if status in {"rendered", "final", "registered"} and (not output or not (root / output).is_file()):
            add(issues, "MISSING_VISUAL_OUTPUT", "error", "visual-register.csv", row_no, f"visual output does not exist: {output}")

    observed_props = {row.get("proposition_id", "").strip() for row in evidence}
    for row_no, row in enumerate(mech, 2):
        if row.get("status", "").strip().lower() in {"required", "necessary", "supported"} and row.get("proposition_id", "").strip() not in observed_props:
            add(issues, "NECESSARY_STEP_NO_EVIDENCE", "error", "mechanism-evidence-matrix.csv", row_no, "required/necessary step has no registered evidence")

    error_count = sum(item["severity"] == "error" for item in issues)
    warning_count = sum(item["severity"] == "warning" for item in issues)
    return {
        "ok": error_count == 0,
        "project": str(root),
        "errors": error_count,
        "warnings": warning_count,
        "issues": issues,
        "conclusion_ceiling": "structurally auditable; substantive human gates still required" if error_count == 0 else "design or preliminary inference only until blocking errors are resolved",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    report = audit(Path(args.project).expanduser().resolve())
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Project audit: {'PASS' if report['ok'] else 'FAIL'}")
        print(f"Errors: {report['errors']}  Warnings: {report['warnings']}")
        print(f"Conclusion ceiling: {report['conclusion_ceiling']}")
        for item in report["issues"]:
            row = f":{item['row']}" if item["row"] else ""
            print(f"[{item['severity'].upper()}] {item['code']} {item['file']}{row}: {item['message']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
