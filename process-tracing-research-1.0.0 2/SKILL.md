---
name: process-tracing-research
description: Use when a political-science or international-relations task asks how a cause produced an outcome within one or more cases, requires causal-mechanism reconstruction, process-tracing tests, competing explanations, source criticism, within-case Bayesian updating, or a process-tracing manuscript or audit.
---

# Process-Tracing Research

Build an auditable causal explanation, not a chronology decorated with mechanism vocabulary. The unit of inference is a proposition about a mechanism fingerprint, evaluated against actual observations and plausible evidence-generating alternatives.

## First response and task contract

State that this Skill is being used because the task requires within-case causal inference. Do not delay work for information that can be discovered or represented as an explicit assumption.

For a build/research request, create or update a project directory with the files in `templates/`. For a read-only review, diagnosis, or answer that does not authorize file writes, keep the same ledger structure inline and do not create files. Assign stable IDs immediately in either form:

- cases `CASE-*`; explanations `H-*`; mechanisms `M-*`; steps `M-*-S*`;
- propositions `P-*`; evidence `E-*`; sources `SRC-*`; source families `FAM-*`;
- events `EV-*`; claims `CL-*`; updates `U-*`; visuals `FIG-*` or `TAB-*`.

For branching mechanisms use `M-1A-S1`, `M-1B-S1`, and so on after the shared upstream steps. IDs are immutable: retire rather than renumber them, and record revisions as `REV-*` entries in `revision-register.csv`. Assign `P-*` to planned fingerprints. Assign `E-*` only to an actual evidentiary state: `found`, `not-found`, `conflicted`, `unavailable`, or prompt-only `stipulated`; never reserve empty E IDs for future searches.

Record the requested deliverable, language, length, citation style, deadline, supplied materials, allowed search scope, and uncertainty policy in `project-metadata.json` and `research-ledger.md`, or in an inline task contract for read-only work.

## Route before researching

Choose one primary design. If uncertain, read [research design](references/research-design.md).

| User's inferential aim | Primary design | Core question |
|---|---|---|
| Test a specified mechanism | Theory-testing | Did the hypothesized mechanism operate here? |
| Discover a transferable mechanism between known C and O | Theory-building | What process plausibly links C to O? |
| Explain why a known mechanism failed in a deviant case | Theory-revision | Where did the mechanism break, and what condition was missing? |
| Explain a singular historical outcome comprehensively | Explaining-outcome | What minimally sufficient causal package best accounts for this outcome? |

Do not use this Skill for generic literature reviews, simple chronology, correlation-only questions, or prose polishing that makes no within-case causal claim.

## Progressive reading routes

Read each selected reference completely before performing that stage.

- Every project: [method foundations](references/method-foundations.md), [quality gates](references/quality-gates.md).
- Question, variant, population, case choice: [research design](references/research-design.md).
- Mechanism or predicted traces: [mechanisms and observables](references/mechanism-and-observables.md).
- Evidence evaluation or updating: [evidence and Bayesian updating](references/evidence-and-bayesian-updating.md) and [sources and triangulation](references/sources-and-triangulation.md).
- Rivals, negative evidence, counterfactuals, or timing: [alternatives, counterfactuals, and sequences](references/alternatives-counterfactuals-sequences.md).
- External literature or case search: [literature and case search](references/literature-and-case-search.md).
- Manuscript, tables, diagrams, or presentation: [writing and visuals](references/writing-and-visuals.md).
- Citations and intellectual provenance: [bibliography](references/bibliography.md).
- For form, not substantive proof: read the [worked reconstruction](examples/full-worked-example-tannenwald.md) for aggregation or manuscript tasks; read [case cards](examples/empirical-case-cards.md) when selecting or teaching exemplars; read [failure and repair](examples/failure-and-repair.md) whenever speeches, post hoc accounts, copied news, or test-label shortcuts are central.

## Mandatory workflow

### 1. Diagnose the question

Write one sentence each for outcome, puzzle, case, time boundary, proposed cause, inferential target, and contribution. Define the outcome before explaining it. Distinguish an event's proper name from a theoretical category.

