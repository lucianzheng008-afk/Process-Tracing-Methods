from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TEMPLATES = ROOT / "templates"


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "USAGE-AND-ACCEPTANCE.md",
    "LICENSE",
    "THIRD-PARTY-NOTICES.md",
    "VERSION",
    "CHANGELOG.md",
    "CITATION.cff",
    ".gitignore",
    ".gitattributes",
    "CONTRIBUTING.md",
    "MANIFEST.sha256",
    "references/method-foundations.md",
    "references/research-design.md",
    "references/mechanism-and-observables.md",
    "references/evidence-and-bayesian-updating.md",
    "references/sources-and-triangulation.md",
    "references/alternatives-counterfactuals-sequences.md",
    "references/literature-and-case-search.md",
    "references/writing-and-visuals.md",
    "references/quality-gates.md",
    "references/bibliography.md",
    "templates/SCHEMA.md",
    "examples/full-worked-example-tannenwald.md",
    "examples/empirical-case-cards.md",
    "examples/failure-and-repair.md",
    "scripts/validate_skill.py",
    "scripts/audit_project.py",
]


SCHEMAS = {
    "mechanism-evidence-matrix.csv": {
        "mechanism_id", "step_id", "sequence", "entity", "activity",
        "input", "change_object", "state_before", "state_after", "output",
        "context_conditions", "expected_timing",
        "proposition_id", "predicted_fingerprint", "theoretical_certainty",
        "theoretical_uniqueness", "alternative_generators",
        "disconfirming_observation", "source_target", "status",
    },
    "evidence-register.csv": {
        "evidence_id", "proposition_id", "case_id", "observation",
        "evidence_type", "found_status", "source_ids", "source_family_ids",
        "access_probability", "empirical_certainty", "empirical_uniqueness",
        "reliability", "independence", "direction", "diagnostic_weight",
        "supports_explanations", "challenges_explanations", "locator",
    },
    "source-register.csv": {
        "source_id", "source_family_id", "citation_key", "source_type",
        "title", "creator", "date", "locator", "url_or_path",
        "access_status", "proximity", "competence", "motive_risk",
        "authenticity", "independence_notes", "permitted_claims",
    },
    "source-dependence-matrix.csv": {
        "proposition_id", "source_id_a", "source_id_b", "dependence_level",
        "shared_channel", "justification",
    },
    "timeline.csv": {
        "event_id", "case_id", "date_start", "date_end", "event",
        "actor", "step_ids", "evidence_ids", "source_ids", "analytic_role",
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
        "context_conditions", "mechanism_status", "access_profile",
        "selection_role", "comparability_limits",
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


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackageTests(unittest.TestCase):
    def test_required_files_exist(self):
        missing = [item for item in REQUIRED_FILES if not (ROOT / item).is_file()]
        self.assertEqual([], missing, f"missing: {missing}")

    def test_skill_frontmatter_is_minimal_and_valid(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---\n", 2)[1]
        lines = [line for line in frontmatter.splitlines() if line.strip()]
        keys = {line.split(":", 1)[0].strip() for line in lines}
        self.assertEqual({"name", "description"}, keys)
        self.assertIn("name: process-tracing-research", frontmatter)

    def test_template_schemas(self):
        for filename, required in SCHEMAS.items():
            with self.subTest(filename=filename):
                with (TEMPLATES / filename).open(encoding="utf-8", newline="") as handle:
                    header = set(next(csv.reader(handle)))
                self.assertTrue(required.issubset(header), required - header)

    def test_package_validator_passes(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_skill.py"), str(ROOT), "--json"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])


class ProjectAuditTests(unittest.TestCase):
    def test_invalid_fixture_fails_with_actionable_codes(self):
        fixture = ROOT / "tests" / "fixtures" / "invalid-project"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "audit_project.py"), str(fixture), "--json"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("MISSING_MECHANISM_FIELD", codes)
        self.assertIn("UNKNOWN_SOURCE_ID", codes)
        self.assertIn("DUPLICATE_SOURCE_FAMILY", codes)
        self.assertIn("UNSUPPORTED_CLAIM", codes)
        self.assertIn("NO_COMPETING_EXPLANATION", codes)

    def test_valid_mini_case_passes(self):
        fixture = ROOT / "examples" / "mini-case"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "audit_project.py"), str(fixture), "--json"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
