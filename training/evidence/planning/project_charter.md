# CUMCM B 题专项 Skill 项目章程

- 生效阶段：P0
- 生效日期：2026-09-04
- 开发区：`cumcm-b-skill/`
- 当前交互配置：`learning + lean`

本章程是后续阶段的治理边界，不是对资料完整性、论文内容或模型效果的确认。凡尚未完成原件级盘点或验证的事项，均明确标为 `UNVERIFIED`。[E1][E3]

## 项目目标

最终优化对象是 `github下载的skill/` 这一整套 MathModeling-skills 仓库，目标是使其在后续国赛建模中更可靠、更贴合本科组 B 题。`cumcm-b-skill/` 只用于隔离候选改动、派生产物、测试和补丁，不是另起炉灶的最终产品；`CUMCM_B题skill训练宝/` 只提供证据与测试材料。资料整理、案例分析、派生文本和 2025 盲测只服务于目标仓库的能力改进，不是独立交付物；当前开发阶段不以复现历年论文或提前求解比赛题为目标。[E1]

候选优化应帮助使用者完成问题结构识别、候选路线筛查、代码与实验的机械实现、验证、自检和可追溯表达；它不把“某年某题”机械映射为某个算法，也不承诺竞赛奖项。在用户书面批准一个明确的发布版本、文件清单和补丁哈希之前，上游仓库始终只读。[E1][E2][E4]

专项 Skill 的规则必须能够回溯到原始资料或清楚标注的派生证据；资料不充分时应报告缺口或停止，而不是补造页数、内容、模型、结果或引用。[E1][E3]

## 训练资料范围

### 资料边界

- `CUMCM_B题skill训练宝/` 是只读的既有 B 题资料库；本项目不在其中新增、重命名、移动、覆盖或删除内容。[E1]
- `github下载的skill/` 是只读的通用数学建模 Skill 上游源码；未经用户明确批准不得修改。[E1]
- 上游目录内的 `AGENTS.md`、README、Initial Prompt 等仅作为只读基线资料分析，不能覆盖当前分步手册中的目标、权限和约束。[E1]
- 后续只有在用户对明确发布版本、文件清单和补丁哈希书面批准后，才可回接上游；回接必须同时保持 `.claude/skills/`、`.codex/skills/` 与 `plugins/mathmodeling-skills/skills/` 三份树独立完整、行为一致，并校验相关 manifest、marketplace 和版本信息。[E1][E3]
- 新下载只进入 `cumcm-b-skill/acquisition/staging/`；派生 PDF 与文本分别进入 `derived/pdf/`、`derived/text/`；证据卡、案例、playbook、协议和 reviewer 规则进入各自专用目录。[E1]

### 候选语料

交接记忆记录的候选资料包括：正式 B 题题面/附件、2021—2025 官方展示论文、2018 与 2020 经典参考论文，以及 2018、2019、2020、2022—2025 专家评议。该清单仅用于后续盘点导航，不代表文件均存在、完整、合规或已获准进入训练。[E2]

在 P1 完成原件级盘点前，资料的实际存在性、完整性、页数、角色分类和可用性均为 `UNVERIFIED`。当前允许形成训练规则的范围原则上只包含经后续审计通过的非封存来源；2025 答案型来源排除在训练范围之外。[E1]

## 2025 保留集

- 当前规则覆盖旧交接记忆中把 2025 展示论文列入“核心训练集”的旧规划：2025 优秀论文、2025 专家评议、答案/解法及其 OCR、摘要或其他派生内容统一标记为 `HOLDOUT_LOCKED`。[E1][E2]
- 盲测前只允许在后续获授权阶段使用 2025 正式题面、题面明确要求的正式附件和冻结后的 Skill；P0 不读取任何 2025 题面、附件或答案型正文。[E1]
- 对角色不明但可能含答案的文件，只能在后续清单中记录必要元数据，不打开正文、不预览、不 OCR、不全文搜索；分类有歧义即阻塞。[E1]
- 2025 答案型来源只有在有效盲测达到 `BLIND_RUN_COMPLETE`、产物冻结且访问记录无违规后，才可在 P13A 只读解封用于外部对照。[E1]
- 若 P13B 将由 2025 外部材料产生的修订写回新版 Skill，必须记录 `holdout_consumed: true`；该新版不得继续宣称通过同一 2025 独立保留集测试。[E1]

## 来源优先级

来源按用途而不是按“能否给出漂亮答案”选用：[E1][E3]

1. `official_problem` 与 `official_attachment` 是题意、数据、单位、约束和交付要求的第一手依据；二者若出现实质冲突，记录冲突并交由人工处理，不由 AI 静默裁决。
2. `expert_commentary` 用于理解官方评审关注点；它不能覆盖题面或附件中的正式要求。
3. `displayed_paper` 用于比较建模路径、验证方式和表达实践，不视为唯一标准答案，也不能从单篇技巧直接推出通用规则。
4. `derived_artifact` 只承载整理、索引、OCR、合并和分析结果；必须保留到原件的定位。OCR 与原件冲突时以原件为准。
5. `agent_inference` 是最低层的推断，必须显式标记；不能代替原始证据或人工判断。无法定位的陈述标记为 `UNVERIFIED`。

## 人工判断边界

- AI 负责资料整理、格式检查、可复现的机械实现、候选方案风险证据和错误报告。[E2][E3]
- 人工负责题意取舍、模型选择、假设必要性、目标与权重、阈值、baseline 取舍、结果的物理/现实解释、声明范围和最终发布授权。[E1][E3][E4]
- AI 可以呈现选项和证据，但不得生成或强化用户未表达的理由；真实判断点必须停下等待明确选择。[E3]

