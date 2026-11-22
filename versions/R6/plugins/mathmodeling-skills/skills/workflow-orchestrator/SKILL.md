---
name: workflow-orchestrator
description: Inspect a mathematical-modeling workspace, evaluate lean or submission gates per subquestion, update machine-readable manifests, classify change impact, and route one next action without duplicating downstream work.
---

# Purpose
Read current evidence and execute gates. Do not invent modeling judgments or solve the model here.

# Canonical contracts
Read [workspace-contract](references/workspace-contract.md) and [gate-runtime](references/gate-runtime.md). Schema owners: [session](schemas/session.schema.json), [manifest](schemas/manifest.schema.json), [gate-result](schemas/gate-result.schema.json). All other producer schemas are in schemas/ and referenced by their skills. The R6 contracts supersede legacy path/examples; old artifacts are read-only migration inputs.

# Workflow
1. Determine active Qx from planning/parse/problem_parse.json and the current profile from planning/session_config.json. Do not create a full workspace unless requested.
2. Read manifest.latest_run as an index, never trust current_gate/status as proof. Inspect actual evidence.
3. Execute scripts/validate_gate.py with --workspace, --question and the proposed gate; use validate_workspace.py for final scope. Treat nonzero exit or unavailable dependencies as blocked. Report the actual mechanical result and its limits, never overwrite it with a self-authored PASS.
4. Route the first failed precondition to its producer, preserving existing user decisions/authorization. Missing user evidence is not permission to invent it. For uncertainty compatibility, method validity, baseline meaning and claim scope, obtain semantic review in addition to machine checks.
5. Before model generation require G2.5; before freezing require G4A and current sign-off, using freeze_results.py. Evidence-only freeze does not advance G4B. Before paper handoff require G4B. Before final assembly rerun G6 across every active question.
6. Rerun only affected checks during lean exploration. In submission, final audit order is consistency → completeness → QA. Completeness has no self or QA dependency.

# Gates and state changes
G1 PROBLEM_FRAMED → G2 METHOD_SCREENED → G2.5 METHOD_CHOSEN → G3 CODE_AND_EXPERIMENT_REVIEWED → G4A RESULTS_JUDGED → G4B RESULTS_FROZEN → G5 PAPER_SECTION_READY → G6 FINAL_AUDIT_PASSED.
G4A may represent a judged failure; G4B requires task completion, selected-output robustness and current freeze in submission. On profile change or any referenced source change, recompute; never infer G4B from a legacy G4 or cached label.

# Semantic guardrails
Carry the R4 information boundary, prospective analysis domain, input-population accounting, group-safe operating point and abstention semantics, feasibility/interaction-preserving candidate screening, defensible continuous constraints and exact-selection robustness through producer checks. The script verifies mechanical evidence and selected fingerprints; it does not prove these modeling assumptions.
An infeasible objective, hidden missing required output or unsupported interpretation must remain a semantic failure even if schemas pass. Do not convert a nonfunctional diagnostic into a usable baseline.

# Execution boundary
Local scripts are not a privileged host hook and cannot prevent an equally privileged writer from bypassing them. Never claim tamper-proof enforcement. Only current program output establishes mechanical status, while reviewers remain responsible for semantic conclusions.
