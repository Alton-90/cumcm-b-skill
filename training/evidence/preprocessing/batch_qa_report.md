# P5B-01 批次 QA 报告

- 批次：`2018正式B题及正式附件`
- 状态：`COMPLETE`
- 验收：`PASS_WITH_WARNINGS`
- 专项整改：`ACCEPTED / PASS_WITH_WARNINGS`（第三次独立复验结论已由总控接受）
- 完成时间：`2026-09-05T16:42:15+08:00`
- 下一来源组：`2020正式B题及正式附件`
- P5 总体仍为 `in_progress`；P6 未启动。

## 三个 job

| job | 类型 | 执行状态 | QA | 主要结果 |
|---|---|---|---|---|
| `JOB-f041097f2f4b` | RAR 只读清单 | PASS | PASS_WITH_WARNINGS | 4 个成员；两轮清单一致；零成员提取；成员 size/mtime 仍未验证 |
| `JOB-66a71884875b` | Appendix1 DOC | PASS | PASS_WITH_WARNINGS | 38 个正文单元；2 个派生页面；4 个图像占位标记；零失败单元 |
| `JOB-e9562bae3013` | 正式题面 DOC | PASS | PASS_WITH_WARNINGS | 16 段、1 表；1 个派生页面；1 个图像占位标记；零失败单元 |

两份 DOC 均以只读方式打开，原件 SHA-256、大小和 mtime 前后相等；每次仅退出本 job 新建的 Word 实例，任务 PID 均无残留。原有 PID 76044/87700 的归属仍未验证，未对其执行终止。

## 原阻塞解除与历史保留

旧 `Documents.Open` 采用 16 个 `[ref]` 参数并夹带空可选值，在 PowerShell 5.1 中稳定返回 `NullReferenceException`。真实 DOCX 烟测证明 4 参数只读调用可用；正式助手同时固定 5 参数 `SaveAs2`、`AddToRecentFiles=false`、STA/NonInteractive 启动、COM 子对象释放和任务 PID 归属检查。

旧 7 份失败记录全部保留于 `qa/p5/failures/`，旧 PARTIAL 状态保留于 `planning/history/20260905_160129_P5B-01-COM-FIX/`，没有回写历史失败事实。

## 正式—replay 一致性

| job | Markdown | 正文哈希 | 规范化结构 | 结构计数 | 页数 | PNG |
|---|---|---|---|---|---|---|
| Appendix1 | 字节一致：`1eab9d…f3f7` | 一致：`f02f50…0e66` | 一致：`e01f75…dd16` | 一致 | 2/2 | 两页逐字节一致 |
| 正式题面 | 字节一致：`93b0fa…75e2` | 一致：`a79236…dad2` | 一致：`ce9cf7…1729` | 一致 | 1/1 | 一页逐字节一致 |

Word 生成的 DOCX/PDF 容器哈希在正式与 replay 间不同，未宣称字节确定；正文、结构、页数和栅格页面均一致。Appendix1 的 r1 因 2 个顶层 `bookmarkEnd` 被旧解析器误判而不采纳；2.1.1 已将这类无可见内容的范围标记排除，并有合成回归测试。

## 渲染与逐页检查

文档技能的 canonical `render_docx.py` 已尝试，但主机缺少 LibreOffice `soffice.exe`，状态为 `FAILED_UNAVAILABLE_DEPENDENCY`。声明的回退链为 Word `ExportAsFixedFormat` PDF → bundled Poppler 26.07.0 `pdftoppm`（180 DPI）。DOCX 与 PDF 均由 Word 产生，因此独立渲染性有限；该限制保留为警告。

正式 PNG 共 3 页，均逐页检查：无裁切、重叠、乱码、坏表或页眉页脚问题；附件图片、题面示意图和表 1 均清晰。附件第一页末句延续到第二页是正常分页。

- Appendix1 page 1：`9711cb98…d9919e`
- Appendix1 page 2：`4bf74146…94c9b1`
- 题面 page 1：`803fcec6…9e6947`

## 文本核对

