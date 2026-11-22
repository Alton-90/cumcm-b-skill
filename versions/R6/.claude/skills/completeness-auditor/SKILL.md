---
name: completeness-auditor
description: Audit whether the semantic evidence required by the active lean or submission profile exists and is current, without requiring one verbose artifact per skill or an arbitrary number of pass bullets.
---

# Purpose

Check deliverable evidence, not whether every invoked skill left a ceremonial report.

# Lean Checks

Per active Qx, require as applicable:

- manifest;
- method card;
- human decision ledger;
- risk-probe summary;
- latest run summary.

Lean completeness does not require final reports, freeze, paper, or G6 artifacts.

# Submission Checks

Per Qx require:

- final method explanation;
- current language review JSON with all required named checks passing;
- final result analysis;
- robustness report;
- solution package;
- current frozen numbers;
- paper section and referenced figures.

Globally require symbols, assumptions, references and the already-passed consistency audit. Never require this completeness audit itself or any QA artifact. Final order is consistency → completeness → QA.

# Workflow

1. Read `rigor_profile`.
2. Resolve active Qx from manifests or artifacts.
3. Check required artifacts and semantic fields.
4. Check staleness only against materially cited evidence.
5. Read legacy reports for context only; migrate to the canonical schema before passing a machine gate.
6. Save named semantic checks to `paper/audits/completeness.json`; optional Markdown is a rendering. Run validate_workspace.py --audit-stage completeness; the program computes mechanical status.

# Status

- `PRESENT`: required evidence exists and is current.
- `MISSING`: required evidence absent.
- `INSUFFICIENT`: artifact exists but required semantic fields/checks are missing.
- `STALE`: cited material evidence changed after approval/review.
- `NOT_APPLICABLE`: justified by task/profile.

# Rules

- Do not require `≥5` prose pass items.
- Do not require a report just because a skill ran.
- Do not mark a decision stale for unrelated code, formatting, or file changes.
- Do not treat legacy artifact count as proof of semantic completeness.
- Do not repair artifacts during audit.

# Verification

- Requirements match the active profile.
- Every gap names the missing evidence and producer/owner.
- Staleness links to a material changed source.
- Final verdict is `PASSED` only when all submission requirements are satisfied.

# R6 canonical machine contract

Authoritative JSON schemas: [audit](../workflow-orchestrator/schemas/audit.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.
