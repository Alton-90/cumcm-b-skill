# P3 PDF QA Report

- Revision: P3-R (`P3R-CORRECT-92bca105-b2c1-4b98-be7c-eeeb9ec94a64`)
- Current effective PDFs: 22
- Current effective PDF pages: 1058
- Physical PDF files retained: 23 (including the superseded 75-page audit copy)
- Text extraction performed: false
- 2025 holdout sources accessed: false

## Outcome

The 21 unchanged PDFs passed SHA-256 and pypdf page-count reverification against the frozen pre-P3-R manifest. The 2019 expert-commentary PDF was regenerated as a 70-page v2 using only original-corpus page_001.jpg through page_070.jpg, reopened with pypdf and pdfinfo, and rendered in full by Poppler. Visual checks covered PDF pages 1, 35, 69, and 70.

The original 75-page PDF is retained but classified as `SUPERSEDED_NONBODY_CONTAMINATION` because it included an auxiliary title thumbnail, a speaker photograph, and three unrelated 2026 site advertisements. This is a human-approved derived boundary, not an official declaration that the source has exactly 70 pages. Official total pages and source completeness remain `UNVERIFIED`.

## Current Output Verification

| source_id | pages | SHA-256 | verification |
|---|---:|---|---|
| SRC-c2223b8c2dd7 | 41 | `ddff44b8f96987ab152a1d76a77b2a969a8ccf81b32d9b92f9ab2e41e9c163f6` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-b4fce6295e11 | 70 | `4f9d5cbde7748465a883ebc126e2f0f2978ce39bb215cb8bb8ffa9dd102a6b23` | REGENERATED_FULL_QA_PASS |
| SRC-c1a180d84907 | 18 | `c40ed88a5347f900450255f134a5a469bf1dd9915e8fd115fa2e943c19517f2b` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-a141969616ab | 52 | `b7a88f05080c75a029134d0eac267968ed56f00e0dd5bd58d261bc019d4d8868` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-ae17dc2a53df | 78 | `37988428a1075a87f6cd66edb5354e8663778b0f917e0eb0046f4c0a0b8de376` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-34b786442a51 | 72 | `d97901734016ee46a17dce0f1ab0aa0428da25968b19a1367e04811f3f5a4465` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-e5cd698ad88f | 45 | `aa4c81184f651bc64cd4185034bfbd9a8575c56ae8cc387c2d20215e25e8cf23` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-8f01c87998ac | 26 | `ddb2102efa9054d14e65b786d12b47d6cc65c3b4a94eddc6d8cd3d0ea20cc7b6` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-50e9cdc8922a | 59 | `a4b33259c7e7475ad7eca3213b84c5cdae13162135e5d3e007fda53b32907b75` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-f9723b6fec3b | 28 | `d2998b26cc7e330a9e014dccfe9059df5663530591f82bd9feb5940a98ed97a6` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-f7da546613ae | 42 | `995f3bbbb0b961411f385adee07ed9f13446defaf24ff744180ea4ad049ff4bd` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-ff5379123217 | 41 | `cae7a9352bee8b7edb9f3c540be1c4833c1b90bd2aab406627f7ac4c72d6aa1a` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-4b50124526fd | 32 | `4b17e7c4defe2c147d766bdd236e6292b26365ce2ec4358e8b93133ead811738` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-2dd18aef554f | 51 | `150ef2fa6b57cb5f76e08857f44878d919050179e58f69b518469519ea1785bc` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-9656ff12349e | 34 | `eb20d7166a68cc28fa3620211cb6c97b463edc7fde5037aa9a1a187956f6e626` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-922010858ece | 50 | `2d1ec9736da1a6ba387f0838f55647c4f33dffa564d92f41cacea649f5e905c2` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-1d7cb75ebd96 | 37 | `50263729a8e0a6d7db1a0ca5915d60465ad54a9ea0230adbf9ce4ffc5913f320` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-3c9be1dbd3e5 | 70 | `60d89177308a62ff46f11da92df9c7ae6e79b87cf8da11077a1bdc7a153fb74c` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-cff1bf003d2c | 28 | `05aee44313ef8274dce7ac838ffec21912480ca3010c5b4949500c7592ed3f43` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-62bd4f9cc941 | 50 | `1ad7241e403e9bd517e64bc1790363c8bc7adea02b4091dbf2c11e00b1063255` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-4831a3b18bb7 | 100 | `b796bb905f90a3f6aafb709756ec79bd8fa8a17d18699d2565b41a1034215a04` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |
| SRC-c205cb3c4bfc | 34 | `def65ed4b7b0e0f8d38e6352d0d01c7f771b77630ba9c641e1875e79fa0139b8` | UNCHANGED_HASH_AND_PAGECOUNT_PASS |

## evidence_refs

- source_path: `cumcm-b-skill/derived/pdf/pdf_manifest.json`
  locator: `$.source_count=22; $.total_pdf_pages=1058; $.sources[*]`
  source_role: `derived_artifact`
  supports: Identifies the 22 current PDFs, current hashes and page counts, and the retained superseded 75-page audit output.
- source_path: `cumcm-b-skill/qa/p3r/p3r_2019_v2_qa.json`
  locator: `$.unchanged_pdf_reverification.status=PASS; $.v2_qa.mechanical_qa_status=PASS`
  source_role: `agent_inference`
  supports: Records the 21 unchanged hash/page-count checks and the 70-page v2 structural, full-render, mapping, blank, crop/stretch, and order QA.
- source_path: `cumcm-b-skill/qa/p3r/p3r_boundary_evidence.json`
  locator: `$.classification_basis=human_approved_derivation; $.document_body_sequence; $.excluded_observed_files`
  source_role: `agent_inference`
  supports: Records why the old 75-page PDF was superseded while official total pages remain UNVERIFIED.
- source_path: `cumcm-b-skill/planning/workflow_manifest.json`
  locator: `$.phases.P3.status=complete; $.phases.P4.status=pending`
  source_role: `derived_artifact`
  supports: Confirms P3 remains complete and P4 was not started.
