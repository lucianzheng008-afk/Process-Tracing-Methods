# Project schema

For an authorized build/research task, copy all templates into one project directory. For a read-only review or answer, do not create files; reproduce only the relevant fields inline, and treat `SKILL.md`'s no-write route as controlling. UTF-8 CSV is required for file-backed projects. Preserve headers. Separate multiple IDs with semicolons, for example `E-1;E-2`; never place the same source family twice in one evidence row.

## Controlled vocabularies

- Confidence/likelihood/access: `very low`, `low`, `medium`, `high`, `very high`, `unknown`, `unassessed`, `not applicable`.
- Evidence type: `pattern`, `sequence`, `trace`, `account`.
- Found status: `found`, `not-found`, `unavailable`, `conflicted`, `stipulated`.
- Prompt-only provenance: use `stipulated`, put `scenario-stipulated, unaudited` in `notes`, and do not treat it as source-verified.
- Independence: `dependent`, `partly independent`, `independent`, `unknown`.
- Direction: `confirm`, `disconfirm`, `none`, `mixed`.
- Update direction: `up`, `down`, `none`, `mixed`.
- Claim type: `observation`, `inference`, `causal`, `boundary`, `unavailable`.
- Claim status: `established`, `supported`, `open`, `unavailable`, `withdrawn`.
- Mechanism status: `planned`, `required`, `necessary`, `supported`, `mixed`, `weakened`, `unsupported`, `unavailable`.
- Explanation status: `active`, `weakened`, `not adjudicated`, `complementary`, `excluded`, `outside scope`.
- Access state: `metadata`, `abstract`, `partial`, `full-text`, `primary-record`, `restricted`, `unavailable`.
- Inference mode: `prospective`, `retrospective-prior-reconstruction`, `evidence-aware-discovery`, `audit`.

Controlled words create comparable rows; their justification belongs in the narrative/notes fields.

## File relationships

```text
project-metadata.main_explanation_id -> competing-explanations.explanation_id
mechanism-evidence-matrix.proposition_id -> evidence-register.proposition_id
evidence-register.source_ids -> source-register.source_id
evidence-register.source_family_ids -> source-register.source_family_id
source-dependence-matrix.proposition_id/source_id_a/source_id_b -> proposition and source registers
bayesian-update.evidence_id -> evidence-register.evidence_id
bayesian-update.explanation_id -> competing-explanations.explanation_id
timeline.step_ids -> mechanism-evidence-matrix.step_id
timeline.evidence_ids -> evidence-register.evidence_id
claim-register.step_ids/evidence_ids/source_ids -> corresponding registers
visual-register.included_ids -> any registered analytic ID
revision-register.object_ids/evidence_ids -> corresponding registers
```

## Key field rules

### mechanism-evidence-matrix.csv

One row is one proposition for one mechanism step. `change_object`, `state_before`, and `state_after` specify exactly what the activity changes and in which direction. Repeat a `step_id` only when the step has multiple distinct propositions; if repeated, use unique `proposition_id`s and keep entity/activity continuity consistent. `alternative_generators` describes other ways the fingerprint could arise. `disconfirming_observation` is not merely “fingerprint absent” unless expected observability is high.

Use lettered mechanism branches after shared steps (`M-1A-S1`, `M-1B-S1`). Never renumber an ID after it has been cited; record supersession in the research ledger. Planned observables receive proposition IDs, not placeholder evidence IDs.

### evidence-register.csv

`observation` records what the material establishes before causal interpretation. `source_ids` and `source_family_ids` must correspond. `empirical_certainty` is especially relevant to not-found evidence; `empirical_uniqueness` to found evidence. `diagnostic_weight` is qualitative and requires explanation in `notes` or the update register.

### source-register.csv

One row is one artifact/testimony. Use the same `source_family_id` when items copy, quote, share an informant, or derive from one underlying record for the proposition. `permitted_claims` sets the maximum factual use of the inspected content.

### source-dependence-matrix.csv

Use one row per source pair and important proposition. `dependence_level` is `dependent`, `partly independent`, `independent`, or `unknown`. A pair in one baseline family may be upgraded for a narrow proposition only when the matrix documents genuinely separate information-generation channels. If dependence differs across propositions, add separate rows.

### bayesian-update.csv

One row evaluates one evidence item against one explanation and its best comparator. Use levels, not numeric scores, unless a separately documented elicitation/sensitivity protocol exists. `source_adjustment` and `dependence_adjustment` must not be hidden inside the theoretical likelihood fields.

### claim-register.csv

Every causal or inferential claim needs evidence IDs. A claim's confidence and status cannot exceed the weakest necessary mechanism step. `scope` must name the case/time/population to which the claim is limited.

### visual-register.csv

`source_tables` lists semicolon-separated project filenames. `included_ids` lists the exact IDs shown. `caption_claim` must not exceed the claim register. `output_path` is relative to the project directory and must exist when status is `rendered` or `final`.

### revision-register.csv

Every material theory, mechanism, evidence-status, or conclusion change receives an immutable `REV-*` row. `object_ids` names affected IDs; `prior_state` and `new_state` preserve the change; `reason` and `evidence_ids` explain it. Do not rewrite history by silently editing or reusing IDs.