Stop and reframe if the question asks only whether X covaries with Y, if C or O cannot be identified, or if the available record cannot in principle contain evidence about the proposed mechanism. A design-only deliverable remains valid; invented evidence does not.

### 2. Map the literature and source environment

Separate three corpora:

1. method sources justify design and inference;
2. theory sources justify C, O, mechanism, scope, and rivals;
3. case sources establish observations.

Record metadata, access status (`metadata`, `abstract`, `full-text`, `primary-record`), locator, and permitted claims. Metadata never supports a substantive case claim. Search for disconfirming and rival-specific material, not only focal-theory terms.

### 3. Build explanations before interpreting observations

Enter the focal explanation and at least one plausible alternative in `competing-explanations.csv`. Alternatives may be complementary; do not force mutual exclusivity. Include an evidence-generating alternative whenever a source might be strategic, retrospective, copied, censored, or selectively preserved.

### 4. Specify the mechanism

For each step record entity, activity, input, output, context, expected timing, and productive link to the next step. Name the object and direction of the changed state: which belief, preference, coalition, capability, rule, or resource changed, from what to what. Use nouns for entities and verbs for activities. A label such as “persuasion,” “pressure,” or “socialization” is not a mechanism until it specifies who does what to whom, through what transmission, under which conditions, and with what changed state.

Use `mechanism-evidence-matrix.csv`. Mark necessary or bottleneck steps in the ledger. If a claimed link is only an arrow, the mechanism gate fails.

### 5. Design case-specific propositions before evidence collection

For every step write at least one proposition about an observable fingerprint and one disconfirming observation. Ask:

- theoretical certainty: if this activity occurred, how likely is this fingerprint?
- theoretical uniqueness: if the focal activity did not occur, how likely is this fingerprint?
- what else could generate it?
- where, when, and in which source genre should it appear?

Do not begin with “find proof.” Begin with a discriminating search plan. If evidence was discovered during exploration, label it discovery material and seek independent validation.

### 6. Select cases and delimit time

Map cause, outcome, context, accessibility, and likely mechanism heterogeneity in `case-comparison.csv`.

- Theory-testing/building normally begins with a typical C+/O+ case in which the mechanism could operate.
- Theory-revision uses a C+/O− deviant-consistency case only after operation was established in a typical case.
- Explaining-outcome selects the historically important outcome itself and does not claim population generalization.

Set start, end, critical junctures, expected lags, and rival timelines. When institutions or outcome paths have different procedural durations, define case-specific windows and run at least one shorter/longer window sensitivity check. Never select a case because it offers only vivid confirming material.

### 7. Collect and criticize sources

Give every document or testimony a source ID and every baseline dependency lineage a family ID. Evaluate authenticity, proximity, competence, motive, genre, access, and preservation process. Because dependence is proposition-specific, use `source-dependence-matrix.csv` whenever two or more sources support the same important proposition; a pair may be independent for event date but dependent for motive.

Record observations separately from interpretation in `evidence-register.csv`. Mark prompt-supplied or hypothetical facts that have no inspectable source as `scenario-stipulated, unaudited`; they can support conditional reasoning but not a source-verified factual conclusion. A reliable observation can be nondiagnostic; a diagnostic statement can be unreliable. Public speeches, memoirs, interviews, press reports, and missing archives require explicit generation-process analysis.

### 8. Reconstruct sequence and evaluate evidence

Build `timeline.csv`; every analytic event must link to step and evidence IDs. A timestamp alone does not establish transmission.

For found evidence assess empirical meaning, reliability, uniqueness, and source independence. For absent evidence assess both theoretical certainty and access probability. Label evidence as pattern, sequence, trace, or account, but never infer strength from type alone.

### 9. Update and aggregate

Use qualitative priors and likelihood comparisons by default. Numbers are allowed only when their elicitation and sensitivity are defensible. For each evidence item compare its expectedness under the focal and best alternative explanation, then adjust for reliability and dependence in `bayesian-update.csv`.

Aggregate bottom-up:

