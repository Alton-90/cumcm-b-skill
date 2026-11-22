# 我们怎么做强化训练

这里的训练对象是 Skill 的规则、提示词、工作流和验证脚本。训练记录里的数字描述语料范围或测试结果。

## 1. 先约定资料怎么用

从 2018、2020–2024 年的 B 题和附件出发，定向检查 19 篇训练论文，每个年度选一篇代表作深读。分开记录题面约束、论文作者的方法、作者报告的结果和我们归纳的模式。OCR 难以判读的公式和参数保留缺口，不拿来填题面事实。将 2025 年的答案类材料放入留出区，先做题并冻结输出，然后再看适用的论文或讲评。

[资料目录](corpus/README.md) · [语料审计](evidence/planning/corpus_audit.md) · [19 篇论文对照矩阵](evidence/analysis/lean/b_training_source_matrix.json) · [PDF 派生质量报告](evidence/preprocessing/pdf_qa_report.md)

## 2. 把失败变成可以复验的规则

先固定候选版、输入、允许读取的材料和验收条件。盲测结束后保存结果与文件摘要，再对照题目要求和可用的外部资料。每轮只把跨题仍成立的改动写回通用 Skill，随后补一个正例与一个反例进行检查。

[三轮盲测复盘](holdout.md) · [原验证计划](evidence/planning/behavior_test_plan.md) · [训练记录索引](evidence)

## 3. 候选通过回归之后再发布

R2 回接审计记录了 36 条行为断言。R4 记录了 54 条行为断言、56 条回归断言和 27 项 Skill 校验，三套 Skill 分发目录也核对了文件一致性。R5 增加解法设计和 17 项窄机制测试。R6 用 28 项合成用例检查运行时门控，包括缺少基线、篡改冻结值、旧 Schema 和依赖过期。

这些测试覆盖各版的规则与工程机制。真实赛题的预测或优化性能、独立团队复用效果和竞赛成绩需要各自的证据。

[R2 回接审计](evidence/qa/lean/P14B_final_release_audit.json) · [R4 回接审计](evidence/qa/lean/P20B_R4_final_release_audit.json) · [R5 测试](evidence/R5/R5-validation.json) · [R6 测试](evidence/R6/R6-runtime-tests.json)

公开证据保留原判定、历史摘要与校验结果，去除了本机路径和原始对话。记录中的历史哈希用于标识当时的产物。
