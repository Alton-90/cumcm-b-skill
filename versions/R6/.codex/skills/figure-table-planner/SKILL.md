---
name: figure-table-planner
description: Plan the smallest set of diagnostic, comparison, paper, and appendix figures or tables needed to support verified mathematical-modeling decisions and claims.
---

# Purpose

Make every visual evidence-bearing. Prefer fewer useful visuals over a decorative inventory.

# Inputs

- method card and decision ledger;
- run summaries and final result analysis;
- robustness evidence;
- solution package and frozen numbers in submission mode;
- existing figures/tables.

# Figure Types

- Type 1 diagnostic: internal debugging; never in the paper.
- Type 2 comparison: main vs usable baseline or a genuinely tested alternative; optional in paper.
- Type 3 paper: directly supports a main claim; required only when the claim benefits materially from a visual.
- Type 4 appendix: supplementary evidence referenced from the main text.

# Workflow

1. List verified claims that need visual or exact tabular support.
2. Reuse an existing artifact when it already communicates the claim.
3. For each proposed visual record:
   - ID and Qx;
   - type;
   - source artifact and frozen claim IDs when applicable;
   - one core claim;
   - chart/table form;
   - target section;
   - status and render needs.
4. Ask the human to confirm judgment-bearing Type 3 claims through one compact choice card when they are not already in the decision ledger.
5. Save `methods/Qx/qx_figure_table_plan.json` when durable planning is needed; submission requires this JSON even when figures is empty (supply no_visual_reason). A companion Markdown view is optional. Lean exploratory discussion alone does not require a plan artifact.

# Planning Heuristics

- Use tables for exact values, parameters, and small comparisons.
- Use plots for trends, distributions, sensitivity, or many-item comparisons.
- Use diagrams for mechanisms, dependencies, and workflows.
- A main-vs-baseline figure needs compatible metrics and the same evaluation setup.
- Do not create a multi-method comparison merely to imply breadth.

# Rules

- Type 1 never enters the paper.
- Type 3 uses final validated sources and a human-confirmed core claim.
- Do not use unresolved exploratory figures as paper evidence.
- Do not fabricate data, captions, or claims.
- Do not fill plans with placeholder sentinels; pause for one human choice instead.
- Every visual must have a source and purpose.

# Verification

- Each planned visual supports a verified claim.
- Types, sources, sections, and statuses are explicit.
- Type 3 claims trace to human decisions and frozen evidence.
- No unnecessary or decorative visual remains.

# R6 canonical machine contract

Authoritative JSON schemas: [figure-plan](../workflow-orchestrator/schemas/figure-plan.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.