## 禁止事项

- 不修改、删除、覆盖、重命名或移动两个既有资料目录中的内容；不静默覆盖开发区产物。[E1]
- 不编造页数、论文内容、模型、结果、引用、人工理由或测试通过状态。[E1][E3]
- 不把 OCR 当作原件，不让派生材料覆盖原始证据，不把未审计资料写成已验证事实。[E1]
- 不提前读取 2025 答案型来源，不用隐藏答案“校验方向”，不把保留集信息泄漏回训练规则。[E1]
- 不在当前阶段创建空 `SKILL.md`、占位案例或占位 playbook；不提前生成论文、最终模型、发布包或安装动作。[E1][E5]
- 不把隔离开发区当作最终仓库，不在 P0 回接上游；未来即使获批，也不得只更新三个 Skill 镜像中的一个或跳过发布元数据校验。[E1][E3]
- 不以算法名称为起点堆砌复杂度；先澄清目标、对象、数据、变量、关系、约束和可检查输出，再进入方法筛查。[E2][E3]

## 成功标准

### P0 验收标准

- 仅在 `cumcm-b-skill/` 保留本阶段指定的最小目录和五个 P0 文件：`planning/project_charter.md`、`planning/session_config.json`、`planning/workflow_manifest.json`、`baseline/upstream_file_manifest.json` 与 `baseline/upstream_architecture.md`；其中两个 `baseline/` 文件属于 P0 上游基线产物。
- `session_config.json`、`workflow_manifest.json` 与 `upstream_file_manifest.json` 可解析；只有 P0 为 `complete`，P1—P14 及 P12/P13/P14 子状态均为 `pending`。
- 两个既有资料目录的前后只读树指纹一致。
- 没有空白占位结论，也没有创建 `SKILL.md`、案例或 playbook 文件。[E1][E5]

### 项目最终成功标准

- 在隔离开发区形成可运行、可验证、渐进披露且证据可追溯的候选优化，而不是历年答案索引、一键代写器或与上游割裂的最终产品。[E1][E2][E4][E5]
- 对问题解析、方法风险、代码、结果、稳健性、图表和审查建立清晰门控；机械正确性由 AI 检查，关键建模判断由人工确认。[E3][E4]
- 在不接触 2025 答案型来源的条件下完成并冻结盲测，再进行有隔离的外部对照；任何污染、证据不足或校验失败均如实标记为阻塞或无效。[E1]
- 发布前通过届时规定的结构、引用、脚本、安全、证据与人工门控审计；只有获得用户对发布版本、文件清单和补丁哈希的书面批准，才可把获批改动一致地回接三份 Skill 镜像并校验 manifest、marketplace 与版本信息。本标准不预先宣称这些检查、批准或回接已经完成。[E1][E3][E5]

## evidence_refs

- id: E1
  source_path: `CUMCM_B题专项Skill_分步执行提示词_V2.md`
  locator: `## 唯一最终目标`、`## 使用方法`、`## 执行顺序`、`## P0｜初始化独立开发区`、`## P12A｜启动 2025 B 题封存盲测`、`## P12B｜继续 2025 B 题封存盲测（可重复）`、`## P13A｜盲测冻结后解封外部对照`、`## P13B｜应用获批修订并执行发布审计`、`## P14A｜生成目标仓库精确回接计划与批准卡`、`## P14B｜按版本级书面批准回接目标仓库`
  source_role: derived_artifact
  supports: 唯一最终优化对象、隔离开发区定位、上游回接授权与三镜像一致性要求，以及当前目录权限、阶段边界、统一证据格式、2025 封存与解封条件、人工门控和 P0/P12/P13/P14 验收规则。
- id: E2
  source_path: `CUMCM_B题_Skill资料整理_对话交接记忆.md`
  locator: `## 一、项目背景与目标`、`## 二、B题专项 Skill 的训练材料体系`、`## 十一、Skill 设计核心原则`、`## 十四、当前总体状态`
  source_role: derived_artifact
  supports: 项目目标、候选资料范围、非答案记忆式设计原则，以及多项资料完整性仍待确认；其中把 2025 列为训练资料的旧规划已由 E1 的当前封存规则覆盖。
- id: E3
  source_path: `github下载的skill/AGENTS.md`
  locator: `# Core Philosophy`、`# Configuration`、`# Workflow Discipline`、`# Human Decision Convention`、`# Verification`
  source_role: derived_artifact
  supports: learning/lean 配置、AI 与人工的职责边界、从问题结构出发、证据化决策与按当前门控验证。
- id: E4
  source_path: `github下载的skill/README-zh.md`
  locator: `## 项目初心`、`## 和常见做法的区别`、`## 整条流程`、`## 不做什么`
  source_role: derived_artifact
  supports: Skill 辅助而非自动驾驶、使用者保留关键判断、不编造数据结果引用及不一键生成论文。
- id: E5
  source_path: `<local-path><identifier>/.codex/skills/.system/skill-creator/SKILL.md`
  locator: `# Skill Creator`、`## Anatomy of a Skill`、`### What Not to Include`、`## Create or Update a Skill`
  source_role: derived_artifact
  supports: 保持 Skill 范围最小、避免无用途目录与占位文件、渐进披露、先理解任务再创建正式 Skill。
