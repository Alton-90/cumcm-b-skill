# 上游仓库架构基线

- 阶段：P0-R
- 上游根目录：`github下载的skill/`
- 记录性质：只读事实映射，不包含质量评价、改进建议或候选补丁。[A1]

## 范围与读取方法

递归清单记录到 116 个目录和 145 个文件；145 个文件中有 128 个 Markdown 与 17 个非 Markdown。128 个 Markdown 按 SHA-256 合并为 57 份唯一正文，唯一正文均完整读取；其余 71 个 Markdown 路径通过同哈希代表正文覆盖。17 个非 Markdown 只记录路径、扩展名、大小、修改时间和 SHA-256，未把其正文作为指令解释或执行。[A1]

本基线的上游树指纹为 `613c2b5c21ca3007c3dd2b31ee0a1b49154b3925da3fd3990660fc3093a562c1`，算法是 `sha256(sorted D|relative_dir and F|relative_path|length|file_sha256)`。[A1]

## 入口文档

| 路径 | 基线角色 | 可定位依据 |
|---|---|---|
| `AGENTS.md` | Codex 侧的工作流政策入口，规定核心理念、配置、阶段门控、Skill 加载与验证纪律。 | [A2] |
| `CLAUDE.md` | README 指向的 Claude 侧项目规则入口；其存在、路径、哈希和仓库角色由文件清单记录。 | [A3] |
| `README.md`、`README-zh.md` | 仓库定位、28 个 Skill、流程阶段、安装、原生插件布局和维护入口。 | [A3] |
| `Initial Prompt.md`、`Initial Prompt-zh.md` | 新会话开场入口；要求先读项目规则与相关 `SKILL.md`，把仓库作为分阶段工作流，并首先调用 `workflow-orchestrator`。 | [A4] |
| 各 Skill 的 `SKILL.md` | 对应 Skill 的触发、前提、流程、输出、验证与停止条件；例如 `workflow-orchestrator` 负责检查工作区和路由下一步。 | [A5] |

## 多副本与分发架构

仓库包含三套按相对路径对应的 Skill 文件树：

1. `.claude/skills/`：Claude 独立开发副本；
2. `.codex/skills/`：Codex 独立开发副本；
3. `plugins/mathmodeling-skills/skills/`：原生插件分发副本。[A3][A6]

清单比较了三棵树中的全部 35 个相对文件：35 个在三处均存在且 SHA-256 完全相同，缺失或不一致项为 0。因此，本次 P0-R 基线下三棵 Skill 文件树是逐文件同哈希镜像；该陈述只适用于清单记录的当前指纹，不外推到未来版本。[A6]

根目录 `AGENTS.md` 与 `plugins/mathmodeling-skills/AGENTS.md` 也属于同一 SHA-256 重复组；根目录 `LICENSE` 与插件包内 `LICENSE` 同理。具体路径、哈希与重复组均保存在清单中。[A7]

## Skill 名称

清单从 `.codex/skills/<name>/SKILL.md` 的稳定路径机械提取出 28 个名称；README 的 “28 个 skill” 分阶段清单提供了正文层面的交叉依据。[A3][A8]

`code-reviewer`、`completeness-auditor`、`consistency-auditor`、`data-auditor-cleaner`、`decision-prompt-builder`、`figure-table-planner`、`final-method-explainer`、`math-figure-generator`、`matlab-code-reviewer`、`matlab-model-code-generator`、`method-selector`、`model-assumptions-builder`、`model-code-analyzer`、`modeler-decision-logger`、`paper-polisher`、`paper-section-writer`、`problem-classifier`、`problem-parser`、`python-code-reviewer`、`python-model-code-generator`、`quality-assurance-auditor`、`reference-manager`、`related-paper-analyzer`、`result-report-generator`、`robustness-checker`、`solution-package-builder`、`symbol-table-builder`、`workflow-orchestrator`。[A8]

## 插件、manifest 与同步入口

README 记录的原生插件分发面与清单中的实际路径一致：[A3][A9]

- Claude marketplace：`.claude-plugin/marketplace.json`；
- Codex marketplace：`.agents/plugins/marketplace.json`；
- 共享安装包：`plugins/mathmodeling-skills/`；
- Claude 插件 manifest：`plugins/mathmodeling-skills/.claude-plugin/plugin.json`；
- Codex 插件 manifest：`plugins/mathmodeling-skills/.codex-plugin/plugin.json`；
- 安装入口：`install.sh`；
- Skill 镜像同步入口：`scripts/sync-plugin.sh`。

