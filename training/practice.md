# 练习与复验

## 用合成数据复习三个常见失败

[练习数据](fixtures/decision-cases.csv) 是为公开复验新编的 8 行合成数据。

1. **信息边界**。做一个顺序决策基线。对每行只允许使用当时可见的 `observed_signal`。先从代码中搜出误用 `future_outcome` 的路径，再记录一条反例。
2. **可行性优先**。筛选 `eligible=1` 的记录后再比较 `candidate_score`。核对两组分别有几行可行，并指出全局得分最高的记录为什么不会被选中。
3. **样本对账**。按 `group` 留组评测。分别报告总数、可用数和排除数，让主方案和基线共享同一组评测记录。确认导出的组别和行号能回到原始输入。

核对顺序可与 [R2 发布审计](evidence/qa/lean/P14B_final_release_audit.json)、[R3 候选测试](evidence/p17/candidate_behavior_test_results.json)及 [R4 改动决策](evidence/p19/revision_decision.json) 对照。

## 跑 R6 自带的合成检查

在仓库根目录用 Python 3.12 或 3.13 执行。

```bash
python -m pip install jsonschema
python -B -X utf8 versions/R6/scripts/test_gate_runtime.py
```

命令在临时工作区构造样例，覆盖门控、Schema、产物哈希和冻结链路。测试结束会重写本地的 `versions/R6/docs/R6-runtime-tests.json`。发布包内的同名记录可用于对照。
