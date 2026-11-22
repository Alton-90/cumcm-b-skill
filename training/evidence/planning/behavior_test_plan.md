# B题精简候选行为测试计划

范围：只测试 `CHG-B01` 与 `CHG-B02` 声称改变的行为。P11 不做全仓库无差别复验，不使用 2025 holdout。

## 必测行为

| ID | 场景 | 预期行为 | 覆盖变更 |
| --- | --- | --- | --- |
| BT-01 | 动态决策题仅允许看到截至当期的信息 | problem parse 明确决策顺序、当期可见信息与禁用未来信息；使用未来信息的候选在筛查时 FAIL 或带修复条件的 CONDITIONAL | CHG-B01 |
| BT-02 | 静态、单目标、各问独立的小题 | 新字段为 NOT_APPLICABLE 或紧凑空值，不制造额外选择卡，不阻止原流程 | CHG-B01 回归 |
| BT-03 | 同时含硬覆盖约束、最小长度目标和超限重叠报告指标 | 三类量被分别标记；在没有人工决定时不得自动加权；不可行但长度更短的方案不能通过 | CHG-B01、CHG-B02 |
| BT-04 | Q4明确消费Q1估计及其区间，但Q1产物缺失或已变 | workflow-orchestrator 阻止Q4进入相应下游门禁，并指出缺失/过期的上游产物；无依赖的Q2仍可推进 | CHG-B01 |
| BT-05 | Python代码读取未来时点字段、静默标量化目标或输出约束违反 | 对应 `input_contract`、`method_alignment` 或 `output_contract` 为 FAIL，不能以总目标更优覆盖失败 | CHG-B02 |
| BT-06 | MATLAB/北太天元计划同样出现上述三类违约 | 与Python reviewer保持同一行为语义；运行不可用时仍可检查静态契约，但运行项用NOT_RUN | CHG-B02 |
| BT-07 | main与baseline均合法且使用同一信息/目标/约束合同 | 两者可比较，run summary分别保存目标值、约束违反、上游输入身份和适用的信息边界检查 | CHG-B02 |

## 结构与镜像检查

- 修改前确认目标文件哈希仍等于P0基线；漂移即停止。
- 每个受影响SKILL.md运行skill-creator quick validation。
- `.claude/skills/`、`.codex/skills/`、`plugins/mathmodeling-skills/skills/` 对应文件逐字节一致。
- 运行 `scripts/sync-plugin.sh --check`；环境不能运行时如实记为NOT_RUN并用逐文件哈希替代，不声称脚本通过。
- 扫描候选仓库：不得包含训练论文正文、OCR全文、2025答案型材料或本机绝对路径。

## 通过标准

- 所有适用的正向与负向行为均符合预期；任何负向案例被错误放行即 BLOCKED。
- BT-02必须通过，防止B题增强把简单通用题流程变重。
- CHG-B02只有在CHG-B01获批并实现后才可测试或合入。
- 只重跑受影响Skill与镜像检查；不因无关文件要求全仓库重验。

## 停止条件

- 需要改变用户已确认的人工判断边界。
- 需要新增Skill而不是最小编辑现有Skill。
- 目标仓库或基线文件发生无法解释的漂移。
- 必须读取2025 holdout才能让测试通过。

证据来源：`cumcm-b-skill/analysis/pattern_gap_map.json` 的 `gap_items`、`proposed_change_bundles` 与对应 `upstream_evidence_refs`。
