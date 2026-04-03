# Platform Support

## Default Execution Model

The skill now uses Python as the default entry layer. Prefer the Python scripts first and use the Windows PowerShell / COM scripts only as compatibility fallbacks.

## Direct Python Paths

These steps do not require `soffice` or Office COM:

- `scripts/list_workspace_files.py`
- `scripts/inspect_xlsx.py`
- `scripts/chunk_text.py`
- `scripts/write_audit_xlsx.py`
- `scripts/export_docx_text.py` for `.docx`

## Routed Document Export

- `.docx`: prefer Python parsing through `scripts/export_review_text.py`
- `.docx` fallback: use `soffice` only if the Python parser fails
- `.doc`: require `soffice`

## Routed Workbook Preparation

- `.xlsx`: direct Python path
- `.xlsm`: direct Python path
- `.xls`: require `soffice`

Do not treat `soffice` as the default route for every Office file. It is mainly the portability layer for formats that the Python path cannot handle directly.

## Windows Fallbacks

These scripts remain useful when the environment is Windows-first:

- `scripts/list_workspace_files.ps1`
- `scripts/export_word_text.ps1`
- `scripts/convert_excel_to_xlsx.ps1`

## No-soffice Scenario

If `soffice` is unavailable, the skill is still partially usable when the selected files stay on the direct Python path:

- `.docx` review file
- `.xlsx` or `.xlsm` standard workbook

If the user selected `.doc` or `.xls`, stop and report that the current environment lacks the required converter.
