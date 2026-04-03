# Acceptance Checklist

Run this checklist before claiming the skill or its scripts are ready.

## Skill Discovery

- Confirm `SKILL.md` frontmatter uses a short `description` that only describes when to use the skill.
- Confirm the body explains the workflow, guardrails, and output contract without repeating low-level script details.
- Confirm the skill explicitly says not to auto-pick files or sheets.

## Script And Contract Alignment

- Confirm `scripts/list_workspace_files.ps1` scans `评级审核文件` and `评级标准文件`.
- Confirm `scripts/write_audit_xlsx.py` writes worksheet `审核结果`.
- Confirm the output columns are exactly `问题`, `问题描述`, `问题出处`.
- Confirm `SKILL.md` uses the same folder names, sheet name, and output headers as the scripts.

## Minimum Regression Scenarios

1. Missing folder scenario
   - Run the scan in a workspace that lacks one or both required folders.
   - Verify the workflow stops and reports the missing folder clearly.

2. Legacy `.xls` standard scenario
   - Select a standard workbook in `.xls` format.
   - Verify the workflow converts it before inspection.

3. Large text scenario
   - Run `chunk_text.py` on a large exported document.
   - Verify `manifest.json` is created and each chunk records line ranges.

4. Result workbook scenario
   - Generate a workbook from sample findings JSON.
   - Verify the file opens normally and the worksheet and column headers match the contract.
