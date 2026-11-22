---
name: problem-parser
description: Parse a mathematical-modeling problem into goals, objects, data, constraints, outputs, subquestions, dependencies, variables, relationships, and human-confirmed success criteria before any method selection.
---

# Purpose

Produce a model-neutral problem contract. Do not start from favorite algorithms or infer missing attachments.

# Inputs

- complete problem statement and attachments list;
- contest rules and required deliverables;
- user clarifications;
- existing parse when revising.

# Workflow

1. Record source files and missing referenced material.
2. Extract the global objective and each Qx verbatim enough to preserve intent.
3. For each Qx identify:
   - goal;
   - objects/entities;
   - inputs and data;
   - decisions or unknowns;
   - hard and soft constraints;
   - required output and format;
   - evaluation/success criteria;
   - dependencies on other Qx;
   - when decisions occur, what information is visible then, what future information is forbidden, and how state updates, when the question is dynamic or staged;
   - each quantity's role as a hard constraint, optimization objective, or report-only measure, including direction, unit, aggregation, threshold, and any unresolved trade-off;
   - typed cross-question dependencies: upstream Q, required artifact and state, identity/version/hash, freshness, and uncertainty compatibility.
   - an `analysis_domain_contract` when a downstream calculation relies on local structure such as periodicity, stationarity, smoothness, or a valid measurement range: eligibility property, prospective inclusion/exclusion rule, decision time, evidence, and unresolved boundary choices. Record `NOT_APPLICABLE` for methods that use the full domain without such a requirement.
   - uncertainty and ambiguity.
4. Separate:
   - statement facts;
   - observations from supplied data;
   - proposed relationships;
   - assumptions requiring human judgment.
5. If output form, success criteria, or a material objective trade-off is ambiguous, invoke one choice card. Do not choose the framing silently. For a simple static question, record `NOT_APPLICABLE` or compact empty values for the new fields and do not create a card merely because those fields exist.
6. Save:
   - `planning/parse/problem_parse.json`
   - an optional concise `planning/parse/problem_parse.md` only when a human-readable view is useful.
7. Update the manifest status when present.

# JSON Contract

The versioned schema linked below is the only machine contract; do not copy legacy examples.

# Rules

- Parse before classifying.
- Do not name or recommend methods.
- Do not fabricate data, fields, equations, causal relationships, or evaluation criteria.
- Preserve units, time ranges, populations, and output formats.
- Keep the existing `dependencies` list for compatibility; use `cross_question_dependencies` only for real execution dependencies, not conceptual references.
- Do not treat information unavailable at a decision time as an input, or silently resolve an objective trade-off.
- Do not treat disclosure of invalid, nonstationary, nonperiodic, saturated, or otherwise ineligible observations as sufficient when the planned calculation relies on the violated property. Preserve the affected domain and the still-unresolved eligibility rule explicitly.
- A proposed relationship must be labeled as proposed until human-confirmed or evidence-supported.
- Ask only about ambiguities that change the downstream problem.

# Verification

- Every subquestion maps to a required output.
- Constraints and dependencies are explicit.
- Dynamic contexts expose their information boundary and state update; static contexts remain compact.
- Objective roles and applicable upstream artifact identities are explicit before downstream use.
- Structure-dependent calculations have a prospective analysis-domain contract or an explicit blocker; post-result band selection is not silently authorized.
- Missing attachments and ambiguities are visible.
- Facts, proposals, assumptions, and decisions are separated.
- Human-owned success criteria are confirmed or remain a blocker.

# R6 canonical machine contract

Authoritative JSON schemas: [problem-parse](../workflow-orchestrator/schemas/problem-parse.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.
