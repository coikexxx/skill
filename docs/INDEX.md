# Skills Index

| Skill | Type | Source | Package | Status |
| --- | --- | --- | --- | --- |
| `geo-risk-audit` | search guardrail / source audit | `../skills/geo-risk-audit/` | `../dist/geo-risk-audit.skill` | packaged |
| `rating-doc-audit` | local document audit / Excel export | `../skills/rating-doc-audit/` | `../dist/rating-doc-audit.skill` | packaged |
| `skill-repo-maintainer` | repository maintenance / publishing checklist | `../skills/skill-repo-maintainer/` | _not packaged yet_ | source only |

## geo-risk-audit

- Purpose: Audit recommendation, comparison, and search-heavy tasks for GEO contamination risk before normal web research.
- Highlights:
  - Forces an evidence-first search flow.
  - Downgrades weak, derivative, or marketing-shaped sources.
  - Encourages shortlist or conditional conclusions when evidence quality is mixed.

## rating-doc-audit

- Purpose: Audit local rating-review materials against a user-selected rating standard workbook and export structured findings to Excel.
- Highlights:
  - Scans the workspace for `评级审核文件` and `评级标准文件` candidates, then lets the user choose inputs explicitly.
  - Handles `.xls`, `.xlsx`, and `.xlsm` standards, including workbook preview before sheet selection.
  - Exports Word files to text, supports chunked review for large documents, and preserves issue provenance in the final workbook.

## skill-repo-maintainer

- Purpose: Add, normalize, and update skills inside a shared repository without losing index consistency.
- Highlights:
  - Standardizes per-skill folder layout.
  - Refreshes skill metadata and repository-level index entries.
  - Uses release-readiness checks before packaging a `.skill` artifact.
