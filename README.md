# 数学建模 B 题 Skill 与强化训练

一套面向国赛 B 题的团队数学建模工作流，覆盖拆题、方法比较、代码审查、稳健性检查和结果冻结。这里收录我们从历年题目中归纳规则、用留出题做盲测，再按失败证据修订 Skill 的全过程。

2026 年国赛 B 题，两支队伍使用了同一套 Skill。我们队获上海赛区三等奖，使用同一套 Skill 的同学队获全国二等奖。留存的同学分享包为 R4。两队具体的赛时运行配置未做独立核验，获奖按队伍反馈记录。

## 从这里开始

| 我想看 | 入口 |
| --- | --- |
| 训练是怎么做的 | [训练过程与迭代记录](training/README.md) |
| 赛题、优秀论文和专家讲评 | [训练资料入口](training/corpus/README.md) · [68 条来源目录](training/corpus/catalog.csv) |
| 盲测后改了哪些规则 | [三轮盲测复盘](training/holdout.md) · [阶段证据](training/evidence) |
| 自己跑一次 | [练习与复验](training/practice.md) |
| 和队友共用一版 | [R4 同学分享包](packages/B-LEAN-20260909-R4.zip) · [R6 门控强化包](packages/B-LEAN-20260910-R6.zip) |

## 版本

| 版本 | 主要变化 |
| --- | --- |
| [R1 候选](versions/R1) | 在拆题、方法和代码之间传递信息边界、目标角色、硬约束与上游产物。 |
| [R2 发布](versions/R2) | 2025 B 盲测后，把有效分析域及其事前判据加入方法和代码审查。 |
| [R3 候选](versions/R3-candidate) | 2025 C 盲测后，加入数据对账、基线公平比较、跨切分稳定性与弃判口径。 |
| [R4 分享版](versions/R4) | 2025 A 盲测后，检查筛选是否丢失可行方案，把稳定性证据绑定到实际选中结果。 |
| [R5 解法强化](versions/R5) | 给常见问题结构补充条件化的求解与验证路线。 |
| [R6 门控强化](versions/R6) | 增加版本化 Schema、机械门控、结果冻结和依赖过期检查。 |

选择版本后，在同一队的独立工作区使用该版本。从版本内的 `README-zh.md` 或 `repo/README-zh.md` 开始，再看中文开场提示词。R6 使用新的产物契约，迁移旧工作区时可先读 [R6 变更说明](versions/R6/docs/R6-review-zh.md)。

[发布包校验值](SHA256SUMS) · [2026 国赛 B 题参赛归档](https://github.com/Alton-90/cumcm-2026-problem-b) · [华数杯初版 Skill](https://github.com/Alton-90/huashu-modeling-skills)

本项目基于 Zhijun Zhang 的 [MathModeling-skills](https://github.com/zhnnky329/MathModeling-skills)。各版本保留上游说明和 MIT 许可。训练来源见[资料索引](training/corpus/README.md)。
