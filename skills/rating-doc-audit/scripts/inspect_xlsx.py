#!/usr/bin/env python3
import argparse
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def column_index_from_ref(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        return 0
    value = 0
    for char in match.group(1):
        value = value * 26 + (ord(char) - 64)
    return value - 1


def load_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        raw = archive.read("xl/sharedStrings.xml")
    except KeyError:
        return []

    root = ET.fromstring(raw)
    values = []
    for si in root.findall("main:si", NS):
        text_parts = []
        for node in si.iter():
            if node.tag == f"{{{NS['main']}}}t":
                text_parts.append(node.text or "")
        values.append("".join(text_parts))
    return values


def workbook_relationships(archive: zipfile.ZipFile) -> dict[str, str]:
    root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    mapping = {}
    for rel in root.findall("pkgrel:Relationship", NS):
        mapping[rel.attrib["Id"]] = rel.attrib["Target"]
    return mapping


def workbook_sheets(archive: zipfile.ZipFile) -> list[dict[str, str]]:
    rels = workbook_relationships(archive)
    root = ET.fromstring(archive.read("xl/workbook.xml"))
    sheets = []
    for sheet in root.findall("main:sheets/main:sheet", NS):
        rid = sheet.attrib[f"{{{NS['rel']}}}id"]
        target = rels[rid]
        if not target.startswith("worksheets/"):
            target = f"worksheets/{Path(target).name}"
        sheets.append({"name": sheet.attrib["name"], "path": f"xl/{target}"})
    return sheets


def read_cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        node = cell.find("main:is/main:t", NS)
        return node.text if node is not None and node.text is not None else ""

    value_node = cell.find("main:v", NS)
    if value_node is None or value_node.text is None:
        return ""

    value = value_node.text
    if cell_type == "s":
        index = int(value)
        return shared_strings[index] if 0 <= index < len(shared_strings) else ""
    return value


def preview_sheet(archive: zipfile.ZipFile, sheet_path: str, shared_strings: list[str], max_rows: int, max_cols: int) -> list[list[str]]:
    root = ET.fromstring(archive.read(sheet_path))
    rows = []
    for row in root.findall("main:sheetData/main:row", NS):
        values = [""] * max_cols
        for cell in row.findall("main:c", NS):
            cell_ref = cell.attrib.get("r", "")
            column_index = column_index_from_ref(cell_ref)
            if 0 <= column_index < max_cols:
                values[column_index] = read_cell_value(cell, shared_strings)
        rows.append(values)
        if len(rows) >= max_rows:
            break
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect xlsx/xlsm workbooks without external packages.")
    parser.add_argument("workbook_path")
    parser.add_argument("--max-rows", type=int, default=8)
    parser.add_argument("--max-cols", type=int, default=12)
    args = parser.parse_args()

    workbook_path = Path(args.workbook_path)
    if workbook_path.suffix.lower() not in {".xlsx", ".xlsm"}:
        raise SystemExit("inspect_xlsx.py only supports .xlsx and .xlsm. Convert .xls first.")

    with zipfile.ZipFile(workbook_path) as archive:
        shared_strings = load_shared_strings(archive)
        sheets = workbook_sheets(archive)
        payload = {
            "workbook_path": str(workbook_path.resolve()),
            "sheet_count": len(sheets),
            "sheets": [],
        }
        for sheet in sheets:
            payload["sheets"].append(
                {
                    "name": sheet["name"],
                    "preview": preview_sheet(
                        archive,
                        sheet["path"],
                        shared_strings,
                        args.max_rows,
                        args.max_cols,
                    ),
                }
            )

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
