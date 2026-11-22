---
name: problem-classifier
description: Classify each parsed mathematical-modeling subquestion by required output and structure, surface ambiguous framing trade-offs for human choice, and record primary/secondary task types without selecting algorithms.
---

# Preconditions

- `planning/parse/problem_parse.json` exists and maps every Qx to an output.
- Material framing ambiguities are visible.

Read legacy parse paths only during migration.

# Task Types

Use these exact machine enums: evaluation, prediction, optimization, mechanism, classification-clustering, graph-routing, simulation, data-analysis, hybrid. Human labels such as descriptive/inference or mixed map to data-analysis or hybrid; never emit slash-delimited alternatives as enum values.

Detailed cues: `references/task-type-guide.md`.

# Workflow

1. Classify from the required output, decision structure, constraints, and relationships—not keywords alone.
2. Assign:
   - primary type;
   - optional secondary type;
   - confidence;
   - evidence from the parse;
   - consequences for validation and deliverables.
3. Identify mixed or ambiguous framings that would change what the team can claim.
4. For a load-bearing ambiguity, invoke one choice card explaining consequences. Do not silently settle it.
5. Save `planning/classification/problem_classification.json`.
6. Record the human framing decision in `methods/Qx/qx_decisions.jsonl`, or in `planning/framing_decisions.jsonl` when the Qx method directory does not yet exist.

# Output Contract

The versioned schema linked below is the only machine contract; do not copy legacy examples.

# Rules

- Do not propose or choose methods.
- Do not classify only from nouns such as “forecast” or “optimal”; verify the required output.
- A subquestion may be mixed, but avoid listing many types without prioritization.
- Human framing is required when alternative classifications lead to materially different outputs or claims.
- Do not create a long taxonomy report when the JSON record is sufficient.

# Verification

- Every Qx has one primary type.
- Mixed/secondary types are justified.
- Classification evidence resolves to the parse.
- Ambiguous framing is human-confirmed or remains a blocker.
- No algorithm selection leaked into classification.

# Reference

- `references/task-type-guide.md`

# R6 canonical machine contract

Authoritative JSON schemas: [problem-classification](../workflow-orchestrator/schemas/problem-classification.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.
