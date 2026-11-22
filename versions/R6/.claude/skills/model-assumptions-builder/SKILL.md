---
name: model-assumptions-builder
description: Extract and maintain global and method-specific mathematical-model assumptions from the problem frame, active method cards, data profile, and risk probes, while leaving necessity and impact judgments to the human modeler.
---

# Inputs

- problem parse;
- active method cards;
- data profile and risk-probe summaries;
- question dependency map;
- existing assumptions and human decisions.

Read legacy candidate pools only during migration.

# Workflow

1. Extract explicit problem assumptions and method-induced assumptions.
2. Remove filler statements that do not affect model validity or interpretation.
3. For each assumption record:
   - scope and source;
   - modeling need;
   - applicable method/Qx;
   - validation evidence;
   - mitigation or fallback link.
4. Identify conflicts across Qx.
5. Present unresolved necessity/impact trade-offs in one compact choice card where possible.
6. Log human `assumption_necessity` decisions in `qx_decisions.jsonl`.
7. Save `planning/model_assumptions.md`, transcribing settled human labels and impacts with decision IDs.

# Assumption Fields

- ID;
- statement;
- scope;
- source and modeling need;
- human-confirmed type: necessary or simplifying;
- validation method/evidence;
- impact if violated;
- mitigation/fallback;
- decision ID.

# Rules

- Do not invent generic assumptions such as “data are accurate” unless they affect a real dependency.
- Do not finalize necessary/simplifying or impact judgments for the human.
- Do not leave many repeated sentinels in the final file; collect missing judgments through a choice card and stop finalization until answered.
- Revisit an assumption only when its method, evidence, or downstream use materially changes.

# Verification

- Every assumption has a modeling need and source.
- Human-owned labels trace to decisions.
- Probe/robustness evidence addresses load-bearing assumptions.
- Cross-Qx conflicts are resolved or explicit.

# R6 canonical machine contract

Authoritative JSON schemas: [report-binding](../workflow-orchestrator/schemas/report-binding.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.

For a durable/final readable report, save `planning/assumptions.json` using [report-binding.schema.json](../workflow-orchestrator/schemas/report-binding.schema.json), report_kind=assumptions, its report hash and actual input hashes. Global symbols/assumptions/references use question_id=null; per-Q reports use the real question ID.