- Appendix1：`body_block_0001` 标题、`body_block_0023` RGV 描述、`body_block_0036` 最后一项均与页面匹配。
- 正式题面：`body_block_0001` 标题、`body_block_0009` 故障条件、`body_block_0014` 三组参数表、`body_block_0017` 附件说明均与页面匹配。
- 图像不伪装成正文：Markdown 显式保留 4 个和 1 个 `EMBEDDED_OBJECT_UNREADABLE` 标记，视觉页证明图像仍在派生文档中。

## 测试与范围

- P5A 回归：8/8 PASS；三份 P4 正式文本哈希不变；临时 replay 已清理。
- P5B 安全与合成测试：11/11 PASS。
- 真实 Word COM 集成：1/1 PASS。
- 冻结 `batch_queue.json` 哈希仍为 `0f27f4a1b9d13a5268a566b430c0a30e8da4d0cf097a917deb95e22e90b96b74`。
- 仅执行本组三个 job；未执行第四个或以后 job；2025 holdout 正文零访问；P6 未启动。

## 剩余警告

1. RAR 成员大小与本地化修改时间仍为 `UNVERIFIED`。
2. DOC 图像只以显式占位符进入 Markdown；视觉图像由派生页保留。
3. canonical DOCX 渲染器缺少 LibreOffice，使用已声明的 Word-PDF + Poppler 回退。
4. DOCX/PDF 容器本身非字节确定。

完整机器证据见 `cumcm-b-skill/qa/p5/batches/P5B-01_2018_official_b.json`。

---

# P5B-02 批次 QA 报告

- 批次：`2020正式B题及正式附件`
- 状态：`COMPLETE`
- 验收：`PASS_WITH_WARNINGS`
- 完成时间：`2026-09-05T17:59:10+08:00`
- 下一来源组：`2021正式B题及正式附件`
- P5 总体仍为 `in_progress`；P6 及以后仍为 `pending`。

## 三个组内 job

| job | 类型 | 本轮动作 | QA | 主要结果 |
|---|---|---|---|---|
| `JOB-3aca073ea667` | 正式题面 DOCX | 仅身份核验 | PASS | 原件身份与 P4 正式文本哈希均不变；未重写正式文本 |
| `JOB-18d7b87d2468` | Result.xlsx | replay + formal | PASS_WITH_WARNINGS | 1 表、34×11、334 个 OOXML 单元格元素、76 个带值或公式单元格、0 公式；不求值、不输出值 |
| `JOB-b14a95cf1ddd` | 附件 DOCX | replay + formal | PASS_WITH_WARNINGS | 123 个正文单元、114 段、9 表、2 公式对象、零失败单元；6 页逐页通过 |

`JOB-97c0000064a7`（`format2020.doc`）保持排除状态，未打开正文、未执行。

## XLSX 只读结构适配器

新增的 `spreadsheet_structure_profile` 只接受冻结队列 job，通过 ZIP/OOXML 与禁用外部实体/网络的 XML 解析器读取结构。它没有任意 `input`/`output` 覆盖、没有 `force` 接口、不调用 Excel 或 LibreOffice，也不计算公式、不解释缓存结果、不输出公式文本、共享字符串内容或单元格值。

正式结构哈希为 `72083daa…f615`，Markdown 为 `0e8e849b…9dfc`。独立 `openpyxl 3.1.5` 以 `read_only=True, data_only=False, keep_links=False` 交叉核验得到同一 `Sheet1`、34 行、11 列、76 个非空值单元、0 个公式，原件身份前后相等。

首轮 r1 replay 保留但不采纳：字段 `nonempty_cell_element_count` 实际统计所有序列化 `<c>` 元素，命名会误导。r2 明确拆为 `cell_element_count=334` 与 `value_or_formula_cell_count=76`，并成为正式对账基准；历史 r1 未删除或覆盖。

## DOCX 正式—replay 与视觉核验

DOCX 正式与 replay Markdown 逐字节一致（`82db5402…28f4`），正文哈希、规范化结构哈希、段落/表格/公式/标记计数全部一致；原件 SHA-256、大小和 mtime 在两次执行前后均不变。

Documents skill 的 canonical `render_docx.py` 已真实尝试，但因主机缺少 `soffice.exe` 失败；失败记录保留于 `qa/p5/failures/20260905_174000_P5B-02_DOCX_RENDER_LIBREOFFICE.json`，未安装软件。回退使用单 job 绑定的 Word 只读导出和 bundled Poppler 150 DPI 栅格化：Word 16.0 实际只读、禁用宏和链接更新、未调用原件保存、未终止既有进程，源身份保持不变。

