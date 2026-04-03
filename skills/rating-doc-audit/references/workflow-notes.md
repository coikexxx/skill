# Workflow Notes

## Scan And Select

Use `scripts/list_workspace_files.py` as the default scan entrypoint.

- Present review documents and standards separately.
- Preserve the reported `index` values so the user can choose by number.
- If either folder is missing, stop and report that before attempting the audit.

## Standard Workbook Triage

After previewing the workbook:

- Identify sheets that look like rule tables, checklists, disclosure requirements, or scoring standards.
- Ignore obvious cover sheets, version sheets, or pure instructions unless the user says they are authoritative.
- If several sheets look authoritative, ask the user to confirm which sheet or sheets define the active standard.

Translate the selected sheet content into a practical checklist before reviewing the document.

## Standard Routing

Route workbook preparation like this:

1. `.xlsx`: inspect directly
2. `.xlsm`: inspect directly
3. `.xls`: run `scripts/prepare_standard_workbook.py` and let it convert through `soffice`

Do not route `.xlsx` or `.xlsm` through `soffice` by default.

## Review Document Routing

Route document export like this:

1. `.docx`: run `scripts/export_review_text.py`, which should try Python first
2. `.doc`: run `scripts/export_review_text.py`, which should require `soffice`

If `.docx` parsing fails and `soffice` is unavailable, stop and report the blocker clearly.

For `.docx` files with embedded images:

- keep each image tied to its nearby paragraph or table context
- when table context is available, prefer the table text as the primary anchor
- include image id plus `anchor_previous` / `anchor_next` style context in the exported review text
- if OCR is skipped, say so inline so reviewers know the screenshot content was not audited

## Large Document Review

For huge files, use this sequence:

1. Export the review file to text.
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
