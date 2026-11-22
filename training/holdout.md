# 三轮留出盲测

三轮试做都先冻结当轮输出，再开始复盘。下表列出导致后来版本修订的观察。完整经过和各轮验证见[开发记录](README.md)。

| 留出题及版本 | 发现的问题 | 后续修订 |
| --- | --- | --- |
| 2025 B · R1 | 数据报告标记了异常谱段，程序仍然使用了整个区间做拟合。 | R2 将有效范围、排除依据和适用性检查写入代码计划，并检查程序实际读取的区间。 |
| 2025 C · R2 | 一处解析漏掉有效记录，部分切分上的阈值不满足硬约束。 | R3 对账输入、排除和实际使用的数据，在训练数据内校准阈值，外层按组复核，并单列弃判结果。 |
| 2025 A · R3 | 代理指标可能在筛选阶段淘汰有可行性的候选，导出方案还需要自己的稳定性证据。 | R4 保留可能可行的候选，锁定最终导出的文件与参数，再核对应约束和稳定性。 |

- **2025 B** [冻结与复验记录](evidence/tests/holdout/2025B) · [外部材料对照](evidence/p13/external_comparison.md)
- **2025 C** [冻结证据](evidence/tests/holdout/2025C) · [失败归因](evidence/p16/external_comparison_and_failure_triage.md) · [R3 行为测试](evidence/p17/candidate_behavior_test_results.json)
- **2025 A** [冻结与验收记录](evidence/tests/holdout/2025A) · [R4 改动决定](evidence/p19/revision_decision.json) · [R4 行为测试](evidence/p19/r4_behavior_test_results.json)