6/6 页均逐页检查通过：无裁切、重叠、乱码、坏表或缺图；9 个表格、6 张地图完整。第 5、6 页各有一个公式对象可见，但 Markdown 仍保守保留总计 2 个 `FORMULA_UNREADABLE` 标记，没有从图像臆写公式语义。

## 正式—replay 一致性

| job | Markdown | 正文/结构哈希 | 结构计数 | 原件身份 |
|---|---|---|---|---|
| Result.xlsx | 字节一致：`0e8e849b…9dfc` | 一致 | 一致 | 两侧均不变 |
| 附件.docx | 字节一致：`82db5402…28f4` | 一致 | 一致 | 两侧均不变 |

run JSON 因 `output_path` 与 `exact_command_argv` 不同而不宣称字节一致。Word PDF 含创建元数据，也不宣称容器字节确定；确定性结论仅覆盖正式 Markdown、正文/结构哈希、结构计数和源身份。

## 测试与范围

- P5A 完整回归：8/8 PASS（419.222 秒）；P4 三份正式文本前后哈希不变，replay 一致，未用 force，临时目录已清理。
- P5B 安全回归第二轮整改后复跑：13/13 PASS（1.213 秒）。新增两项确定性动态测试直接执行生产 `Wait-ForOwnedWordProcessExit`：模拟任务 PID 在最后一次 sleep 内退出时不误报；模拟最终快照仍有任务 PID 时保持超时失败。
- XLSX 专项：6/6 PASS。
- 旧报告曾记录 Word COM 1/1 PASS（9.499 秒），但对应原始日志未持久化，因此不再把该说法作为当前门禁证据。
- 2026-09-06 独立验收真实复跑为 0/1：任务创建的 WINWORD PID 38992 在旧 5 秒等待结束时仍存在，断言失败；该 PID 随后自行退出且最终无残留。原始失败日志未持久化，缺失字段不得重建或推测；边界记录见 `qa/p5/integration/20260906_P5B-02_independent_failure_boundary.json`。
- 第一轮整改把清理改为从 `Quit(0)` 起计时的 30 秒硬门限和 250 ms 轮询，但报告中“最终复检”的声明不准确：实现仍可能在最后一次 sleep 后由 while 条件直接退出，并以 sleep 前旧快照判定超时。
- 整改后真实 Word COM 连续三轮均 1/1 PASS：PID 44608 / 33968 / 50608 的退出延迟分别为 18364.551 / 18342.660 / 18358.418 ms，均在门限内自行退出，三轮最终残留均为空。完整 argv、cwd、时刻、退出码、stdout/stderr、源前后身份和清理字段已分别持久化在 `qa/p5/integration/20260906_P5B-02_word_com_remediation_run1.json` 至 `run3.json`。
- 第二次独立复验仍为 `BLOCKED`，尽管其动态复跑本身 1/1 PASS 且最终 `WINWORD=[]`；阻断原因正是上述最后一次 sleep 后可能使用旧快照。事实边界保存在 `qa/p5/integration/20260906_P5B-02_second_independent_reaudit_boundary.json`。
- 第二轮最小修复在循环结束后、计算 `shutdown_timed_out` 前无条件重新调用 `Get-WordProcessIds`，只与任务自有 PID 求交；最终快照成为唯一判定依据，并记录 `final_recheck_performed`、`final_recheck_at` 和 `final_process_ids_snapshot`。30 秒门限、250 ms 间隔、超时失败和无强杀语义不变。
- 第二轮修复后的新真实 Word COM 运行 1/1 PASS：PID 61836，shutdown latency 18391.998 ms，无条件最终复检为 true，最终快照及任务残留均为空。新日志为 `qa/p5/integration/20260906_P5B-02_word_com_final_recheck_run4.json`，未覆盖前三轮。
- 第三次独立只读复验结论为 `PASS_WITH_WARNINGS`，并已由总控接受：`test_12/test_13` 独立 2/2 PASS、0 skip；独立真实 Word COM 1/1 PASS、0 skip，PID 48940，shutdown latency 18141.427 ms，`final_recheck_performed=true`，最终全量快照、任务残留和结束后 WINWORD 均为空。验收者已删除临时证据，项目目录未新增该临时日志；该边界如实保留，不虚构日志路径。
- 冻结 `batch_queue.json` 哈希仍为 `0f27f4a1b9d13a5268a566b430c0a30e8da4d0cf097a917deb95e22e90b96b74`。
- `extract_source_text.py` 未修改，因此未重跑耗时 P5A OCR；仅核验三份 P4 正式输出仍为 `e58515e1…a94c`、`5c8ef49c…bf01`、`3afbff6d…bd5b`，并引用独立验收此前确认的 P5A 8/8。
- 未修改两个受保护目录；未访问 2025 holdout 正文；未启动 P6；未生成模型、论文或方法总结。

