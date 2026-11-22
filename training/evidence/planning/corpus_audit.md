# P1 资料标题级盘点与完整性审计

- 生成时间：`2026-09-04T19:18:31.116462+08:00`
- 范围：仅 `CUMCM_B题skill训练宝/` 的目录名、文件名和允许的机械元数据。
- 内容访问：0 个正文文件；22 个 PDF 仅读取结构页数；未提取文本、未渲染页面、未读取 TXT/CSV/URL/DOC/DOCX/XLS/XLSX/图片/视频/压缩包正文。
- 结论边界：文件名与目录名只支持身份、年份、类别和文件序列判断；不支持论文内容、模型、结果或引用。

## 审计结论

P1 验收通过。递归盘点 86 个子目录、1504 个文件，并为 68 个直接承载文件的实际来源文件夹分配了稳定唯一 `source_id`。所有无法从允许元数据确认的页数、类别或完整性均保留为 `UNVERIFIED`。3 个 2025 答案型来源全部为 `HOLDOUT_LOCKED` 且 `content_accessed=false`；未发现封存正文访问或角色与正式题面/附件不可区分的污染。

## 分类汇总

| 类别 | 来源文件夹数 |
|---|---:|
| 专家评议 | 8 |
| 优秀论文 | 15 |
| 参考经典论文 | 6 |
| 官方附件 | 11 |
| 无法确认类别 | 1 |
| 赛题 | 27 |

## 特别复核

- `参考经典论文/2020/B125`：从每个图片文件名的最后一个数值标记解析并按数值排序，观察到 `0–33` 共 34 张，无重复、无区间内缺页、无无法解析文件。外部声明总页数未取得，因此只能判定“观察序列连续”，不能宣称来源整体完整。
- `专家评议/2019/同心协力策略分析`：观察范围 `1–75` 共 74 张，缺少数值页 `71`；`72` 为 JPEG、`73/75` 为 PNG，其余主要为 JPG，构成扩展名混杂。
- 2021—2025 优秀论文：15 个论文目录均已逐目录复核数值序列；2021 的 4 个目录未见 `官方来源.txt`，仅能确认图片序列，来源侧车完整性为 `UNVERIFIED`。
- 2025 优秀论文 `B060`、`B157` 与 2025 专家评议 `碳化硅外延层厚度` 均为 `HOLDOUT_LOCKED`、`content_accessed=false`。
- 根目录 `专家评议下载任务.csv` 与 `专家评议/下载汇总.csv` 可能包含 2025 专家资料下载元数据，已标为 `HOLDOUT_QUARANTINE` 且未打开；其位置和文件名足以将其与 `赛题/2025/...` 的正式题面/附件路径区分，因此不构成 P1 阻塞。

## 完整性与异常

- 零字节文件：0。
- 异常小文件（机械阈值 `<1024` 字节）：34；只标记复核，不据此判坏。
- 重复文件名：97 组，涉及 489 个文件；仅凭同名不判定内容重复，本阶段未对语料文件做字节哈希。
- 扩展名混杂的来源文件夹：41。混杂常由图片与来源侧车文件共存造成，逐项记录但不自动判为错误。
- DOC/DOCX 页数、压缩包内部清单以及无可信声明的总页数均为 `UNVERIFIED`。
- `赛题/2019` 目录未观察到；现有材料未声明其必须存在，因此只记录覆盖缺口，不把它写成已证实的资料缺失。

## 2021—2025 优秀论文目录

