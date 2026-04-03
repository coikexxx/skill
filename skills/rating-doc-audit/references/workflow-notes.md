# Workflow Notes

## Scan And Select

Run `scripts/list_workspace_files.ps1` at the workspace root.

- Present review documents and standards separately.
- Preserve the reported `index` values so the user can choose by number.
- If either folder is missing, stop and report that before attempting the audit.

## Standard Workbook Triage

After previewing the workbook:

- Identify sheets that look like rule tables, checklists, disclosure requirements, or scoring standards.
- Ignore obvious cover sheets, version sheets, or pure instructions unless the user says they are authoritative.
- If several sheets look authoritative, ask the user to confirm which sheet or sheets define the active standard.

Translate the selected sheet content into a practical checklist before reviewing the document.

## Large Document Review

For huge files, use this sequence:

1. Export the Word file to text.
2. Chunk the text to disk.
3. Review chunk by chunk.
4. Keep an accumulating finding list in JSON on disk.
5. Deduplicate repeated findings before writing the final workbook.

When a chunk contains a likely issue, capture at least one of:

- heading text
- nearby quoted phrase
- table caption
- chunk id and line range

## Provenance Wording

Prefer precise provenance over vague wording.

Good examples:

- `第一章 主体概况，chunk-0002 lines 201-244`
- `表 3-2 偿债指标，chunk-0005 lines 88-124`
- `“担保措施能够有效覆盖”附近段落，chunk-0007 lines 411-436`

Avoid generic wording like `文中提到` or `材料里没写`.

## Result Quality Bar

Only write an issue when there is a clear mismatch, omission, contradiction, or material ambiguity relative to the standard.

If the evidence is weak:

- state the uncertainty in `问题描述`
- still provide the best available provenance
- avoid overstating the conclusion
