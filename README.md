# 国赛 B 题数学建模 Skill

这套 Skill 用于团队建模。它把拆题、数据核查、方法比较、Python 或 MATLAB 实现、稳健性检查和论文写作串在一个工作区里。选择主方案时，要先写清可用信息、硬约束和比较对象。论文定稿时，要能查到每个数字来自哪次运行。

2026 年国赛 B 题，我们队和另一支同学队使用了同一套 Skill，分别获得上海赛区三等奖、全国二等奖。留存的同学分享文件是 R4。获奖和使用情况由队伍提供。 [我们队的 B 题论文与代码](https://github.com/Alton-90/cumcm-2026-problem-b)

## 使用哪个版本

| 版本 | 用途 |
| --- | --- |
| [R4 同学分享包](packages/B-LEAN-20260909-R4.zip) | 查看当时用于团队协作的版本，以及盲测后写入的输入、约束和结果核对规则。 |
| [R5 解法强化包](packages/B-LEAN-20260910-R5.zip) | 查阅有条件的解法设计，例如哪些状态可以合并，以及怎样设计追加实验来区分两个模型。 |
| [R6 流程校验包](packages/B-LEAN-20260910-R6.zip) | 在新项目中使用结构化产物、结果冻结和依赖过期检查。 |

各队使用独立工作区，队内先统一版本。解压后从版本里的 `README-zh.md` 和 `Initial Prompt-zh.md` 开始。以 R6 为例，在解压目录中运行以下命令，将项目文件安装到已建立的比赛目录。

```bash
bash install.sh --mode project --target codex --project-dir /path/to/contest
```

如果使用 Claude Code、插件模式或已有工作区，参阅 [R6 安装说明](versions/R6/README-zh.md#安装)及[迁移说明](versions/R6/docs/R6-review-zh.md)。发布包的哈希值用于核对队友拿到的是否为同一版。 [SHA-256 校验值](SHA256SUMS)

## 开发过程

初版先从 2018、2020–2024 年的 B 题和 19 篇训练论文提炼可迁移的做法。2025 年赛题作为留出题。每轮先用固定版本做题并冻结结果，随后回看失败发生在题意、数据、方法还是验证环节，再决定需要修改哪些 Skill。

| 版本 | 该轮解决的问题 |
| --- | --- |
| [R1 候选](versions/R1) | 拆题结果须写清每个时点能获得哪些信息、硬约束是什么、下游程序要读取哪些产物。代码审查按同一份约定检查。 |
| [R2 发布](versions/R2) | 2025 B 盲测标记了异常谱段，拟合仍读入整个区间。R2 要求在选方法前说明分析域及排除依据，并核对代码实际读取的范围。 |
| [R3 候选](versions/R3-candidate) | 2025 C 盲测发现解析时丢失了有效记录，阈值在一些切分上也失去稳定性。R3 增加逐步样本对账、训练内校准、分组复核和弃判覆盖率。 |
| [R4 发布](versions/R4) | 2025 A 盲测暴露了候选筛选和定稿证据之间的断点。R4 要求保留可能可行的方案，并把约束与稳定性证据对应到实际导出的候选。 |
| [R5 强化](versions/R5) | 为调度、实验、定位、覆盖等问题补写方法选择的适用条件、最小验证和反例。 |
| [R6 强化](versions/R6) | 统一需要程序读取的文件格式，让校验脚本重新检查上游文件、选中方案与论文数字，并区分结果已审阅与可定稿。 |

开发记录附有各轮的冻结证据、改动决定和测试结果。R4 的 54 条行为检查、56 条回归检查，以及 R6 的 28 项合成测试均有记录。 [详细开发记录](training/README.md) · [三轮盲测](training/holdout.md) · [复验步骤](training/practice.md)

## 训练资料

- [语料目录](training/corpus/catalog.csv)记录 68 项来源及官方入口，包括赛题、附件、优秀论文和讲评。
- [19 篇论文对照矩阵](training/evidence/analysis/lean/b_training_source_matrix.json)记载方法、使用条件、验证方式和能迁移的做法。
- [建模任务拆解](training/evidence/analysis/lean/b_training_problem_contracts.json)、[训练综合笔记](training/evidence/analysis/lean/b_training_synthesis.md)和[合成练习数据](training/fixtures/decision-cases.csv)可直接查阅。

第三方原文与附件从发布方页面获取，资料页标明了来源和链接粒度。 [资料说明](training/corpus/README.md)

## 许可

本项目的 Skill、工作流代码与原创合成练习采用 [MIT 许可证](LICENSE)。各版本保留 Zhijun Zhang 的 [MathModeling-skills](https://github.com/zhnnky329/MathModeling-skills) 署名与上游许可。第三方赛题、论文、讲评与数据的权利以来源说明为准。
