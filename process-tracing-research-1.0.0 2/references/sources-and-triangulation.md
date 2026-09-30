# Sources and triangulation

## Source register principle

A source is a produced artifact, not a transparent window. Record who created it, for what audience, with what access, incentives, genre conventions, and preservation path. Assign one `source_id` per artifact and one conservative baseline `source_family_id` per underlying information lineage.

## Core questions

1. Is it authentic and complete?
2. Could the creator know the reported fact?
3. How many steps separate creator and event?
4. Was the creator competent to perceive or record it?
5. What audience and purpose shaped it?
6. What motives favored candor, silence, exaggeration, or blame shifting?
7. Is it representative or a selected survivor?
8. Does it depend on another registered source?
9. What exact claim may it support?
10. What would it be unsafe to infer from it?

## Genre cautions

### Official records

Minutes, memoranda, cables, and orders can be close to decisions but remain curated. Determine who attended, who drafted, whether dissent was recorded, whether language was sanitized, and whether later declassification was selective.

### Public speeches and press releases

Strong for what was communicated publicly and sometimes for strategic positioning. Usually weak for private motivation without independent internal evidence. Audience costs or rhetorical constraint are separate propositions that must be demonstrated.

### Memoirs and retrospective interviews

Useful for leads, sequence, and actor interpretation. Vulnerable to hindsight, reputation management, memory decay, rehearsal, and exposure to public accounts. Verify timing and seek contemporaneous records.

### Elite interviews

Record role, date, access, question wording, anonymity, recall horizon, and possible coordination. Three interviews are not triangulation if interviewees consulted the same minutes or shared a common public narrative.

### News

Useful for public chronology and contemporaneous claims. Trace wire copy, pooled reporting, official briefings, and unnamed-source chains. Five outlets citing one official equal one family for that proposition.

### Secondary histories

Map historiographic schools, source bases, and theoretical assumptions. A respected book may synthesize primary sources well but remains secondary evidence. Trace distinctive claims back to the cited record when stakes are high.

### Quantitative and administrative records

Audit definitions, collection incentives, missingness, revisions, and temporal granularity. A pattern may establish context while remaining silent on actor activity.

## Independence test

Two items are independent **for proposition P** only if learning one does not make the other substantially more expected through copying, shared informants, coordination, or common record selection. Independence is not an intrinsic document property: an internal minute and public speech may independently record their own dates but share one governmental account of motive.

Document:

- lineage and citations;
- common informants or briefing channels;
- whether one source read another;
- institutional coordination;
- whether sources have genuinely different information channels;
- degree of independence: `dependent`, `partly independent`, `independent`, `unknown`.

Default to `unknown` or `partly independent` when proof is unavailable. Never reward an uncertainty with full duplicate weight.

When two or more sources bear on an important proposition, fill `source-dependence-matrix.csv` for each relevant pair. The baseline family is conservative; a proposition-level upgrade to `independent` requires a different information channel and written justification. A proposition-level downgrade always controls aggregation.

## Triangulation

Triangulation is not majority voting. Strong triangulation combines different source-generation processes whose weaknesses are not correlated, such as a contemporaneous internal record, a material trace, and an independently situated observer.

Convergence matters only after:

1. sources are independently generated for the proposition;
2. each can competently observe it;
3. their incentives do not produce the same false account;
4. wording is not suspiciously copied;
5. the convergent observation discriminates among explanations.

## Search and access log

For every important not-found item log:

- repository/database;
- collection and file series;
- date searched;
- keywords and names;
- date range;
- access restrictions;
- missing or closed files;
- expected coverage;
- result.

This turns “no evidence” into an auditable statement about detection probability.

## Ethical and legal boundaries

- Use lawful access and respect archive, interview, privacy, and data-protection rules.
- Do not fabricate interview metadata or infer identities from anonymized sources.
- Separate confidential material from publishable claims.
- Preserve exact locators privately even when the public output must redact them.
- Flag security or harm risks before publishing sensitive causal attributions.

## Claim permission

Use the `permitted_claims` field narrowly. Examples:

- `public statement on date X` — allowed by the transcript;
- `actor privately believed Y` — not allowed from that transcript alone;
- `document records proposal Z` — allowed;
- `proposal caused decision` — requires mechanism evidence beyond document existence.
