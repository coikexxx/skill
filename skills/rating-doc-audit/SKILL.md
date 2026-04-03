---
name: rating-doc-audit
description: Use when auditing rating-review materials against local Word and Excel standards in the current workspace, especially when the agent must scan candidate files, let the user choose inputs, handle large documents safely, and export structured findings.
---

# Rating Doc Audit

Use this skill for repeatable audits of rating-review materials stored in the current workspace.

## Workflow

1. Run `{baseDir}/scripts/list_workspace_files.ps1` from the workspace root.
2. Show the candidate review documents and rating standards separately, preserving the reported `index` values.
3. Ask the user to choose:
   - one file from `评级审核文件`
   - one file from `评级标准文件`
   - an optional extra audit prompt
4. If the chosen standard file is `.xls`, convert it with `{baseDir}/scripts/convert_excel_to_xlsx.ps1`.
5. Inspect the selected workbook with `{baseDir}/scripts/inspect_xlsx.py`, identify the relevant sheets, and translate the selected rules into a concrete checklist before judging the document.
6. Export the selected Word document to text with `{baseDir}/scripts/export_word_text.ps1`.
7. If the extracted text is too large for comfortable review, split it with `{baseDir}/scripts/chunk_text.py` and review chunk by chunk instead of loading the whole file into context.
8. Evaluate the document against the chosen rating standard and the optional user prompt.
9. Save findings to JSON first, then write the final workbook with `{baseDir}/scripts/write_audit_xlsx.py`.

## Guardrails

- Always let the user choose both inputs after scanning. Do not auto-pick a document, workbook, or worksheet unless the user explicitly asks for that.
- If the user gives no extra prompt, default to checking completeness, consistency, rule compliance, missing evidence, contradictions, and material formatting or structure issues.
- Never paste the full extracted document text into the conversation.
- When the standard is ambiguous, mark the finding as a risk or clarification need instead of a definite violation.
- If parsing fails or the tooling is unavailable, report the exact blocker and stop before the audit stage.

## Large-File Handling

Treat documents above 500 MB as chunked-review inputs. Smaller files should also be chunked when the extracted text is too large for comfortable context usage.

For each issue, preserve provenance with at least one of:

- section heading
- nearby quoted phrase
- table caption
- chunk id and line range

## Output Contract

Write findings to JSON first. Accepted JSON shapes:

- a top-level array of finding objects
- an object with a `findings` array

Each finding should use these keys:

- `问题`: short issue title
- `问题描述`: why it violates or risks violating the standard
- `问题出处`: where it appears in the source document

The final workbook must contain one worksheet named `审核结果` with these three columns in order:

1. `问题`
2. `问题描述`
3. `问题出处`

## Scripts

- `{baseDir}/scripts/list_workspace_files.ps1`: scan the workspace and emit candidate files as JSON
- `{baseDir}/scripts/export_word_text.ps1`: export `.doc` or `.docx` to plain text through Word COM
- `{baseDir}/scripts/convert_excel_to_xlsx.ps1`: convert `.xls` to `.xlsx` through Excel COM
- `{baseDir}/scripts/inspect_xlsx.py`: inspect workbook structure and preview rows without third-party packages
- `{baseDir}/scripts/chunk_text.py`: split very large extracted text into manageable chunks with a manifest
- `{baseDir}/scripts/write_audit_xlsx.py`: write the final Excel result workbook without external dependencies

## Do Not

- Do not auto-select files or authoritative sheets without user confirmation.
- Do not paste full extracted text into chat.
- Do not present uncertain findings as definitive violations.
- Do not fabricate audit results when a file cannot be parsed.

## References

- Read `{baseDir}/references/workflow-notes.md` for workbook triage, chunk-review guidance, and provenance wording.
- Read `{baseDir}/references/acceptance-checklist.md` before publishing changes to this skill or its scripts.
