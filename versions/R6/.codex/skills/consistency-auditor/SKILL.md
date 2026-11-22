---
name: consistency-auditor
description: Run scoped or final cross-media consistency checks for mathematical-modeling artifacts, comparing canonical numbers, symbols, parameters, decisions, files, and paper claims without performing full-workspace audits for low-risk changes.
---

# Modes

- `scoped`: run only for a `CANONICAL` or `FROZEN` change and only for affected Qx/identifiers.
- `final`: run across all submission artifacts before assembly.

# Sources of Truth

Prefer:

- `frozen_numbers.json` for paper numbers;
- `qx_decisions.jsonl` for human judgments;
- `planning/symbol_table.md` for symbols/units;
- approved code plan and run summary for parameters and executed methods;
- solution package for writer-facing structure.

Use legacy decision logs or Markdown reviews only during migration.

# Checks

1. Numerical claims match frozen values and units.
2. Formula, parameter, constraint, and method roles match approved code and plan.
3. Symbols and units match the global symbol table.
4. Referenced tables, figures, code, and data files exist.
5. Why-this-method, result verdict, stability, confidence, and claim scope resolve to human decision IDs.
6. Freeze and decisions are not stale relative to materially changed cited evidence.

# Scoped Workflow

1. Receive changed files/identifiers and their impact class.
2. Resolve affected Qx and downstream consumers.
3. Check only those relationships.
4. Return a compact digest or save `results/Qx/reports/scoped_consistency.json` (audit.schema.json, audit_kind=consistency and scope=[Qx]) when durable evidence is needed.
5. Do not rewrite other artifacts.

# Final Workflow

1. Check all submission Qx.
2. Save `paper/audits/consistency.json`.
3. Run validate_workspace.py --audit-stage consistency after recording named checks. Report its mechanical status separately from semantic findings.
4. List concrete divergences and repair owners. Do not pad a pass list.

# Rules

- Do not run a full audit for formatting, comments, scratch work, or ordinary pre-freeze exploration.
- Do not infer canonical numbers from the paper.
- Do not repair divergences inside the audit.
- Do not approve final assembly directly.

# Verification

- Scope matches the semantic impact.
- Every divergence identifies source, consumer, and expected repair.
- Final audit covers all six check classes.
- Verdict follows actual evidence rather than an item count.

# R6 canonical machine contract

Authoritative JSON schemas: [audit](../workflow-orchestrator/schemas/audit.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.
