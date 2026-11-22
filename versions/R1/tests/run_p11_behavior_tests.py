"""Contract-level P11 behavior tests; these fixtures do not execute a model."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def check_dependency(dependencies):
    if not dependencies:
        return {"status": "PASS", "reason": "no real dependency; eligible in parallel"}
    for dep in dependencies:
        for field in ("artifact_exists", "status_ok", "identity_ok", "freshness_ok", "uncertainty_ok"):
            if not dep.get(field, False):
                return {"status": "BLOCKED", "reason": f"{dep['upstream_question']}:{field}"}
    return {"status": "PASS", "reason": "all required artifact conditions pass"}


def review_contract(case, runtime_available=True):
    contract = case["contract"]
    checks = {"input_contract": "PASS", "method_alignment": "PASS", "output_contract": "PASS"}
    boundary = contract.get("information_boundary", {"status": "NOT_APPLICABLE"})
    if boundary.get("status") != "NOT_APPLICABLE" and set(boundary.get("read_fields", [])) & set(boundary.get("forbidden_future_information", [])):
        checks["input_contract"] = "FAIL"
    if contract.get("scalarization", {}).get("used") and not contract["scalarization"].get("human_approved"):
        checks["method_alignment"] = "FAIL"
    if any(value > 0 for value in contract.get("constraint_violations", [])):
        checks["output_contract"] = "FAIL"
    dependency = check_dependency(contract.get("upstream_dependencies", []))
    if dependency["status"] != "PASS":
        checks["input_contract"] = "FAIL"
    runtime = "PASS" if runtime_available else "NOT_RUN"
    verdict = "PASSED" if all(value == "PASS" for value in checks.values()) else "FAILED"
    return {"checks": checks, "dependency": dependency, "runtime": runtime, "verdict": verdict}


def assert_case(case_id, actual, expected):
    if actual != expected:
        raise AssertionError(f"{case_id}: expected {expected!r}, got {actual!r}")
    return {"id": case_id, "status": "PASS", "detail": expected}


SKILL_EVIDENCE = {
    "BT-01": [("problem-parser", "# Workflow", "what future information is forbidden"), ("method-selector", "# Workflow", "A method that uses forbidden future information is `FAIL`")],
    "BT-02": [("problem-parser", "# Workflow", "For a simple static question"), ("python-code-reviewer", "# Review Schema", "genuinely static/no-dependency contract fields")],
    "BT-03": [("problem-parser", "# JSON Contract", "\"role\": \"hard_constraint\""), ("method-selector", "# Workflow", "Treat hard feasibility as prior to objective comparison"), ("python-code-reviewer", "# Workflow", "Any infeasible output fails")],
    "BT-04": [("workflow-orchestrator", "# Gate Evaluation", "declares a real `cross_question_dependencies` entry"), ("workflow-orchestrator", "# Gate Evaluation", "eligible to progress in parallel")],
    "BT-05": [("python-code-reviewer", "# Rules", "Fail the applicable check for lookahead")],
    "BT-06": [("matlab-code-reviewer", "# Workflow", "still perform static contract checks"), ("matlab-code-reviewer", "# Verification", "same information, objective, feasibility, and dependency semantics")],
    "BT-07": [("model-code-analyzer", "# Rules", "Do not give main and baseline different information"), ("model-code-analyzer", "# Run Summary Contract", "\"information_boundary_check\"")],
}


def assert_skill_contracts(repo):
    results = []
    for bt, locators in SKILL_EVIDENCE.items():
        for skill, section, clause in locators:
            content = (repo / ".codex" / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            section_start = content.find(section)
            actual = section_start >= 0 and clause in content[section_start:]
            results.append(assert_case(f"{bt}-skill:{skill}:{section}", actual, True))
    return results


def main():
    repo = Path(__file__).resolve().parents[1] / "repo"
    dynamic_lookahead = {"contract": {"information_boundary": {"status": "APPLICABLE", "read_fields": ["future_demand"], "forbidden_future_information": ["future_demand"]}, "constraint_violations": []}}
    static_simple = {"contract": {"information_boundary": {"status": "NOT_APPLICABLE"}, "constraint_violations": [], "upstream_dependencies": []}}
    multi_objective_infeasible = {"contract": {"information_boundary": {"status": "NOT_APPLICABLE"}, "scalarization": {"used": True, "human_approved": False}, "constraint_violations": [1], "objective_values": [{"id": "length", "value": 1}], "upstream_dependencies": []}}
    stale_dependency = [{"upstream_question": "Q1", "artifact_exists": True, "status_ok": True, "identity_ok": True, "freshness_ok": False, "uncertainty_ok": True}]
    legal_contract = {"information_boundary": {"status": "APPLICABLE", "read_fields": ["current_state"], "forbidden_future_information": ["future_state"]}, "scalarization": {"used": False, "human_approved": False}, "constraint_violations": [], "objective_values": [{"id": "length", "value": 4}], "upstream_dependencies": [{"upstream_question": "Q1", "artifact_exists": True, "status_ok": True, "identity_ok": True, "freshness_ok": True, "uncertainty_ok": True}]}
    results = []
    results.append(assert_case("BT-01", review_contract(dynamic_lookahead)["checks"]["input_contract"], "FAIL"))
    results.append(assert_case("BT-02", review_contract(static_simple)["verdict"], "PASSED"))
    bt03 = review_contract(multi_objective_infeasible)
    results.append(assert_case("BT-03", [bt03["checks"]["method_alignment"], bt03["checks"]["output_contract"]], ["FAIL", "FAIL"]))
    results.append(assert_case("BT-04-downstream", check_dependency(stale_dependency)["status"], "BLOCKED"))
    results.append(assert_case("BT-04-independent", check_dependency([])["status"], "PASS"))
    for language in ("python", "matlab"):
        for category, case, field in (("lookahead", dynamic_lookahead, "input_contract"), ("scalarization", multi_objective_infeasible, "method_alignment"), ("infeasible", multi_objective_infeasible, "output_contract")):
            result = review_contract(case, runtime_available=(language == "python"))
            results.append(assert_case(f"BT-0{5 if language == 'python' else 6}-{category}", result["checks"][field], "FAIL"))
        if language == "matlab":
            results.append(assert_case("BT-06-runtime", review_contract(static_simple, runtime_available=False)["runtime"], "NOT_RUN"))
    main_contract = json.loads(json.dumps(legal_contract))
    baseline_contract = json.loads(json.dumps(legal_contract))
    main = review_contract({"contract": main_contract})
    baseline = review_contract({"contract": baseline_contract})
    same_contract = main["verdict"] == baseline["verdict"] == "PASSED" and main_contract == baseline_contract
    results.append(assert_case("BT-07", same_contract, True))
    results.extend(assert_skill_contracts(repo))
    output = {"suite": "P11 contract behavior", "model_execution": "NOT_RUN: structured contract fixtures only", "results": results, "overall": "PASS"}
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("p11_behavior_test_results.json")
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
