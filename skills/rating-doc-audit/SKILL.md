---
name: rating-doc-audit
description: Use when auditing rating-review materials against local Word and Excel standards in the current workspace, especially when the agent must scan candidate files, let the user choose inputs, handle large documents safely, and export structured findings.
---

# Rating Doc Audit

Use this skill for repeatable audits of rating-review materials stored in the current workspace.

## Platform Support

The workflow now uses Python as the default control plane.

- `list_workspace_files.py`, `inspect_xlsx.py`, `chunk_text.py`, and `write_audit_xlsx.py` are the default portable tools.
- `export_review_text.py` is the default review-document export entrypoint.
- `prepare_standard_workbook.py` is the default standard-workbook entrypoint.

Portable support on Linux and macOS depends on `soffice` for the legacy formats that Python does not handle directly.

- `.docx`: prefer Python extraction first, fall back to `soffice` only if the Python parser fails.
- `.doc`: requires `soffice`.
- `.xlsx` and `.xlsm`: inspect directly with Python.
- `.xls`: requires `soffice`.

Windows-only scripts remain available as compatibility fallbacks:

- `{baseDir}/scripts/list_workspace_files.ps1`
- `{baseDir}/scripts/export_word_text.ps1`
- `{baseDir}/scripts/convert_excel_to_xlsx.ps1`

If the current environment lacks `soffice`, continue with the Python-only subset when the user-selected files are still compatible, and clearly state which formats remain blocked.

## Workflow

1. Scan the workspace root with `{baseDir}/scripts/list_workspace_files.py`.
2. Show the candidate review documents and rating standards separately, preserving the reported `index` values.
3. Ask the user to choose:
   - one file from `评级审核文件`
   - one file from `评级标准文件`
   - an optional extra audit prompt
4. Prepare the selected standard workbook.
   - Use `{baseDir}/scripts/prepare_standard_workbook.py`.
   - `.xlsx` and `.xlsm` stay on the direct Python path.
   - `.xls` routes through `soffice`.
5. Inspect the resulting workbook with `{baseDir}/scripts/inspect_xlsx.py`, identify the relevant sheets, and translate the selected rules into a concrete checklist before judging the document.
6. Export the selected review document to text with `{baseDir}/scripts/export_review_text.py`.
   - `.docx` uses Python first.
   - `.doc` routes through `soffice`.
7. If the extracted text is too large for comfortable review, split it with `{baseDir}/scripts/chunk_text.py` and review chunk by chunk instead of loading the whole file into context.
8. Evaluate the document against the chosen rating standard and the optional user prompt.
9. Save findings to JSON first, then write the final workbook with `{baseDir}/scripts/write_audit_xlsx.py`.

## Guardrails

- Always let the user choose both inputs after scanning. Do not auto-pick a document, workbook, or worksheet unless the user explicitly asks for that.
- If the user gives no extra prompt, default to checking completeness, consistency, rule compliance, missing evidence, contradictions, and material formatting or structure issues.
- Never paste the full extracted document text into the conversation.
- When the standard is ambiguous, mark the finding as a risk or clarification need instead of a definite violation.
- If parsing fails or a required converter is unavailable, report the exact blocker and stop before the audit stage.
- Do not imply that `soffice` is required for `.docx`, `.xlsx`, or `.xlsm` when the direct Python path is available.

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

- `{baseDir}/scripts/list_workspace_files.py`: cross-platform workspace scan and the default scan entrypoint
- `{baseDir}/scripts/prepare_standard_workbook.py`: route `.xlsx` / `.xlsm` directly and convert `.xls` via `soffice` when needed
- `{baseDir}/scripts/export_review_text.py`: route `.docx` through Python first and `.doc` through `soffice`
- `{baseDir}/scripts/export_docx_text.py`: direct Python `.docx` text export
- `{baseDir}/scripts/inspect_xlsx.py`: inspect workbook structure and preview rows without third-party packages
- `{baseDir}/scripts/chunk_text.py`: split very large extracted text into manageable chunks with a manifest
- `{baseDir}/scripts/write_audit_xlsx.py`: write the final Excel result workbook without external dependencies
- `{baseDir}/scripts/list_workspace_files.ps1`: Windows PowerShell scan fallback
- `{baseDir}/scripts/export_word_text.ps1`: Windows Word COM export fallback
- `{baseDir}/scripts/convert_excel_to_xlsx.ps1`: Windows Excel COM conversion fallback

## Do Not

- Do not auto-select files or authoritative sheets without user confirmation.
- Do not paste full extracted text into chat.
- Do not present uncertain findings as definitive violations.
- Do not fabricate audit results when a file cannot be parsed.
- Do not route `.xlsx` or `.xlsm` through `soffice` unless there is a separate explicit reason outside this skill.

## References

- Read `{baseDir}/references/workflow-notes.md` for workbook triage, chunk-review guidance, and provenance wording.
- Read `{baseDir}/references/platform-support.md` when deciding which scripts are usable in the current environment.
- Read `{baseDir}/references/acceptance-checklist.md` before publishing changes to this skill or its scripts.
