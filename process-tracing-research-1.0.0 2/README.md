# Process-Tracing Research Skill

`process-tracing-research` is a reusable research operating system for causal-mechanism analysis in international relations, comparative politics, and adjacent social sciences. It converts a question and source corpus into linked design, mechanism, evidence, timeline, updating, claim, visual, and quality-control artifacts.

## What is distinctive

- Mechanisms are systems of entities and activities, not labels between X and Y.
- Predicted fingerprints are specified before evidence is interpreted.
- Theoretical diagnosticity is separated from source reliability and access.
- Dependence is tracked with source-family IDs, so copied reports cannot inflate support.
- Proposition-level source pairs are audited separately because independence can change with the claim being tested.
- Focal and competing explanations receive parallel likelihood assessment.
- Prose and visuals are generated from the same registered IDs.
- Deterministic scripts catch structural errors; substantive gates catch inferential overreach.

## Install

Copy the whole directory to an Agent Skills location, for example:

```bash
cp -R process-tracing-research ~/.agents/skills/process-tracing-research
```

Keep the directory intact because `SKILL.md` progressively loads `references/`, `templates/`, and `examples/`.

## Typical invocations

- “用过程追踪解释某项政策为什么在这个案例中发生，并比较两个竞争机制。”
- “把这个理论的因果机制拆成实体—活动—经验指纹，并设计取证计划。”
- “审查这篇案例研究是否把时间先后误当成因果证据。”
- “基于这些档案、访谈和新闻材料写一节可审计的机制分析。”
- “为一个正案例和一个偏离案例设计理论修正型过程追踪。”

## Start a project

Copy the files in `templates/` into a new project directory, preserve headers, and replace the instructional rows with project data. Use `examples/mini-case/` as a structural example only. The Tannenwald worked example demonstrates argument form but does not license unverified factual reuse.

Field meanings, controlled vocabularies, and multi-ID delimiters are defined in `templates/SCHEMA.md`.

## Validate

```bash
python3 scripts/validate_skill.py .
python3 scripts/audit_project.py examples/mini-case
```

Exit code `0` means no blocking structural issue was detected. Warnings still require substantive judgment. Exit code `1` means the report contains blocking errors.

## Intellectual basis

The central operating framework is derived from Beach and Pedersen's *Process-Tracing Methods* (2nd ed., 2019), supplemented by original methods research on process tracing, evidence tests, Bayesian updating, causal mechanisms, active citation, case selection, sequence, and counterfactual reasoning. See `references/bibliography.md` for verified metadata and links.

## Limits

The Skill does not make inaccessible records observable, turn biased sources into neutral ones, or make single-case findings automatically generalizable. Its numerical fields are not a scoring machine. Automated checks can detect missing links and duplicated families; they cannot decide whether a historical source is truthful or a rival is substantively plausible.

## License and versioning

Version `1.0.0` is released under the MIT License for the original Skill materials. Third-party scholarship remains under its own terms; see `THIRD-PARTY-NOTICES.md`. The directory is designed to be tracked as an independent Git repository.