| 年份 | paper_code | observed_pages | 缺页/重复/无法解析 | holdout | content_accessed |
|---:|---|---|---|---|---|
| 2021 | B007 | 1–45 (45 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2021 | B026 | 1–26 (26 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2021 | B050 | 1–59 (59 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2021 | B160 | 1–28 (28 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2022 | B030 | 1–42 (42 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2022 | B035 | 1–41 (41 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2022 | B086 | 1–32 (32 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2023 | B226 | 1–51 (51 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2023 | B311 | 1–34 (34 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2023 | B477 | 1–50 (50 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2024 | B159 | 1–37 (37 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2024 | B195 | 1–70 (70 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2024 | B196 | 1–28 (28 images) | missing=[]; duplicates=0; unparsed=[] | NOT_HOLDOUT | false |
| 2025 | B060 | 1–72 (72 images) | missing=[]; duplicates=0; unparsed=[] | HOLDOUT_LOCKED | false |
| 2025 | B157 | 1–67 (67 images) | missing=[]; duplicates=0; unparsed=[] | HOLDOUT_LOCKED | false |

## 来源清单

完整逐文件元数据见 `corpus_manifest.json` 的 `$.sources[*].files`。下表不承载正文结论。

| source_id | category | year | problem_code | paper_code | title | path | format | observed_pages | completeness | holdout | issues |
|---|---|---:|---|---|---|---|---|---|---|---|---:|
| SRC-cdb4ee2aea69 | 无法确认类别 | UNVERIFIED | UNVERIFIED | UNVERIFIED | 资料库根目录散置文件 | `CUMCM_B题skill训练宝` | .csv | UNVERIFIED | UNVERIFIED | HOLDOUT_QUARANTINE | 4 |
| SRC-1b4deafeca43 | 专家评议 | UNVERIFIED | UNVERIFIED | UNVERIFIED | 专家评议 | `CUMCM_B题skill训练宝/专家评议` | .csv | UNVERIFIED | UNVERIFIED | HOLDOUT_QUARANTINE | 3 |
| SRC-c2223b8c2dd7 | 专家评议 | 2018 | UNVERIFIED | UNVERIFIED | 智能RGV动态调度策略 | `CUMCM_B题skill训练宝/专家评议/2018/智能RGV动态调度策略` | .jpg, .txt, .url | 0–40 (41 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-b4fce6295e11 | 专家评议 | 2019 | UNVERIFIED | UNVERIFIED | 同心协力策略分析 | `CUMCM_B题skill训练宝/专家评议/2019/同心协力策略分析` | .jpeg, .jpg, .png, .txt, .url | 1–75 (74 images) | OBSERVED_SEQUENCE_HAS_GAPS | NOT_HOLDOUT | 4 |
| SRC-c1a180d84907 | 专家评议 | 2020 | UNVERIFIED | UNVERIFIED | 穿越沙漠 | `CUMCM_B题skill训练宝/专家评议/2020/穿越沙漠` | .jpg, .txt, .url | 2–19 (18 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-a141969616ab | 专家评议 | 2022 | UNVERIFIED | UNVERIFIED | 无人机纯方位无源定位 | `CUMCM_B题skill训练宝/专家评议/2022/无人机纯方位无源定位` | .jpg, .txt, .url | 1–52 (52 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-ae17dc2a53df | 专家评议 | 2023 | UNVERIFIED | UNVERIFIED | 多波束测线 | `CUMCM_B题skill训练宝/专家评议/2023/多波束测线` | .jpg, .txt, .url | 1–78 (78 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-34b786442a51 | 专家评议 | 2024 | UNVERIFIED | UNVERIFIED | 生产过程中的决策问题 | `CUMCM_B题skill训练宝/专家评议/2024/生产过程中的决策问题` | .jpg, .txt, .url | 1–72 (72 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-11fb6d74f691 | 专家评议 | 2025 | UNVERIFIED | UNVERIFIED | 碳化硅外延层厚度 | `CUMCM_B题skill训练宝/专家评议/2025/碳化硅外延层厚度` | .jpg, .txt, .url | 1–90 (90 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | HOLDOUT_LOCKED | 4 |
| SRC-e5cd698ad88f | 优秀论文 | 2021 | B | B007 | B007 | `CUMCM_B题skill训练宝/优秀论文/2021/B007` | .jpg | 1–45 (45 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-8f01c87998ac | 优秀论文 | 2021 | B | B026 | B026 | `CUMCM_B题skill训练宝/优秀论文/2021/B026` | .jpg | 1–26 (26 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-50e9cdc8922a | 优秀论文 | 2021 | B | B050 | B050 | `CUMCM_B题skill训练宝/优秀论文/2021/B050` | .jpg | 1–59 (59 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-f9723b6fec3b | 优秀论文 | 2021 | B | B160 | B160 | `CUMCM_B题skill训练宝/优秀论文/2021/B160` | .jpg | 1–28 (28 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-f7da546613ae | 优秀论文 | 2022 | B | B030 | B030 | `CUMCM_B题skill训练宝/优秀论文/2022/B030` | .jpg, .txt | 1–42 (42 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-ff5379123217 | 优秀论文 | 2022 | B | B035 | B035 | `CUMCM_B题skill训练宝/优秀论文/2022/B035` | .jpg, .txt | 1–41 (41 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-4b50124526fd | 优秀论文 | 2022 | B | B086 | B086 | `CUMCM_B题skill训练宝/优秀论文/2022/B086` | .jpg, .txt | 1–32 (32 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-2dd18aef554f | 优秀论文 | 2023 | B | B226 | B226 | `CUMCM_B题skill训练宝/优秀论文/2023/B226` | .jpg, .txt | 1–51 (51 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-9656ff12349e | 优秀论文 | 2023 | B | B311 | B311 | `CUMCM_B题skill训练宝/优秀论文/2023/B311` | .jpg, .txt | 1–34 (34 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-922010858ece | 优秀论文 | 2023 | B | B477 | B477 | `CUMCM_B题skill训练宝/优秀论文/2023/B477` | .jpg, .txt | 1–50 (50 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-1d7cb75ebd96 | 优秀论文 | 2024 | B | B159 | B159 | `CUMCM_B题skill训练宝/优秀论文/2024/B159` | .jpg, .txt | 1–37 (37 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-3c9be1dbd3e5 | 优秀论文 | 2024 | B | B195 | B195 | `CUMCM_B题skill训练宝/优秀论文/2024/B195` | .jpg, .txt | 1–70 (70 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-cff1bf003d2c | 优秀论文 | 2024 | B | B196 | B196 | `CUMCM_B题skill训练宝/优秀论文/2024/B196` | .jpg, .txt | 1–28 (28 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-6005e94c9e67 | 优秀论文 | 2025 | B | B060 | B060 | `CUMCM_B题skill训练宝/优秀论文/2025/B060` | .jpg, .txt | 1–72 (72 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | HOLDOUT_LOCKED | 3 |
| SRC-d3220cc480d4 | 优秀论文 | 2025 | B | B157 | B157 | `CUMCM_B题skill训练宝/优秀论文/2025/B157` | .jpg, .txt | 1–67 (67 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | HOLDOUT_LOCKED | 3 |
| SRC-f17470e228fc | 参考经典论文 | 2018 | B | B203 | B203 | `CUMCM_B题skill训练宝/参考经典论文/2018/B203` | .pdf, .txt | B203.pdf=56 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-e947282cddac | 参考经典论文 | 2018 | B | B217 | B217 | `CUMCM_B题skill训练宝/参考经典论文/2018/B217` | .pdf, .txt | B217.pdf=45 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-a3bc6b564489 | 参考经典论文 | 2018 | B | B334 | B334 | `CUMCM_B题skill训练宝/参考经典论文/2018/B334` | .pdf, .txt | B334.pdf=29 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-62bd4f9cc941 | 参考经典论文 | 2020 | B | B078 | B078 | `CUMCM_B题skill训练宝/参考经典论文/2020/B078` | .jpg | 0–49 (50 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 0 |
| SRC-4831a3b18bb7 | 参考经典论文 | 2020 | B | B108 | B108 | `CUMCM_B题skill训练宝/参考经典论文/2020/B108` | .jpg | 0–99 (100 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 0 |
| SRC-c205cb3c4bfc | 参考经典论文 | 2020 | B | B125 | B125 | `CUMCM_B题skill训练宝/参考经典论文/2020/B125` | .jpg | 0–33 (34 images) | OBSERVED_SEQUENCE_CONTIGUOUS_DECLARED_TOTAL_UNVERIFIED | NOT_HOLDOUT | 0 |
| SRC-0c22fbf5301f | 赛题 | 2018 | B | UNVERIFIED | 年度根目录多赛题文件 | `CUMCM_B题skill训练宝/赛题/2018/2018-B-Chinese` | .doc, .rar | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-9992e98f513e | 赛题 | 2020 | UNVERIFIED | UNVERIFIED | 2020 | `CUMCM_B题skill训练宝/赛题/2020` | .doc | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-710e1a0526e8 | 赛题 | 2020 | A | UNVERIFIED | 2020A-炉温曲线 | `CUMCM_B题skill训练宝/赛题/2020/A` | .csv, .docx, .xlsx | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 4 |
| SRC-70ad205f7ef3 | 赛题 | 2020 | B | UNVERIFIED | 2020B-穿越沙漠 | `CUMCM_B题skill训练宝/赛题/2020/B` | .docx, .xlsx | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-7f5a84550812 | 赛题 | 2020 | C | UNVERIFIED | 2020C-中小微企业的信贷决策 | `CUMCM_B题skill训练宝/赛题/2020/C` | .docx, .xlsx | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-076a63d12334 | 赛题 | 2020 | D | UNVERIFIED | 2020D-接触式轮廓仪的自动标注 | `CUMCM_B题skill训练宝/赛题/2020/D` | .docx, .xlsx | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-f020aa988424 | 赛题 | 2020 | E | UNVERIFIED | 2020E-校园供水系统智能管理 | `CUMCM_B题skill训练宝/赛题/2020/E` | .docx, .xlsx | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-bbcd2e60afa9 | 赛题 | 2021 | UNVERIFIED | UNVERIFIED | 2021 | `CUMCM_B题skill训练宝/赛题/2021` | .doc | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-fed5a8e63e00 | 赛题 | 2021 | A | UNVERIFIED | CUMCM2021-A | `CUMCM_B题skill训练宝/赛题/2021/A` | .csv, .pdf, .xlsx | CUMCM2021-A.pdf=3 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-6cb49090e816 | 赛题 | 2021 | B | UNVERIFIED | CUMCM2021-B | `CUMCM_B题skill训练宝/赛题/2021/B` | .pdf, .xlsx | CUMCM2021-B.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-c54bced2dd31 | 赛题 | 2021 | C | UNVERIFIED | CUMCM2021-C | `CUMCM_B题skill训练宝/赛题/2021/C` | .pdf, .xlsx | CUMCM2021-C.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-a6f6061a3e5a | 赛题 | 2021 | D | UNVERIFIED | CUMCM2021-D | `CUMCM_B题skill训练宝/赛题/2021/D` | .pdf | CUMCM2021-D.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 0 |
| SRC-ededcc2cba03 | 赛题 | 2021 | E | UNVERIFIED | CUMCM2021-E | `CUMCM_B题skill训练宝/赛题/2021/E` | .pdf, .xlsx | CUMCM2021-E.pdf=3 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-9580ab24cf5e | 赛题 | 2022 | MULTIPLE | UNVERIFIED | 年度根目录多赛题文件 | `CUMCM_B题skill训练宝/赛题/2022` | .doc, .pdf, .rar | B题.pdf=2; D题.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 5 |
| SRC-8b088cf2558c | 赛题 | 2023 | MULTIPLE | UNVERIFIED | D题 | `CUMCM_B题skill训练宝/赛题/2023` | .doc, .pdf, .rar | D题.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 5 |
| SRC-674f39535948 | 赛题 | 2024 | UNVERIFIED | UNVERIFIED | 2024 | `CUMCM_B题skill训练宝/赛题/2024` | .doc | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 2 |
| SRC-1423f499c399 | 赛题 | 2024 | A | UNVERIFIED | A题 | `CUMCM_B题skill训练宝/赛题/2024/A题` | .pdf | A题.pdf=3 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-dcf56c13c2d1 | 官方附件 | 2024 | A | UNVERIFIED | A题/附件 | `CUMCM_B题skill训练宝/赛题/2024/A题/附件` | .xlsx | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-fb8d66aeff99 | 赛题 | 2024 | B | UNVERIFIED | B题 | `CUMCM_B题skill训练宝/赛题/2024/B题` | .pdf | B题.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-b225ec6916b8 | 赛题 | 2024 | C | UNVERIFIED | C题 | `CUMCM_B题skill训练宝/赛题/2024/C题` | .pdf, .xlsx | C题.pdf=1 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-fb40c0dc288d | 官方附件 | 2024 | C | UNVERIFIED | C题/附件3 | `CUMCM_B题skill训练宝/赛题/2024/C题/附件3` | .xlsx | UNVERIFIED | UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-52fdc5b5b6df | 赛题 | 2024 | D | UNVERIFIED | D题 | `CUMCM_B题skill训练宝/赛题/2024/D题` | .pdf | D题.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 1 |
| SRC-905e9d4b4c40 | 赛题 | 2024 | E | UNVERIFIED | E题 | `CUMCM_B题skill训练宝/赛题/2024/E题` | .csv, .pdf, .xlsx | E题.pdf=1; 附件3.pdf=1 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | NOT_HOLDOUT | 3 |
| SRC-b89498a15c5f | 赛题 | 2025 | UNVERIFIED | UNVERIFIED | 2025 | `CUMCM_B题skill训练宝/赛题/2025` | .doc | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 2 |
| SRC-8c57a0f07d5c | 赛题 | 2025 | A | UNVERIFIED | A题 | `CUMCM_B题skill训练宝/赛题/2025/A题` | .pdf | A题.pdf=1 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-23bdb025389d | 官方附件 | 2025 | A | UNVERIFIED | A题/附件 | `CUMCM_B题skill训练宝/赛题/2025/A题/附件` | .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-8662afd67e0f | 赛题 | 2025 | B | UNVERIFIED | B题 | `CUMCM_B题skill训练宝/赛题/2025/B题` | .pdf | B题.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-cace74a2951d | 官方附件 | 2025 | B | UNVERIFIED | B题/附件 | `CUMCM_B题skill训练宝/赛题/2025/B题/附件` | .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-d38facaf8b96 | 赛题 | 2025 | C | UNVERIFIED | C题 | `CUMCM_B题skill训练宝/赛题/2025/C题` | .pdf, .xlsx | C题.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 3 |
| SRC-87abd03556ad | 赛题 | 2025 | D | UNVERIFIED | D题 | `CUMCM_B题skill训练宝/赛题/2025/D题` | .pdf | D题.pdf=2 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-962190292db4 | 官方附件 | 2025 | D | UNVERIFIED | D题/附件 | `CUMCM_B题skill训练宝/赛题/2025/D题/附件` | .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-22ce9f7cd50f | 官方附件 | 2025 | D | UNVERIFIED | D题/附件/附件3 | `CUMCM_B题skill训练宝/赛题/2025/D题/附件/附件3` | .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 0 |
| SRC-d8289d97edde | 赛题 | 2025 | E | UNVERIFIED | E题 | `CUMCM_B题skill训练宝/赛题/2025/E题` | .pdf | E题.pdf=1 | PDF_PAGE_COUNT_OBSERVED_COMPLETENESS_UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-30284720e8a1 | 官方附件 | 2025 | E | UNVERIFIED | E题/附件 | `CUMCM_B题skill训练宝/赛题/2025/E题/附件` | .jpg, .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 2 |
| SRC-e04b3ae70ca6 | 官方附件 | 2025 | E | UNVERIFIED | E题/附件/附件1 | `CUMCM_B题skill训练宝/赛题/2025/E题/附件/附件1` | .mp4, .txt, .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-749a592ca0b8 | 官方附件 | 2025 | E | UNVERIFIED | E题/附件/附件3/姿势调整前 | `CUMCM_B题skill训练宝/赛题/2025/E题/附件/附件3/姿势调整前` | .mp4, .txt, .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-73635a5fc5b6 | 官方附件 | 2025 | E | UNVERIFIED | E题/附件/附件3/姿势调整后 | `CUMCM_B题skill训练宝/赛题/2025/E题/附件/附件3/姿势调整后` | .mp4, .txt, .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |
| SRC-9927e4bdf09e | 官方附件 | 2025 | E | UNVERIFIED | E题/附件/附件5 | `CUMCM_B题skill训练宝/赛题/2025/E题/附件/附件5` | .mp4, .xlsx | UNVERIFIED | UNVERIFIED | OFFICIAL_2025_METADATA_ONLY | 1 |

## 未解决但不阻塞 P1 的事项

- `P1-U001` [OPEN]: 专家评议/2019/同心协力策略分析 has no file for numeric page 71 within observed 1-75.
- `P1-U002` [UNVERIFIED]: Declared page totals are unavailable under the permitted boundary; contiguous observed sequences are not asserted complete against an external total.
- `P1-U003` [UNVERIFIED]: Archives were not opened and DOC/DOCX page counts were not inferred; package/page completeness remains UNVERIFIED for those formats.
- `P1-U004` [QUARANTINED]: Two download-summary/task folders may reference 2025 expert material; they are distinguishable from official problem/attachment paths, remained unopened, and are quarantined.
- `P1-U005` [UNVERIFIED]: No 赛题/2019 directory was observed; whether 2019 was intended in the corpus scope is not declared and therefore remains UNVERIFIED rather than asserted missing.

## evidence_refs

- source_path: `CUMCM_B题skill训练宝`
  locator: recursive directory and filename inventory; 86 child directories and 1504 files
  source_role: agent_inference
  supports: P1 audit scope, directory/file counts, source-folder definition, formats, sizes, modification times, duplicate filenames, and zero/small-file checks.
- source_path: `CUMCM_B题skill训练宝/参考经典论文/2020/B125`
  locator: filenames B125_00.jpg through B125_33.jpg parsed by last numeric token
  source_role: displayed_paper
  supports: B125 observed numeric image sequence is 0-33, 34 files, with no duplicate, internal gap, or unparsed filename.
- source_path: `CUMCM_B题skill训练宝/专家评议/2019/同心协力策略分析`
  locator: page_001.jpg through page_070.jpg; no page_071.*; page_072.jpeg, page_073.png, page_074.jpg, page_075.png
  source_role: expert_commentary
  supports: Observed 1-75 numeric range has 74 image files, missing 71, with mixed JPG/JPEG/PNG extensions.
- source_path: `cumcm-b-skill/planning/workflow_manifest.json`
  locator: $.phases; $.p0_alignment.status; $.development_root
  source_role: derived_artifact
  supports: P1 preconditions: P0 complete, P0 alignment complete, P1 pending before execution, later stages pending, and development root aligned.