## 剩余警告

1. 附件 Markdown 保留 2 个 `FORMULA_UNREADABLE`，仅视觉证明公式对象存在。
2. canonical DOCX 渲染器缺少 LibreOffice，已保留失败并使用受控 Word-PDF + Poppler 回退。
3. XLSX r1 replay 字段命名不准确，已保留并由 r2 取代。
4. Word PDF 与 run JSON 容器不作字节确定性声明。
5. 独立验收 0/1 的原始失败日志未持久化；本地只保存用户确认的事实边界，不能补造当时 argv、时间、退出码或 stdout/stderr。
6. 前两次独立复验的 `BLOCKED` 历史继续保留；第三次独立复验已按总控决定正式记为 `ACCEPTED / PASS_WITH_WARNINGS`。

完整机器证据见 `cumcm-b-skill/qa/p5/batches/P5B-02_2020_official_b.json`。

## P5B-13 与 P5 完成（2026-09-07）

- 总控接受最终组 `2024优秀论文B159、B195、B196三个PDF`：formal/replay 均 PASS，去且仅去 `generated_at` 后正文 3/3 一致；独立机器与视觉 QA 均为 `PASS_WITH_WARNINGS`，视觉关闭门禁为真，12/12 replay 样图已核验。
- 保留两项警告：R3 replay runtime 与旧 formal runtime 不同但已通过 SHA/version/signature 门禁；B159 第 37 页是原件一致的合法空白尾页。R2、旧 partial replay 与失败链未删除；未声称逐字符 OCR 准确。
- P5 现为 complete；冻结 queue SHA-256 `0f27f4a1b9d13a5268a566b430c0a30e8da4d0cf097a917deb95e22e90b96b74` 未改，holdout 未访问，P6 未启动且 P6–P14 pending。workflow 补入已接受 P5B-06 的 `JOB-b7aa3d474332`，作为历史汇总遗漏修正。
## P5B-03｜2021正式B题及正式附件（2026-09-06）

- 结论：`COMPLETE / PASS_WITH_WARNINGS`；三个冻结 job 全部 PASS，P5 仍 `in_progress`，下一组推进至 2022。
- `JOB-431fffda24b9`：2021 B 题 PDF，2 页 native text，0 OCR，首/末页视觉抽查通过。
- `JOB-a62dfe1f637f`：附件1.xlsx，结构计数 `cell_element_count=1265`、`value_or_formula_cell_count=964`、公式 0。
- `JOB-9f8db3dad8e4`：附件2.xlsx，结构计数 `cell_element_count=80`、`value_or_formula_cell_count=66`、公式 0。
- Formal 与 accepted replay Markdown 哈希三项一致；XLSX 未求值、未解释缓存、未输出单元格值或公式文本；三个原件 SHA-256、大小、mtime 前后不变。
- 快速回归：P5A `8/8 PASS`；P5B adapter `13/13 PASS`；spreadsheet profile `6/6 PASS`。未运行 Word COM（本批无 DOC/DOCX）。
- 保留警告：Poppler 对 Symbol/ArialUnicode 发出字体提示但页面可读；结构计数不等于业务非空计数；此前 P5B-02 两次 BLOCKED 历史及其接受警告均保留。

证据：`cumcm-b-skill/qa/p5/batches/P5B-03_2021_official_b.json` 及其 `evidence_refs`。

## P5B-04｜2022正式B题及正式附件（2026-09-06）

