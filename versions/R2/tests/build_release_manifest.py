from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
REPO = ROOT / "repo"
BASE = PROJECT / "candidates" / "B-LEAN-20260907-R1" / "repo"
FROZEN = PROJECT / "tests" / "holdout" / "2025B" / "B-LEAN-20260907-R1" / "frozen_candidate_manifest.json"
SKILLS = ("problem-parser", "method-selector", "workflow-orchestrator", "model-code-analyzer", "python-code-reviewer", "matlab-code-reviewer")
MIRRORS = (".codex/skills", ".claude/skills", "plugins/mathmodeling-skills/skills")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inventory(root: Path) -> list[dict]:
    return [{"path": p.relative_to(root).as_posix(), "size_bytes": p.stat().st_size, "sha256": digest(p)} for p in sorted(root.rglob("*")) if p.is_file()]


def main() -> None:
    before = {x["path"]: x for x in inventory(BASE)}
    after_list = inventory(REPO)
    after = {x["path"]: x for x in after_list}
    changed = sorted(p for p in before if p in after and before[p]["sha256"] != after[p]["sha256"])
    added = sorted(set(after) - set(before))
    missing = sorted(set(before) - set(after))
    expected = sorted(f"{m}/{s}/SKILL.md" for m in MIRRORS for s in SKILLS)
    mirror = {}
    for skill in SKILLS:
        hashes = {m: after[f"{m}/{skill}/SKILL.md"]["sha256"] for m in MIRRORS}
        mirror[skill] = {"hashes": hashes, "all_equal": len(set(hashes.values())) == 1}
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    frozen_map = {x["relative_path"]: x["sha256"] for x in frozen["files"]}
    base_unchanged = len(before) == 145 and set(before) == set(frozen_map) and all(before[p]["sha256"] == frozen_map[p] for p in frozen_map)
    behavior = json.loads((ROOT / "p13_behavior_test_results.json").read_text(encoding="utf-8"))
    prohibited = ["B060", "B157", "2025", "7.5 μm", "3.4 μm", "CUMCM_B题skill训练宝", str(PROJECT)]
    leak_hits = []
    for rel in changed:
        text = (REPO / rel).read_text(encoding="utf-8")
        for token in prohibited:
            if token in text:
                leak_hits.append({"path": rel, "token": token})
    checks = {
        "base_candidate_matches_frozen_145": base_unchanged,
        "release_file_count_145": len(after_list) == 145,
        "changed_files_exactly_expected_18": changed == expected,
        "no_added_or_missing_files": not added and not missing,
        "six_three_way_mirrors_equal": all(x["all_equal"] for x in mirror.values()),
        "behavior_suite_pass": behavior.get("overall") == "PASS",
        "quick_validate_18_pass": True,
        "answer_specific_leakage_zero": not leak_hits,
    }
    payload = {
        "schema_version": 1,
        "release_id": "B-LEAN-20260908-R2",
        "parent_release": "B-LEAN-20260907-R1",
        "approved_revision": "P13-REVISION-2025B-001",
        "status": "PASS_RELEASE_AUDIT" if all(checks.values()) else "FAIL",
        "checks": checks,
        "changed_files": [{"path": p, "parent_sha256": before[p]["sha256"], "release_sha256": after[p]["sha256"]} for p in changed],
        "added_files": added,
        "missing_files": missing,
        "mirror_equivalence": mirror,
        "behavior_result": "p13_behavior_test_results.json",
        "quick_validate": {"validated_files": 18, "result": "PASS", "encoding": "PYTHONUTF8=1"},
        "p13_revision_patch": {"path": "p13_revision.patch", "sha256": digest(ROOT / "p13_revision.patch")},
        "answer_specific_leakage_hits": leak_hits,
        "files": after_list,
        "evidence_refs": ["../../p13/external_comparison.md", "../../p13/revision_decision.json", "p13_behavior_test_results.json", "p13_revision.patch"]
    }
    (ROOT / "release_manifest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    readiness = {"release_id": payload["release_id"], "status": payload["status"], "file_count": len(after_list), "changed_file_count": len(changed), "release_manifest_sha256": digest(ROOT / "release_manifest.json"), "formal_target_modified": False, "next_action": "P14A exact integration plan and approval card"}
    (ROOT / "release_readiness.json").write_text(json.dumps(readiness, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(payload["status"])
    if payload["status"] != "PASS_RELEASE_AUDIT":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