README 明确说明维护者在更新两套独立 Skill 副本后运行 `./scripts/sync-plugin.sh`，并以 `./scripts/sync-plugin.sh --check` 检测分发包是否陈旧；本轮只记录该公开契约，没有读取或执行脚本正文。[A3][A9]

插件包还包含 `plugins/mathmodeling-skills/hooks/hooks.json`。由于它是非 Markdown，本轮只确认其路径、大小、修改时间与 SHA-256，不对 hook 行为作解释。[A9]

## 工作流入口关系

中英文 Initial Prompt 都把 `workflow-orchestrator` 放在标准流程开头和末尾，并要求新题先由它确认阶段；对应 `SKILL.md` 将其定位为检查数学建模工作区、评估门控并路由下一动作的编排器。[A4][A5]

AGENTS 进一步规定：先识别阶段与输入，再按需读取相关 Skill；每个 Skill 只完成自己的阶段，不得自行把整个流程推进到底；AI 负责机械正确性，使用者负责建模判断。[A2]

## P0-R 边界

本文件只回答“目标仓库现在由哪些入口、Skill 镜像、插件分发目录、同步入口和 manifest 构成”。它不评价这些设计是否适合 B 题，不提出改动，也不启动 P1；任何后续差距分析或候选优化须由后续阶段另行取得证据和授权。[A1][A2]

## evidence_refs

- id: A1
  source_path: `cumcm-b-skill/baseline/upstream_file_manifest.json`
  locator: `$.source_policy; $.source_tree_fingerprint; $.summary; $.entries`
  source_role: derived_artifact
  supports: 本轮只读范围、目录与文件计数、Markdown 读取覆盖、非 Markdown 的元数据边界及上游树指纹。
- id: A2
  source_path: `github下载的skill/AGENTS.md`
  locator: `# Core Philosophy`、`# Configuration`、`# Workflow Discipline`、`# Skill Loading Rules`、`# Verification`
  source_role: derived_artifact
  supports: AGENTS 的入口作用、AI/人工职责边界、阶段门控、按需加载 Skill 与验证纪律。
- id: A3
  source_path: `github下载的skill/README-zh.md`
  locator: `## 整条流程`、`## 28 个 skill，按所在阶段划分`、`## 安装` 下的 `### 原生插件结构`、`### 开场指令`、`## 相关文档`
  source_role: derived_artifact
  supports: 仓库定位、28 个 Skill、入口文档、三份 Skill 树、插件布局、manifest 位置和同步脚本公开契约。
- id: A4
  source_path: `github下载的skill/Initial Prompt-zh.md`
  locator: 标题 `# Initial Prompt` 下“在开始建模、写代码或写论文之前”段、标准流程代码块及“第一个任务”
  source_role: derived_artifact
  supports: 新会话先读规则与相关 SKILL、分阶段工作流顺序以及 workflow-orchestrator 的首个任务位置。
- id: A5
  source_path: `github下载的skill/.codex/skills/workflow-orchestrator/SKILL.md`
  locator: YAML `name`/`description`、`# Purpose`、`# Workflow`、`# Handoff`
  source_role: derived_artifact
  supports: workflow-orchestrator 的名称、编排职责和工作流路由角色。
- id: A6
  source_path: `cumcm-b-skill/baseline/upstream_file_manifest.json`
  locator: `$.mirror_comparison`
  source_role: derived_artifact
  supports: 三套 Skill 树的路径、35 个相对文件逐文件同哈希及零缺失/零不一致。
- id: A7
  source_path: `cumcm-b-skill/baseline/upstream_file_manifest.json`
  locator: `$.duplicate_groups[35]`（`id=DG036`）与 `$.duplicate_groups[36]`（`id=DG037`）
  source_role: derived_artifact
  supports: 根政策文件与插件内政策文件、根许可证与插件许可证的重复关系。
- id: A8
  source_path: `cumcm-b-skill/baseline/upstream_file_manifest.json`
  locator: `$.skill_inventory`
  source_role: derived_artifact
  supports: 从稳定 Skill 路径提取的 28 个 Skill 名称和数量。
- id: A9
  source_path: `cumcm-b-skill/baseline/upstream_file_manifest.json`
  locator: `$.entries[?(@.repository_role contains "manifest" || @.repository_role contains "installer" || @.repository_role contains "sync_script")]`
  source_role: derived_artifact
  supports: marketplace、插件 manifest、hook manifest、安装脚本和同步脚本的实际路径、元数据与 SHA-256。