- 结论：`COMPLETE / PASS_WITH_WARNINGS`；唯一允许 job `JOB-e7baa99b7142` PASS，P5 仍 `in_progress`，下一组推进至 2023。
- 2022 B 题 PDF：2 页，2 页均 native text，0 OCR，0 失败页；首/末页视觉核验通过。
- Formal 与 accepted replay Markdown 字节一致：`2b4c6458…1046d0f`；原件 SHA-256 `f2d0db2e…ac8924d`、大小 568238、mtime 前后不变。
- P5A：`NOT_RERUN_REUSED_IMMEDIATE_P5B03_PASS`；复用 P5B-03 刚完成的 8/8 接受结果，本轮未重复运行；本批无 XLSX/DOC/DOCX，未运行 spreadsheet/Word 测试。
- 保留警告：Poppler 发出 Symbol/ArialUnicode 无显示字体提示，但两页可读；未解释题目内容。

证据：`cumcm-b-skill/qa/p5/batches/P5B-04_2022_official_b.json` 及其 `evidence_refs`。

## P5B-05 — 2023正式B题及正式附件（2026-09-06）

- 状态：COMPLETE / PASS_WITH_WARNINGS；JOB-4594f7cebcb8 唯一执行。
- RAR 两轮只读清单：4 个成员，顺序与规范化清单字节一致，SHA-256 `864c3b755040e85248ffe0734dd87d6bc09078b9d278e7524d2b0cc998c1f2d2`。
- extraction_performed=false、成员正文未访问；原 RAR SHA-256、大小 1168748、mtime 前后不变。
- 警告：冻结 title=D题 与路径/verified_code=B 不一致；身份未改写。成员名含 cp936 解码记录。
- P5A 回归与 adapter 证据按要求 NOT_RERUN/复用；本批未做视觉、Spreadsheet、Word 测试。
- 状态文件：`cumcm-b-skill/qa/p5/batches/P5B-05_2023_official_b.json`；下一组：P5B-06（2024）。

## P5B-06 — 2024正式B题及正式附件（2026-09-06）

- 唯一执行 `JOB-b7aa3d474332`（`SRC-fb8d66aeff99` / `DOC-aad89d701ef0`），输入为正式题面 PDF；`format2024.doc` 保持 `EXCLUDED_CONTEST_FORMAT_GUIDE`，未打开、未哈希、未转换、未渲染。
- 正式 PDF 2 页，2 页 native text、0 OCR、0 失败页；formal/replay Markdown 字节一致，SHA-256 均为 `3748355c9a147ecbde2fb1403398b8780e16912a79002c2d25dec61e4895b951`。
- dry-run 先通过；首/末页因总页数为 2 而逐页视觉核验通过。Poppler 的 Symbol/ArialUnicode 字体警告保留为警告。
- 原件 SHA-256 `f54529dd15d729b046e248ea41033b4f66ef68333be2bee912b0c54eafd227ab`、大小 636910、mtime 前后一致。P5A、适配器、Spreadsheet、Word 测试按要求分别记为 NOT_RERUN/NOT_APPLICABLE，未宣称本轮 PASS。
- 状态文件：`cumcm-b-skill/qa/p5/batches/P5B-06_2024_official_b.json`；下一组：P5B-07（2025正式B题及正式附件）；当前等待总控复核。


## P5B-07｜2025正式B题及正式附件（2026-09-06）

- 结论：`COMPLETE / PASS_WITH_WARNINGS`；五个冻结官方 job 均 PASS。
- PDF：2 页 native text、0 OCR、0 失败页；formal/replay Markdown 字节一致，首末页视觉核验通过。
- 四个 XLSX：均为只读 OOXML 结构提取，1 表、A1:B7470、7470 行、14940 个 `<c>`、14940 个 value/formula 单元、0 公式；formal/replay 字节一致，独立 ZIP/XML 复算通过。
- 专项测试：spreadsheet profile 6/6 PASS；P5A 8/8 与 adapter 13/13 复用最近可定位接受证据，未重跑；Word 不适用。
- 边界：format2025 未访问；三项答案型 HOLDOUT_LOCKED 均 content_accessed=false，且无 run/输出；P6 未启动。
- 下一组：`2018经典论文组三个PDF`，等待总控复核。

