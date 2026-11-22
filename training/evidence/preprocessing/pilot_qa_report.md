# P4 文本提取流水线试点 QA 报告

## 结论与范围

P4 三个白名单来源均已完成提取、定位、指标计算、首中末与风险页视觉核对，以及两次完整一致性复跑。总体结论为 PASS_WITH_WARNINGS：普通正文在机械消除中文字符间 OCR 空格后可连续阅读，未发现会阻止后续阅读的系统性乱码或整体倒序；局部错字、栏序干扰、公式、表格、图示与代码损失仍存在，且均保留原 OCR 结果并用显式标记声明。本阶段没有建立逐字真值，以下指标不代表文字准确率。

evidence_refs:
- source_path: cumcm-b-skill/derived/text/text_manifest.json
  locator: $.status; $.metric_definitions; $.reproducibility; $.sources
  source_role: derived_artifact
  supports: 支持三个试点完成、指标口径和两次输出哈希一致。
- source_path: cumcm-b-skill/qa/p4/p4_pilot_qa.json
  locator: $.qa_verdict; $.ordinary_body_readability; $.visual_checks
  source_role: agent_inference
  supports: 支持普通正文可读性、局部警告与视觉核对结论。

## 前置门禁

- P3.status=complete，P3.verdict=PASSED；P4、P5 在启动时均为 pending。
- 当前有效派生 PDF 为 22 份、1,058 页；23 份物理 PDF 中有 1 份已废止留档。
- 三个试点来源均为 NOT_HOLDOUT。
- 三个 2025 答案型来源仍为 HOLDOUT_LOCKED 且 content_accessed=false。
- 两份试点 PDF 均为 CURRENT；未使用已标记 SUPERSEDED_NONBODY_CONTAMINATION 的留档 PDF。

evidence_refs:
- source_path: cumcm-b-skill/planning/workflow_manifest.json
  locator: $.phases.P3; $.phases.P4; $.phases.P5
  source_role: derived_artifact
  supports: 支持阶段状态和有效 PDF 数量、页数。
- source_path: cumcm-b-skill/planning/corpus_manifest.json
  locator: 三个试点 source_id 的 holdout_status；$.holdout_summary
  source_role: derived_artifact
  supports: 支持试点非留出集及 2025 锁定来源未访问。
- source_path: cumcm-b-skill/derived/pdf/pdf_manifest.json
  locator: $.current_output_count; $.current_total_pdf_pages; $.physical_pdf_file_count; $.superseded_output_count；两个试点 derivative_status=CURRENT
  source_role: derived_artifact
  supports: 支持当前/废止 PDF 状态与试点输入选择。

## 工具链

| 类别 | 已验证工具 |
|---|---|
| Python | 3.12.14；python-docx 1.2.0；lxml 6.1.1；pypdf 6.10.0；pdfplumber 0.11.9；Pillow 12.3.0 |
| Poppler | pdfinfo 26.07.0；pdftoppm 26.07.0；pdftotext 25.02.0 |
| DOCX 结构读取 | Python zipfile + lxml 6.1.1，按 word/document.xml 的 w:body 直属子节点顺序 |
| 离线 OCR | Windows.Media.Ocr；Windows PowerShell 5.1.26100.6899；zh-Hans-CN 已安装 |
| DOCX 只读渲染 | Microsoft Word for Microsoft 365 16.0.20326.20112；只读打开后导出 2 页 QA PDF |

未安装或未发现 Tesseract、pytesseract、EasyOCR、PaddleOCR、LibreOffice；未联网、未下载模型或语言包、未安装软件。

evidence_refs:
- source_path: cumcm-b-skill/derived/text/text_manifest.json
  locator: $.toolchain
  source_role: derived_artifact
  supports: 支持工具、版本、语言包、调用方式和未安装项记录。
