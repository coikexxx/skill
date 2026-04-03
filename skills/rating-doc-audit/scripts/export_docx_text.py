#!/usr/bin/env python3
import argparse
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def extract_docx_text(docx_path: Path) -> str:
    with zipfile.ZipFile(docx_path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))

    lines: list[str] = []
    for paragraph in root.findall(".//w:p", WORD_NS):
        text_parts: list[str] = []
        for node in paragraph.iter():
            if node.tag == f"{{{WORD_NS['w']}}}t" and node.text:
                text_parts.append(node.text)
            elif node.tag == f"{{{WORD_NS['w']}}}tab":
                text_parts.append("\t")
        line = "".join(text_parts).strip()
        if line:
            lines.append(line)

    return "\n".join(lines) + ("\n" if lines else "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export .docx text without Word COM.")
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    if input_path.suffix.lower() != ".docx":
        raise SystemExit("export_docx_text.py only supports .docx files.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(extract_docx_text(input_path), encoding="utf-8")

    print(
        json.dumps(
            {
                "input_path": str(input_path.resolve()),
                "output_path": str(output_path.resolve()),
                "method": "python-docx-xml",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
