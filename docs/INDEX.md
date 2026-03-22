# Skills Index

| Skill | Type | Source | Package | Status |
| --- | --- | --- | --- | --- |
| `geo-risk-audit` | search guardrail / source audit | `../skills/geo-risk-audit/` | `../dist/geo-risk-audit.skill` | packaged |
| `skill-repo-maintainer` | repository maintenance / publishing checklist | `../skills/skill-repo-maintainer/` | _not packaged yet_ | source only |

## geo-risk-audit

- Purpose: Audit recommendation, comparison, and search-heavy tasks for GEO contamination risk before normal web research.
- Highlights:
  - Forces evidence-first search flow.
  - Downgrades weak, derivative, or marketing-shaped sources.
  - Encourages shortlist or conditional conclusions when evidence quality is mixed.

## skill-repo-maintainer

- Purpose: Add, normalize, and update skills inside a shared repository without losing index consistency.
- Highlights:
  - Standardizes per-skill folder layout.
  - Refreshes skill metadata and repository-level index entries.
  - Uses release-readiness checks before packaging a `.skill` artifact.
