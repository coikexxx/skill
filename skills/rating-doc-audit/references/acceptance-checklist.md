# Acceptance Checklist

Run this checklist before claiming the skill or its scripts are ready.

## Skill Discovery

- Confirm `SKILL.md` frontmatter uses a short `description` that only describes when to use the skill.
- Confirm the body explains the workflow, routing rules, platform split, guardrails, and output contract without repeating low-level script details.
- Confirm the skill explicitly says not to auto-pick files or sheets.

## Script And Contract Alignment

- Confirm `scripts/list_workspace_files.py` is the default scan entrypoint.
- Confirm `scripts/export_review_text.py` prefers Python for `.docx` and requires `soffice` for `.doc`.
- Confirm `scripts/prepare_standard_workbook.py` keeps `.xlsx` / `.xlsm` on the direct Python path and routes `.xls` through `soffice`.
- Confirm `scripts/write_audit_xlsx.py` writes worksheet `审核结果`.
- Confirm the output columns are exactly `问题`, `问题描述`, `问题出处`.
- Confirm `SKILL.md` uses the same folder names, sheet name, and output headers as the scripts.

## Platform Expectations

- Confirm the docs clearly describe the no-`soffice` partial-usable path.
- Confirm the docs do not imply that `.doc` or `.xls` work without `soffice`.
- Confirm the docs do not imply that `.xlsx` / `.xlsm` should go through `soffice` by default.

## Minimum Regression Scenarios

1. Missing folder scenario
   - Run the scan in a workspace that lacks one or both required folders.
   - Verify the workflow stops and reports the missing folder clearly.

2. Cross-platform scan scenario
   - Run `list_workspace_files.py` without PowerShell.
   - Verify it returns the expected candidate structure.

3. No-`soffice` partial-usable scenario
   - Use a `.docx` review file and an `.xlsx` standard workbook.
   - Verify the workflow can still complete the portable chain without `soffice`.

4. Legacy `.doc` blocker scenario
   - Run `export_review_text.py` on a `.doc` file without `soffice`.
   - Verify it fails clearly and reports the blocker.

5. Legacy `.xls` blocker scenario
   - Run `prepare_standard_workbook.py` on a `.xls` file without `soffice`.
   - Verify it fails clearly and reports the blocker.

6. Large text scenario
   - Run `chunk_text.py` on a large exported document.
   - Verify `manifest.json` is created and each chunk records line ranges.

7. Result workbook scenario
   - Generate a workbook from sample findings JSON.
   - Verify the file opens normally and the worksheet and column headers match the contract.
