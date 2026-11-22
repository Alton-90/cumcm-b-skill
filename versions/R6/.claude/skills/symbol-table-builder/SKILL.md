---
name: symbol-table-builder
description: Build and maintain one global mathematical symbol and unit table from the problem frame and active method cards, resolving cross-subquestion conflicts before code or paper work.
---

# Purpose

Ensure the same concept uses one symbol and different concepts do not collide.

# Inputs

- problem parse and relationships;
- active `methods/Qx/qx_method_card.json`;
- approved code plans when available;
- question dependency map;
- existing `planning/symbol_table.md`.

Read legacy candidate pools only when method cards are absent.

# Workflow

1. Extract inputs, outputs, parameters, decisions, states, indices, sets, functions, and intermediate quantities.
2. Preserve user-established notation unless it conflicts or is ambiguous.
3. Resolve:
   - same meaning with different symbols;
   - different meanings with the same symbol;
   - unit/domain conflicts;
   - Qx output-to-input handoff conflicts.
4. Classify each symbol by role and scope.
5. Save or update `planning/symbol_table.md`.
6. If a canonical symbol changes, classify it `CANONICAL` and run scoped consistency for affected Qx.

# Table Fields

- symbol;
- plain name;
- definition;
- type: input, output, parameter, estimated parameter, decision, state, intermediate, index, set, function;
- domain/range;
- unit;
- scope/Qx;
- source artifact;
- notes or conflict resolution.

# Rules

- Define every symbol before first use.
- Record units and domains when applicable.
- Use one notation for cross-question handoffs.
- Do not invent variables to make a table look complete.
- Do not maintain a separate verbose conflict log; record material resolutions in the table notes.

# Verification

- Active method-card and code-plan variables are covered.
- No unresolved symbol or unit collision remains.
- Shared quantities agree across Qx.
- Downstream artifacts can cite one canonical table.

# R6 canonical machine contract

Authoritative JSON schemas: [report-binding](../workflow-orchestrator/schemas/report-binding.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.

For a durable/final readable report, save `planning/symbols.json` using [report-binding.schema.json](../workflow-orchestrator/schemas/report-binding.schema.json), report_kind=symbols, its report hash and actual input hashes. Global symbols/assumptions/references use question_id=null; per-Q reports use the real question ID.
