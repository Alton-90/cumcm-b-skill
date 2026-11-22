---
name: modeler-decision-logger
description: Faithfully append a human modeler's choice and rationale to one canonical per-subquestion JSONL decision ledger. Use after a choice card is answered or when migrating legacy decision artifacts; never originate or improve the decision.
---

# Purpose

Make human judgment traceable without multiplying decision files.

# Canonical Output

`methods/Qx/qx_decisions.jsonl`

One JSON object per line. Records are append-only.

Use `planning/framing_decisions.jsonl` for global/pre-Qx framing decisions.

# Required Fields

The versioned schema linked below is the only machine contract; do not copy legacy examples.

Optional structured fields may include confidence, rejected alternatives, round action, claim scope, assumption labels, or fallback activation.

# Workflow

1. Receive the human's answer, the choice-card ID, and evidence paths.
2. Preserve the user's meaning and wording. Normalize only structure, identifiers, and whitespace.
3. Verify:
   - the choice is one of the presented options or explicitly records a user-supplied alternative;
   - evidence paths exist;
   - rationale is non-empty and contains no placeholder;
   - the record does not falsely label AI-authored prose as human-authored.
4. Append one JSON line.
5. If revising a decision, append a new record with `supersedes`; never overwrite history.
6. Update the compact history in `qx_method_card.json` only when the decision changes method state.
7. Update the manifest gate/status fields when present.

# Decision Types

Typical values:

- `framing`
- `method_choice`
- `fallback_activation`
- `result_verdict`
- `stability_verdict`
- `assumption_necessity`
- `claim_scope`
- `package_signoff`
- `submission_authorization`

# Staleness

Mark a decision stale only when its cited evidence materially changed:

- append a `decision_stale` record naming the old decision and changed evidence;
- ask the human to reconfirm through one choice card;
- do not mark decisions stale because unrelated files or formatting changed.

# Legacy Migration

Read legacy:

- `methods/Qx/qx_decision_log.md`
- `methods/Qx/decisions/*_modeler_decision.md`

Migrate only completed human decisions. Preserve original timestamps and source paths when available. Do not convert PENDING placeholders into decisions.

# Rules

- Never choose, rationalize, strengthen, or complete the user's decision.
- Never create a separate pending decision artifact.
- Never copy `ai_suggestion` into the human rationale.
- One evidence-linked sentence is enough; do not impose arbitrary prose length.
- Preserve an honest AI-use provenance distinction.

# Verification

- JSONL is valid one-object-per-line.
- Record is append-only and uniquely identified.
- Human ownership and evidence are accurate.
- Supersession and staleness preserve history.

# R6 canonical machine contract

Authoritative JSON schemas: [decision](../workflow-orchestrator/schemas/decision.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.
