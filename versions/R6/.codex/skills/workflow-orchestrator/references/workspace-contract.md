# R6 唯一路径与机器产物契约

新工作区统一使用正斜线相对路径。Qx实际写Q1/Q2等；文件前缀qx实际写q1/q2等。机器状态为JSON；决策保留追加式JSONL，每行都是同一decision schema的JSON。论文、推导、代码计划和可读报告可以是Markdown/TeX，它们不自行授予门控状态。

## 路径与Schema
所有Schema位于本技能的 `../schemas/`。这是唯一逻辑源；Codex、Claude及插件为独立安装入口，携带字节一致的生成副本，并非三份独立维护的契约。

| 产物 | 唯一新写入路径 | Schema文件名（后缀.schema.json） |
|---|---|---|
| 会话 | planning/session_config.json | session |
| 审题 | planning/parse/problem_parse.json | problem-parse |
| 分类 | planning/classification/problem_classification.json | problem-classification |
| 数据画像 | planning/data/data_profile.json | data-profile |
| 原始/清洗数据 | data/raw/、data/clean/ | 原始数据格式不强套流程Schema |
| 共用清洗脚本 | code/shared/ | 不适用 |
| 文献分析 | planning/literature/related_paper_analysis.md及同名.json | report-binding |
| 方法卡 | methods/Qx/qx_method_card.json | method-card |
| 方法卡可读副本 | methods/Qx/qx_method_card.md | 非状态源 |
| 风险探针 | methods/Qx/probes/risk_probe_summary.json | risk-probe |
| 决策台账 | methods/Qx/qx_decisions.jsonl | decision（逐行） |
| 最新运行索引 | planning/manifests/Qx.json | manifest |
| 代码计划 | code/Qx/qx_code_plan.md | 非状态源 |
| Python/MATLAB代码 | code/Qx/python/、code/Qx/matlab/ | 不适用 |
| 代码审查 | code/Qx/reviews/qx_python_review.json或qx_matlab_review.json | review |
| 运行摘要 | results/Qx/experiments/roundN/run_summary.json | run-summary |
| 指标JSON | results/Qx/experiments/roundN/metrics/ | 任务定义；由运行输出登记哈希，不强套流程Schema |
| 稳健性 | robustness/Qx/qx_robustness_summary.json | robustness |
| 图表计划 | methods/Qx/qx_figure_table_plan.json | figure-plan |
| 冻结计划 | results/Qx/reports/freeze_plan.json | freeze-plan |
| 冻结数字 | results/Qx/reports/frozen_numbers.json | frozen-numbers |
| 最终方法/结果/稳健性/交接报告绑定 | results/Qx/reports/method_explanation.json、final_analysis.json、robustness_report.json、writer_package.json | report-binding |
| 论文段落绑定 | paper/sections/qx.json | report-binding |
| 符号/假设绑定 | planning/symbols.json、planning/assumptions.json | report-binding |
| 引用核验绑定 | paper/references.json | report-binding |
| 审计 | paper/audits/consistency.json、completeness.json、qa.json | audit |
| 机器检查输出 | planning/gates/任意名称.json | gate-result |

report-binding.report保存原文文件path/sha256；inputs保存其实际依赖。方法说明等仍可放原有方法/报告目录；绑定JSON按上表写。重要报告依赖至少含当前run和robustness；论文绑定必须含冻结数字。全局绑定question_id=null。

## 通用字段
所有受管理JSON均有schema_version=2、artifact_type。inputs为依赖引用数组，每项有path与sha256；所有额外自定义字段进入extensions。研究内容的开放对象（如parameters、metrics_summary）由任务自己定义，不假装通用Schema能验证科学语义。
SHA-256使用文件原始字节。改动任意已引用内容（包括格式）会保守地使引用过期；不声称能判断改动的科学重要性。无关且未被引用的文件改变不影响门控。重新绑定只能发生在复核之后，不能批量刷新哈希来掩盖未复核变更。
同一文件同一快照不能登记冲突哈希；引用需可解析、在工作区内，禁止绝对路径和..逃逸。

## 主要字段约定
- 分类枚举：evaluation、prediction、optimization、mechanism、classification-clustering、graph-routing、simulation、data-analysis、hybrid。
- main_candidate、usable_baseline用于方法卡；运行中对应main、usable_baseline。主方法与基线必须不同ID且均有成功运行、脚本和输出。当前严格门控不接受failed运行冒充已完成基线；调整方法后需要新的批准与运行。
- core review checks：syntax、input_contract、method_alignment、reproducibility、output_contract，均需PASS和证据。其他不适用检查可NOT_APPLICABLE并说明原因。
- inputs绑定了上游数据，required_status比较上游status/verdict的原值；uncertainty_requirement由语义审查确认，机械脚本只检查该字段存在、哈希和状态，不自动证明不确定性兼容。
- run.output_obligations逐项声明id/satisfied/evidence。G4B要求全部满足；改小题目要求必须先由用户确认并更新审题/证据，不能仅写claim downgrade跳过。
- 审计六类consistency checks：numbers、symbols、methods、claims、references、freshness；completeness：required_artifacts、evidence_fields、freshness；qa：workflow_integrity、evidence_integrity、method_quality、paper_quality、presentation。
- decision.source提供用户消息导出或用户提供的记录、哈希、原文摘录、定位。脚本核验存在和摘录，不证明作者身份；agent_under_authorization不能伪称human。全局framing可保留用于阅读，但门控使用每Qx明确的framing记录，可引用同一全局原始授权。
- 方法选择记录selected_methods包含主方法和基线ID；稳定性、结果及claim_scope记录绑定同一run和robustness；package_signoff绑定freeze_plan和run。
- selected_fingerprint由 `Workspace.fingerprint(Qx)` 对选择配置与当前run哈希规范化计算，不能人工近似拼写。改参数/组合/评价器/分辨率/运行会改变指纹。

## 旧版迁移
旧路径、schema_version=1和旧G4只读；不得静默当作新门控通过。迁移时先保留旧文件，写新路径记录，补来源并实际复核。遇到未执行、无来源或未知字段必须保留未验证/阻塞，不能伪造时间或人类决定。
旧G4在lean至多作为“待核验G4A”的线索；切submission后重新验证G4B，不能直接沿用旧current_gate。旧method-plan/qa等模板已从templates删除；不要在同一文件里维护两套schema。