- source_path: cumcm-b-skill/scripts/windows_ocr.ps1
  locator: SHA-256 e160aa2c1767c7ad486317961cb98f5459d72e9c701c4d1f7fec7fcf68faab5d
  source_role: derived_artifact
  supports: 支持 Windows.Media.Ocr 的可脚本化离线调用。

## 指标口径与结果

覆盖率为成功处理单元数除以预期 PDF 页数或 DOCX 可访问正文块数；空单元率为提取正文为空的单元数除以预期单元数；U+FFFD 比率为替换字符数除以生成 Markdown 字符数。非法控制字符不含 TAB、CR、LF。不可读标记数是显式损失声明数量，不是错误率或准确率。

| source_id | 结构/页覆盖率 | 空单元率 | U+FFFD 比率 | 非法控制字符 | OCR 页 | 失败页/单元 | 不可读标记 |
|---|---:|---:|---:|---:|---:|---:|---:|
| SRC-70ad205f7ef3 | 24/24 = 100% | 3/24 = 12.5% | 0/3101 = 0% | 0 | 0 | 0 | 13 |
| SRC-c205cb3c4bfc | 34/34 = 100% | 0/34 = 0% | 0/26919 = 0% | 0 | 34 | 0 | 43 |
| SRC-c1a180d84907 | 18/18 = 100% | 0/18 = 0% | 0/8341 = 0% | 0 | 18 | 0 | 12 |

DOCX 的 3 个空单元是原始 w:body 顺序中的空段落，仍保留结构标记，不计为读取失败。DOCX 中 13 个 Equation.DSMT4 OLE 公式对象在实际内联位置标为 [FORMULA_UNREADABLE]。

evidence_refs:
- source_path: cumcm-b-skill/derived/text/text_manifest.json
  locator: $.metric_definitions; $.sources[*] 的覆盖率、空单元率、替换字符率、非法控制字符数和不可读标记数
  source_role: derived_artifact
  supports: 支持指标定义和三源计算结果。
- source_path: cumcm-b-skill/qa/p4/run_SRC-70ad205f7ef3.json
  locator: $.native_unit_count; $.empty_unit_count; $.formula_object_count; $.failed_units
  source_role: derived_artifact
  supports: 支持 DOCX 空段落、公式对象和失败单元说明。

## 视觉 QA

### 正式题面 DOCX

| 核对项 | 原始定位 | 派生定位 | 观察 | 结果 |
|---|---|---|---|---|
| 首正文单元 | word/document.xml 首个正文块；qa_render_page 1 | body_block_0001 | 标题文字和正文顺序一致 | PASS |
| 中正文单元 | body_block_0012；qa_render_page 1 | body_block_0012 | 普通文字顺序一致；内联倍数公式为 MathType OLE，已在原位置标记 | WARN |
| 末正文单元 | word/document.xml 末个正文块；qa_render_page 2 | body_block_0024 | 注 2 普通正文顺序一致 | PASS |
| 标题、正文、表格顺序 | qa_render_page 1-2 | 24 个结构标记 | 标题和正文顺序可核对；原 DOCX 的 w:tbl 数为 0，无表格顺序可核对 | PASS |

evidence_refs:
- source_path: CUMCM_B题skill训练宝/赛题/2020/B/2020B-穿越沙漠.docx
  locator: word/document.xml w:body；qa_render_page 1-2
  source_role: official_problem
  supports: 支持标题、正文和公式对象的原始视觉与结构位置。
- source_path: cumcm-b-skill/derived/text/SRC-70ad205f7ef3.md
  locator: body_block_0001；body_block_0012；body_block_0024
  source_role: derived_artifact
  supports: 支持首中末结构单元的派生定位和公式损失标记。

### 展示论文 PDF

