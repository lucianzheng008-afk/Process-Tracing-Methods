# GREEN and REFACTOR pressure-test report

Date: 2026-07-14  
Method: the same three agents that produced the no-Skill RED baselines re-ran their original scenarios after reading `SKILL.md` and routed references. They did not edit package files.

## Results

| Scenario | RED failure | GREEN behavior | Score |
|---|---|---|---:|
| Strategic speech + two-week policy change + five dependent reports | Correct intuition but no auditable artifacts, no focal/rival mechanism symmetry, and no conclusion ceiling | Defined C/O thresholds; decomposed four necessary steps; separated result alternatives from evidence generators; grouped reports by family; treated unavailable minutes as no update; rejected smoking-gun claim | 16/16 |
| Three-country divergent responses with unequal access | Plausible design but IDs, access asymmetry, branch logic, and likelihood reasoning were not fully disciplined | Classified the task as theory-building + structured comparison; treated prompt outcomes as unaudited; built shared and branch mechanisms; used case-specific and cross-case ceilings; separated discovery from validation; modeled time-window sensitivity | 16/16 |
| Falklands narrative under a 45-minute deadline | Fluent case narrative outran the evidence; internal record was labeled near-smoking-gun and later public statements helped support an overly strong mechanism verdict | Distinguished dispatch, limited action, and main-theater force; audited internal, public, post-action, memoir, and interview material; weakened only the “same-day war decision” rival; left the authorization bottleneck open; capped the conclusion | 15/16 |

Scoring dimensions were task fit, mechanism completeness, evidence diagnosis, alternatives, temporal reasoning, source independence, uncertainty, and prose/table consistency, each 0–2. The Falklands source-independence score was 1 because the available evidence set lacked a genuinely independent channel for private motivation; the answer exposed rather than hid this limitation.

## Behavioral changes attributable to the Skill

1. Prompt-given facts were no longer silently upgraded to source-verified observations.
2. Outcomes and decision thresholds were defined before causal claims.
3. Mechanisms used named entities, activities, state changes, transmission, timing, and bottlenecks.
4. Evidence moved observation → proposition → step → mechanism → claim through stable IDs.
5. Alternatives received their own mechanisms and unfriendly evidence.
6. Strategic speech, copied news, and retrospective accounts were treated as evidence-generation problems.
7. Source quantity was replaced by proposition-specific lineage and independence analysis.
8. Missing/inaccessible records capped conclusions instead of automatically disconfirming a mechanism.
9. Test labels no longer substituted for focal-versus-rival likelihood reasoning.
10. Deadline pressure reduced breadth and conclusion strength rather than creating certainty.

## Loopholes found and refactors applied

| Loophole found in GREEN | Refactor |
|---|---|
| Read-only tasks conflicted with “create a project directory” | Added an inline-ledger route that prohibits unauthorized writes |
| Priors were impossible to preregister in retrospective audits | Added `retrospective prior reconstruction` and `evidence-aware discovery` labels |
| Prompt-stipulated facts had unclear epistemic status | Added `scenario-stipulated, unaudited` and a preliminary conditional ceiling |
| A changed “belief” or “threat perception” could remain vague | Required the object, direction, and before/after state of every change |
| Multi-outcome cases were too easily called typical cases of one O | Added branch/stage/distinct-outcome diagnosis before case classification |
| IDs for branches and iterations were underspecified | Added lettered branches, immutable IDs, `REV-*`, and no placeholder E IDs |
| A prior could be fabricated as neutral when literature access was barred | Added `unassessed` as a valid state |
| A thin case could wrongly cap a rich case's within-case conclusion | Separated within-case ceilings from the common cross-case ceiling |
| Common time windows could hide different institutional durations | Required shorter/longer window sensitivity checks |
| Source dependence was treated too statically | Added `source-dependence-matrix.csv` for proposition-level source pairs |
| Example routing was optional and vague | Made example selection conditional on task type |
| No explicit safe mode existed for severe deadlines | Added rapid-delivery mode with five non-negotiable outputs |
| Mechanism state change was required in prose but absent from the CSV/gates | Added `change_object`, `state_before`, and `state_after` fields and Gate B checks |
| Stipulated scenario facts conflicted with evidence-ID rules | Added a distinct `stipulated` status, provenance note, and conditional ceiling |
| Revision IDs lacked a structured home | Added `revision-register.csv` and immutable revision semantics |

## Automated regression after refactor

- Unit tests: 6/6 passed.
- Package validator: PASS, 0 errors, 0 warnings.
- Valid fictional mini-case: PASS, 0 errors, 0 warnings.
- Deliberately invalid fixture: FAIL as expected with exactly five target blocking codes: missing mechanism activity, unknown source, duplicate family, no rival, and unsupported causal claim.
- Final cross-file regression: all seven targeted routes passed, including read-only/no-write, retrospective prior, stipulated evidence, named state change, branch IDs, proposition-specific dependence, and rapid-delivery mode; no blocking ambiguity remained.

## Residual limits

- The validator cannot decide whether a historian, archive, interviewee, or policymaker is truthful.
- Stable IDs and likelihood fields make reasoning auditable; they do not turn qualitative judgment into measurement.
- A GREEN score measures compliance and internal consistency, not whether a real-world mechanism is true.
- Research using confidential, restricted, or politically sensitive sources still requires case-specific ethical review.