## P5B-08｜2018经典论文组三个PDF（2026-09-06）

- 状态：`COMPLETE / PASS_WITH_WARNINGS / CONTROLLER_REVIEWED_BATCH_COMPLETE`；仅执行 `JOB-712c63c1521a`、`JOB-6b8554e92a3d`、`JOB-1b1aad6f446e`。
- B203：56 页全 native；B217：45 页全 native；B334：29 页（28 native、1 OCR），三者均零失败页、页边界完整。正式 Markdown 与独立 replay 均字节一致，正文哈希及结构计数一致。
- 视觉抽样：B203 页 1/15/21/28/56；B217 页 1/12/18/23/29/45；B334 页 1/8/10/15/25/29。各首/中/尾以及公式、表格/图形或代码密集页均无实质裁切、重叠或视觉乱码；B334 末页 OCR 可读。
- 原始 PDF 的 SHA-256、大小及 mtime 在正式与重放后复核均不变。B217 的 134 个 U+FFFD 仅位于页 4、5、6、7、11、12、13、14、16、17、20 的公式/矩阵/求和/变量结构，保留为公式机器可读性警告；未猜写或更正任何文本、公式、表格、图或嵌入对象。B334 第 29 页 OCR 与渲染的单行代码“92 print(ans)”相符，无明显幻觉或漏页。
- P5A 8/8 与 adapter 13/13 未重跑：提取器 SHA-256 与 P5B-03 可定位通过证据一致；本批纯 PDF，未运行 Word/XLSX 测试。
- 队列未改，三个 2025 HOLDOUT_LOCKED 来源未访问，P6 未启动。总控轻量机器核验与独立局部质量复核已接受本批。唯一下一组：`2020参考经典论文组B078、B108两个PDF`；`B007` 属于后续 2021优秀论文组，不纳入 P5B-09。

证据：`cumcm-b-skill/qa/p5/batches/P5B-08_2018_classic_papers.json` 及其 `evidence_refs`。

## P5B-09｜2020参考经典论文组B078、B108两个PDF（2026-09-06）

- 状态：`COMPLETE / PASS_WITH_WARNINGS / CONTROLLER_REVIEWED_BATCH_COMPLETE`；总控已接受，仅执行 B078 与 B108 两个冻结 job，P5 仍 `in_progress`，P6–P14 未启动。
- B078：50 页全 OCR；B108：100 页全 OCR；两者均 0 失败页、0 U+FFFD、页边界完整。formal/replay Markdown、正文哈希及结构计数均一致，输入 SHA-256、大小、mtime 前后不变。
- B078 页 1/10/25/47/48/50 与 B108 页 1/25/50/79/83/100 的视觉抽样未见实质裁切、重叠或视觉乱码。B078 第 48 页和 B108 第 83 页各保留一个 `[UNREADABLE]`：页面为可读的代码图像，但 OCR 未得可靠文本；没有猜写或重建。
- 提取器未变，P5A 8/8 与 adapter 13/13 均复用 P5B-03 的可定位证据、未重跑；本批纯 PDF，未运行 Word/XLSX 测试。队列、pdf_manifest、P3 PDF 未改；holdout 未访问。
- 下一组仅导航为 `2021优秀论文组B007、B026、B050、B160四个PDF`，不在本批处理。

证据：`cumcm-b-skill/qa/p5/batches/P5B-09_2020_classic_papers.json` 及其四项 `evidence_refs`。

## P5B-10 2021优秀论文组

状态：`BATCH_COMPLETE_AWAITING_CONTROLLER_REVIEW`。四个 job 均为 2.4.0 formal + isolated replay PASS；P5 仍 in_progress，P6–P14 pending。总控已对15张真实OCR输入PNG逐张目检 PASS；未声称总控接受批次。

## P5B-10 acceptance

总控独立只读复核后接受：`COMPLETE / PASS_WITH_WARNINGS`。P5仍 in_progress，P6未启动；下一组仅为P5B-11（2022优秀论文B030/B035/B086）。

## P5B-11｜2022优秀论文组B030、B035、B086（待整批总控审阅）