| PDF 页 | 原始定位 | 派生定位 | 观察 | 结果 |
|---:|---|---|---|---|
| 1 | source_page 0；B125_00.jpg | pdf_page 1 | 普通段落行序可读；存在局部 OCR 替换和标题插入顺序偏差，未人工修正 | WARN |
| 17 | source_page 16；B125_16.jpg | pdf_page 17 | 普通正文可读；表格列序与路线图文本丢失，已显式标记 | WARN |
| 28 | source_page 27；B125_27.jpg | pdf_page 28 | 风险页表格被展平，列关系无法可靠恢复，已显式标记 | WARN |
| 34 | source_page 33；B125_33.jpg | pdf_page 34 | 末页代码的操作符、缩进和标识符不可靠，已标 [UNREADABLE] | WARN |

全页接触表还用于识别其他公式、表格、图示和代码风险页；对应页级标记保存在运行记录的 $.parameters.risk_markers，没有用视觉内容替换 OCR 文本。

evidence_refs:
- source_path: cumcm-b-skill/derived/pdf/pdf_manifest.json
  locator: SRC-c205cb3c4bfc 的 page_mapping
  source_role: derived_artifact
  supports: 支持 PDF 页、原始图片编号和文件名映射。
- source_path: cumcm-b-skill/derived/text/SRC-c205cb3c4bfc.md
  locator: pdf_page 1、17、28、34
  source_role: derived_artifact
  supports: 支持抽查页的派生文本、定位和显式损失标记。
- source_path: cumcm-b-skill/qa/p4/samples/SRC-c205cb3c4bfc_contact_sheet.png
  locator: pdf_page 1-34 thumbnails
  source_role: derived_artifact
  supports: 支持全页版面风险筛查，不作为文本提取器。

### 专家评议 PDF

| PDF 页 | 原始定位 | 派生定位 | 观察 | 结果 |
|---:|---|---|---|---|
| 1 | source_page 2；page_002.jpg | pdf_page 1 | 左右混合版面导致局部栏序和英文 OCR 错误，图示部分已显式标记 | WARN |
| 9 | source_page 10；page_010.jpg | pdf_page 9 | 普通要点可读；状态转移公式符号损失，已标 [FORMULA_UNREADABLE] | WARN |
| 16 | source_page 17；page_017.jpg | pdf_page 16 | 普通要点可读；路线图关系无法文本化，已标 [FIGURE_UNREADABLE] | WARN |
| 18 | source_page 19；page_019.jpg | pdf_page 18 | 末页可见文字被提取，无空页或乱码 | PASS |

evidence_refs:
- source_path: cumcm-b-skill/derived/pdf/pdf_manifest.json
  locator: SRC-c1a180d84907 的 page_mapping
  source_role: derived_artifact
  supports: 支持 PDF 页、原始图片编号和文件名映射。
- source_path: cumcm-b-skill/derived/text/SRC-c1a180d84907.md
  locator: pdf_page 1、9、16、18
  source_role: derived_artifact
  supports: 支持抽查页的派生文本、定位和显式损失标记。
- source_path: cumcm-b-skill/qa/p4/samples/SRC-c1a180d84907_contact_sheet.png
  locator: pdf_page 1-18 thumbnails
  source_role: derived_artifact
  supports: 支持全页版面风险筛查，不作为文本提取器。

## 边界与状态

本阶段只读取了三个白名单正文输入和六个前置门禁文件；未读取题面同目录的 Result.xlsx、附件.docx，未读取 2025 优秀论文或专家评议正文，未使用任何 SUPERSEDED PDF。所有写入均位于 cumcm-b-skill，系统临时目录仅用于逐页渲染且已清理。github下载的skill 未写入；P5 未启动。

evidence_refs:
- source_path: cumcm-b-skill/qa/p4/p4_pilot_qa.json
  locator: $.scope_compliance; $.acceptance
  source_role: agent_inference
  supports: 支持白名单、留出集、写入范围、临时文件和 P5 边界声明。
- source_path: cumcm-b-skill/planning/corpus_manifest.json
  locator: $.holdout_summary.locked_sources[*].content_accessed=false
  source_role: derived_artifact
  supports: 支持阶段启动前 2025 锁定来源未访问；本阶段执行记录没有这些路径。

## 下一步

等待人工验收P4后再决定是否启动P5
