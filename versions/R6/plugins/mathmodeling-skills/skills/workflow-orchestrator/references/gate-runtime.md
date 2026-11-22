# 确定性机械门控及其边界

## 使用
Python 3.10+与jsonschema>=4.18,<5。完整发行包可运行根目录scripts下的同名命令；单技能树/插件从workflow-orchestrator/scripts运行。单树安装可用 `python -m pip install -r <workflow-orchestrator>/scripts/requirements.txt`。安装依赖失败、读入失败、Schema错误均应阻塞，不能降级为“模型自行判断通过”。

```bash
python scripts/validate_gate.py --workspace ROOT --question Q1 --gate G3 --output planning/gates/Q1-G3.json
python scripts/validate_workspace.py --workspace ROOT --gate G5
python scripts/validate_workspace.py --workspace ROOT --audit-stage consistency
python scripts/validate_workspace.py --workspace ROOT --audit-stage completeness
python scripts/validate_workspace.py --workspace ROOT --audit-stage qa
python scripts/freeze_results.py --workspace ROOT --question Q1 --mode complete
python scripts/check_staleness.py --workspace ROOT --artifact results/Q1/reports/frozen_numbers.json
```

退出码0只表示当前命令机械检查PASS；非0阻塞。JSON输出保留checked_files快照与limits。动作前重新调用，不把之前输出文件当成永不过期的许可，也不信任manifest.current_gate或手写audit.verdict。结果文件只允许写planning/gates/，不能覆盖已检查输入。

## 门控链
- G1：审题、分类、数据画像、真实存在的framing来源及上游引用。
- G2：唯一主候选与可用基线、对应风险探针。
- G2.5：有效方法选择及对应证据。
- G3：主方法/基线运行、输出、批准匹配、所有实际语言审查和哈希；数据计数契约适用时检查对账。
- G4A RESULTS_JUDGED：当前选择的稳健性记录及结果/稳定性/论断范围决定。允许已明确判断失败的结果。
- G4B RESULTS_FROZEN：submission、输出义务全部满足、当前选择稳健性PASS、程序冻结及最终报告绑定。
- G5：论文段落绑定当前freeze；需要的图表已渲染且源文件当前。
- G6：所有审题中的Q先过G5；再consistency→completeness→QA，检查全局符号、假设与引用证据。不能仅验证一个Q就放行整个提交。

## 无环审计
consistency不依赖completeness或QA；completeness只依赖consistency，不依赖自己或QA；QA依赖前两者。审计输入绑定当前各Q论文、freeze、图表及全局报告。记录检查结果后执行相应audit-stage命令；该命令检查记录的充分性和先决条件，不代替六类/五类语义审查本身。
局部consistency记录可保存单Q scope，最终审计必须覆盖全部Q。只有变动引用涉及的下游报告需要重审；哈希变动使已绑定的后续审计过期，重新运行按依赖顺序处理。

## 冻结与旧结果
freeze_plan使用RFC6901 JSON Pointer，如 /rmse 或 /rows/0/value，不接受未经定义的$.foo或OCR行号。数值从被选方法登记的JSON输出读取，拒绝布尔、NaN与不存在指针。冻结不接受人工提供value。使用--replace-reason重新冻结时保留旧快照并追加日志；需要当前签署证据。
证据留存使用--mode evidence_only，允许保留已判断失败，但G4B拒绝该模式。此举不解决未完成的题目。若降级论断，必须在真实任务要求与批准范围内重建一致证据链。

## 不能承诺什么
这些脚本不是Codex底层拦截器：拥有相同文件写权限的代理或人仍能不调用脚本或修改脚本。本版本提供可复算执行门控，不是不可绕过的安全边界。要硬性阻止提交，应由受保护CI/宿主动作调用验证器；本包没有安装或宣称已安装这样的机制。
脚本检查的是证据文件与声明一致性。语义正确、原始用户身份、实验确实运行、图像真的人工看过，不能仅由同一代理可写的JSON证明。核心审查状态仍由负责审查者产生；机械状态只能由程序计算，不得互相冒充。