- 状态：`BATCH_COMPLETE_AWAITING_CONTROLLER_REVIEW / PASS_WITH_WARNINGS`；不得解读为整批已接受。P5 仍 `in_progress`，P6–P14 pending。
- B030（42 页）、B035（41 页）、B086（32 页）的 2.4.0 formal 与隔离 replay 均 PASS：全页 OCR，0 failed，`unreadable_marker_total=0`，页数、边界、identity、source/input SHA、geometry/adaptive/counters 一致。源 PDF、formal/replay JSON 与 Markdown 输出的记录 SHA 均已独立实算核对。
- formal/replay Markdown 仅删除 front matter 的 `generated_at` 行后，3/3 body 完全一致；整文件 SHA 不同仅因生成时间不同。
- 9 张既有 final OCR-input PNG（B030 1/21/42，B035 1/21/41，B086 1/16/32）均已核对路径、记录/实算 SHA、dimensions 与 provenance。独立机器 QA PASS；总控视觉门禁 PASS：方向和页边界正确，无裁切、重叠、黑块、错误空白或渲染乱码，正文、公式、图表、流程图与代码页可辨。B035 p41、B086 p32 的大面积页尾空白是带页码的末页代码尾部。未声明逐字符 OCR 准确率。
- 提取器 SHA 未变；P5B-10 的 independent adaptive 12/12、adapter 13/13、P5A final_v2 8/8 仅复用，均为 `NOT_RERUN`。冻结队列未改，三个 holdout 保持 `content_accessed=false`。
- 下一组由冻结队列推导为 `2023优秀论文B226、B311、B477三个PDF`，本次未启动。

证据：`cumcm-b-skill/qa/p5/batches/P5B-11_2022_outstanding_papers.json` 与 `cumcm-b-skill/qa/p5/visual/P5B-11_visual_qa.json`。

## P5B-11｜总控整批接受

- 状态：`COMPLETE / PASS_WITH_WARNINGS / CONTROLLER_REVIEWED_BATCH_COMPLETE`。总控已基于三 job 全部 formal/replay 机器证据与 9 页实际视觉检查正式接受本批。
- B030 为 42/42、B035 为 41/41、B086 为 32/32；三者身份、source/input/output 哈希、计数、geometry 一致，0 failed、0 unreadable、adaptive=0，normalized body 3/3 一致。9/9 final OCR-input PNG 的记录/实算哈希、dimensions 与 provenance 均一致，视觉检查 PASS。
- 保留警告：整文件 SHA 因 `generated_at` 不同；无逐字符真值；B035 p41 与 B086 p32 的留白为合法末页代码尾部。
- P5 仍 `in_progress`；唯一下一组是 P5B-12（`2023优秀论文B226、B311、B477三个PDF`），未启动。P6 未启动，冻结队列与三个 holdout 边界保持不变。

## P5B-12｜总控整批接受

- 状态：`COMPLETE / PASS_WITH_WARNINGS / CONTROLLER_REVIEWED_BATCH_COMPLETE`。总控依据独立机器审计 `hard_gate_passed=true` 与独立视觉审计 10/10 正式接受 B226、B311、B477；P5 仍 `in_progress`。
- formal/replay 均执行 3 个冻结 job、exit 0：B226 51/51、B311 34/34、B477 50/50；所有页面均 0 failed、0 empty、0 unreadable。仅删除 `generated_at` 行后，3/3 Markdown 正文一致。
- 10 个 replay 样本的哈希、尺寸和 provenance 全部一致，视觉通过。B311 仅页 14 重试：220 DPI 空文本后选择 400 DPI attempt 2；最终字段等于 attempt 2，adaptive 计数为 0/0。
- 保留警告：无逐字符真值；B311 p14 密集图内标签 OCR 有噪声，PNG 为视觉权威；formal `qa_sample_count=0` 属预期设计。早期 R1/V1/V2 失败历史保留。
- 冻结 queue、原件、三个 holdout 和 P6 边界均不变。唯一下一组为 P5B-13：`2024优秀论文B159、B195、B196三个PDF`；本次未启动。

证据：`cumcm-b-skill/qa/p5/batches/P5B-12_2023_outstanding_papers.json`、`cumcm-b-skill/qa/p5/independent/P5B-12_machine_audit.json`、`cumcm-b-skill/qa/p5/visual/P5B-12_visual_qa.json`。