1. observation to proposition;
2. proposition to mechanism step;
3. step to mechanism;
4. mechanism to bounded claim.

Evidence travels only one level at a time. Claims can never be stronger than the weakest necessary step supporting them. Dependent reports count as one family, not many votes. Stop collecting when new material is cumulative and no longer changes a proposition.

### 10. Analyze alternatives and counterfactuals

For each rival specify its own process and fingerprints, evidence friendly to it, evidence unfriendly to it, and compatibility with the focal mechanism. Use counterfactuals only when antecedent, minimal rewrite, causal pathway, and comparative world are explicit and historically possible.

Do not say “ruled out” unless the rival is genuinely incompatible with high-quality evidence. Prefer “weakened,” “not adjudicated,” “complementary,” or “outside the evidentiary reach.”

### 11. Write and visualize from the ledgers

Each analysis unit follows this order:

1. theoretical function of the step;
2. case-specific condition and timing;
3. entity and activity;
4. highest-value evidence with source context;
5. transmission to the next step;
6. comparison with the best alternative;
7. update and limitation.

Generate mechanism diagrams, timelines, evidence heatmaps, or alternative trees only from registered IDs. Captions state what the visual establishes and what it does not. Background chronology is shortened unless it changes a causal inference.

### 12. Audit before delivery

Run:

```bash
python3 scripts/audit_project.py PATH_TO_PROJECT
python3 scripts/validate_skill.py PATH_TO_THIS_SKILL
```

Then complete the human gates in [quality gates](references/quality-gates.md). If any blocking gate fails, revise or explicitly downgrade the conclusion. Never report completion from file existence alone.

## Hard gates

These rules override deadlines, requested confidence, and polished narrative:

1. No mechanism without entity + activity + transmission + timing + context.
2. No evidence strength from “before/after,” source prestige, or test label alone.
3. No smoking-gun label without a focal-versus-alternative likelihood justification and source audit.
4. No negative inference from missing evidence without high expected observability and documented access.
5. No triangulation without source-family independence.
6. No decisive mechanism claim with an unsupported necessary step.
7. No “alternative eliminated” merely because focal evidence was found.
8. No exact posterior when inputs are impressionistic.
9. No factual detail from metadata, abstract-only access, an example template, or model memory.
10. No citation, locator, quotation, archive reference, or interview detail that was not verified.

## Uncertainty and stopping language

Use four claim states:

- `established observation`: directly supported and source-audited;
- `supported inference`: best current explanation with bounded confidence;
- `open inference`: plausible but not adjudicated;
- `unavailable`: evidence could not be accessed or does not exist in the record.

For retrospective audits where focal evidence is already known, reconstruct the pre-evidence prior explicitly and label it `retrospective prior reconstruction`; never present it as a genuinely preregistered belief. If the same evidence inspired the mechanism, mark the run `evidence-aware discovery` and require new nonoverlapping validation material. Scenario-stipulated observations cap the conclusion at a preliminary conditional inference until their sources are checked.

## Rapid-delivery mode

When time is extremely short, reduce breadth before reducing evidentiary discipline:

1. define O and the decision threshold;
2. select one focal mechanism and one strongest rival;
3. identify the bottleneck step and its highest-value proposition;
4. audit the top source family and any post-outcome material;
5. produce a minimal timeline, one update table, and a conclusion ceiling.

Use minimalist resolution if a systems analysis cannot be supported in time, and label it a plausibility probe or preliminary design. Never fill skipped steps with narrative certainty.

If evidence is thin, deliver the best completed design, populated search matrix, and explicit adjudication needs. Never fill a gap with a plausible story.

## Minimum deliverable

A full research execution returns:

- project contract and design memo;
- literature/source map;
- case-selection table and bounded timeline;
- mechanism–observable matrix;
- source, evidence, claim, update, and rival registers;
- integrated analysis or manuscript section;
- at least one useful analytic visual when three or more steps/branches are involved;
- audit report containing passes, warnings, blocking failures, and conclusion ceiling.

For a smaller request, produce the relevant subset but preserve IDs and hard gates.
