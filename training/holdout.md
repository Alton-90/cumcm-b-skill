# 三轮盲测怎么改变了 Skill

| 留出题与使用版本 | 盲测暴露的问题 | 写回 Skill 的规则 |
| --- | --- | --- |
| 2025 B · R1 | 异常谱段已被标记，整个数据区间仍被送入拟合。后续回退保留了不确定性，但前端缺少分析域门槛。 | 在选择依赖局部结构的方法前，记录分析域、排除理由和适用性检查。主线和基线使用可比较的输入口径。 |
| 2025 C · R2 | 解析或筛选后的样本范围没有完整对账，关键阈值在不同切分下不稳，弃判口径也影响比较。 | 对账审核、解析、排除与实际使用的记录数。对阈值实行组间隔离的校准和外层复核，报告弃判覆盖率。 |
| 2025 A · R3 | 代理指标过早筛掉可能可行的候选，导出结果缺少与选中方案一致的稳定性证据。 | 筛选优先保留可行性与关键交互。导出前针对实际选中产物核对约束、稳定性与来源。 |

**2025 B** [冻结与复验记录](evidence/tests/holdout/2025B) · [外部对照](evidence/p13/external_comparison.md)

**2025 C** [冻结证据](evidence/tests/holdout/2025C) · [失败归因](evidence/p16/external_comparison_and_failure_triage.md) · [R3 行为测试](evidence/p17/candidate_behavior_test_results.json)

**2025 A** [冻结与验收记录](evidence/tests/holdout/2025A) · [候选改动决策](evidence/p19/revision_decision.json) · [R4 行为测试](evidence/p19/r4_behavior_test_results.json)

练习时可以用同样流程做一轮新的留出题。先冻结输入合同、主线与基线的输出，再用题目和外部材料回看一个失败点。
