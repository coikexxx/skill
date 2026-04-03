#!/usr/bin/env python3
import argparse
import json
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


SHEET_NAME = "审核结果"
HEADERS = ["问题", "问题描述", "问题出处"]


def load_findings(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(payload, list):
        findings = payload
    else:
        findings = payload.get("findings", [])
    if not isinstance(findings, list):
        raise ValueError("Input JSON must be a list or an object with a findings list.")
    return findings


def inline_cell(ref: str, value: str, style: int | None = None) -> str:
    style_attr = f' s="{style}"' if style is not None else ""
    safe_value = escape(value or "")
    return f'<c r="{ref}" t="inlineStr"{style_attr}><is><t xml:space="preserve">{safe_value}</t></is></c>'


def build_sheet_xml(findings: list[dict]) -> str:
    rows = []
    header_cells = []
    for idx, header in enumerate(HEADERS):
        cell_ref = f"{chr(65 + idx)}1"
        header_cells.append(inline_cell(cell_ref, header, style=1))
    rows.append(f'<row r="1">{"".join(header_cells)}</row>')

    for row_index, finding in enumerate(findings, start=2):
        cells = []
        for col_index, header in enumerate(HEADERS):
            cell_ref = f"{chr(65 + col_index)}{row_index}"
            value = ""
            if isinstance(finding, dict):
                value = str(finding.get(header, ""))
            cells.append(inline_cell(cell_ref, value))
        rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    sheet_data = "".join(rows)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        '<cols>'
        '<col min="1" max="1" width="28" customWidth="1"/>'
        '<col min="2" max="2" width="72" customWidth="1"/>'
        '<col min="3" max="3" width="42" customWidth="1"/>'
        '</cols>'
        f"<sheetData>{sheet_data}</sheetData>"
        "</worksheet>"
    )


def build_styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2">'
        '<font><sz val="11"/><name val="Calibri"/></font>'
        '<font><b/><sz val="11"/><name val="Calibri"/></font>'
        '</fonts>'
        '<fills count="2">'
        '<fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill>'
        '</fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
        '</cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Write audit findings to a minimal xlsx workbook.")
    parser.add_argument("input_json")
    parser.add_argument("output_xlsx")
    args = parser.parse_args()

    findings = load_findings(Path(args.input_json))
    output_path = Path(args.output_xlsx)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
            '</Types>',
        )
        archive.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            '</Relationships>',
        )
        archive.writestr(
            "docProps/core.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{SHEET_NAME}</dc:title>"
            '<dc:creator>Codex</dc:creator>'
            '</cp:coreProperties>',
        )
        archive.writestr(
            "docProps/app.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Application>Codex</Application>'
            '</Properties>',
        )
        archive.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<sheets><sheet name="{SHEET_NAME}" sheetId="1" r:id="rId1"/></sheets>'
            '</workbook>',
        )
        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '</Relationships>',
        )
        archive.writestr("xl/styles.xml", build_styles_xml())
        archive.writestr("xl/worksheets/sheet1.xml", build_sheet_xml(findings))

    print(str(output_path.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
