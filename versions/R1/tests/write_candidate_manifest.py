"""Build the P11 manifest from hashes and already-recorded candidate evidence."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


SKILLS = (
    "problem-parser", "method-selector", "workflow-orchestrator",
    "model-code-analyzer", "python-code-reviewer", "matlab-code-reviewer",
)
ROOTS = (".claude/skills", ".codex/skills", "plugins/mathmodeling-skills/skills")
BT_LOCATORS = {
    "BT-01": ["problem-parser#Workflow: future information is forbidden", "method-selector#Workflow: forbidden future information is FAIL"],
    "BT-02": ["problem-parser#Workflow: simple static question", "python-code-reviewer#Review Schema: static/no-dependency NOT_APPLICABLE"],
    "BT-03": ["problem-parser#JSON Contract: objective_contract roles", "method-selector#Workflow: feasibility before objective comparison", "python-code-reviewer#Workflow: infeasible output fails"],
    "BT-04": ["workflow-orchestrator#Gate Evaluation: real cross_question_dependencies", "workflow-orchestrator#Gate Evaluation: no-dependency parallel progress"],
    "BT-05": ["python-code-reviewer#Rules: lookahead/scalarization/infeasibility/dependency FAIL"],
    "BT-06": ["matlab-code-reviewer#Workflow and #Verification: static checks and parity"],
    "BT-07": ["model-code-analyzer#Run Summary Contract and #Rules: shared main/baseline contract"],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_baseline(manifest, source):
    missing, mismatched = [], []
    for entry in manifest["entries"]:
        if entry["type"] != "file":
            continue
        path = source / entry["relative_path"]
        if not path.is_file():
            missing.append(entry["relative_path"])
        elif sha256(path) != entry["sha256"]:
            mismatched.append(entry["relative_path"])
    return {"expected_files": manifest["source_tree_fingerprint"]["file_count"], "missing": missing, "hash_mismatches": mismatched}


def main():
    candidate = Path(sys.argv[1])
    source = Path(sys.argv[2])
    baseline_manifest = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
    files = []
    for root in ROOTS:
        for skill in SKILLS:
            rel = Path(root) / skill / "SKILL.md"
            files.append({"path": rel.as_posix(), "baseline_sha256": sha256(source / rel), "candidate_sha256": sha256(candidate / "repo" / rel)})
    test_results = json.loads((candidate / "p11_behavior_test_results.json").read_text(encoding="utf-8"))
    pre_post = audit_baseline(baseline_manifest, source)
    payload = {
        "release_id": "B-LEAN-20260907-R1",
        "approved_change_ids": ["CHG-B01", "CHG-B02"],
        "baseline_identity": {"stage": "P0-R", "file_count": 145, "tree_fingerprint": baseline_manifest["source_tree_fingerprint"]["digest"]},
        "pre_target_integrity": {"files": 145, "missing": 0, "hash_mismatches": 0},
        "post_target_integrity": {"files": pre_post["expected_files"], "missing": len(pre_post["missing"]), "hash_mismatches": len(pre_post["hash_mismatches"])},
        "modified_files": files,
        "supporting_candidate_artifacts": ["tests/run_p11_behavior_tests.py", "tests/make_candidate_diff.py", "tests/write_candidate_manifest.py", "p11_behavior_test_results.json", "candidate_diff.patch", "candidate_change_report.md"],
        "validation": {
            "behavior_tests": test_results,
            "behavior_test_skill_evidence_locators": BT_LOCATORS,
            "quick_validate": {"command": "python -X utf8 skill-creator/scripts/quick_validate.py <each affected skill>", "validated_files": 18, "result": "PASS", "note": "Initial default-encoding attempt was NOT_RUN/encoding-limited for 6 Chinese-text files; UTF-8 rerun passed all 18."},
            "mirror_sha256": {"result": "PASS", "skills": list(SKILLS), "roots": list(ROOTS)},
            "sync_plugin_check": {"command": "bash scripts/sync-plugin.sh --check", "result": "NOT_RUN", "reason": "Windows Bash/WSL could not resolve the candidate Windows path; per-file mirror SHA-256 check passed instead."},
            "candidate_leakage_scan": {"result": "PASS", "groups": ["prohibited identifiers", "2025 answer-like content", "user-machine absolute paths"], "hash_ledger_exclusion": "The integrity hash ledger is excluded from identifier-token matching because an arbitrary SHA-256 substring is not source content."},
            "patch_roundtrip": {"command": "git -c core.autocrlf=false apply --check candidate_diff.patch; git -c core.autocrlf=false apply candidate_diff.patch", "result": "PASS", "fresh_baseline_copy": True, "applied_file_hashes_verified": 18, "hash_mismatches": 0}
        },
        "holdout_zero_access_declaration": "No designated holdout, answer-like, expert-review, training-paper, or OCR body was opened for this candidate.",
        "limitations": ["Behavior verification evaluates structured contract fixtures and explicit rules; it does not claim model execution.", "The upstream sync shell check was not runnable on this Windows Bash/WSL path."],
        "candidate_diff_sha256": sha256(candidate / "candidate_diff.patch")
    }
    (candidate / "candidate_manifest.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
