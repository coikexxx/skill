#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


WORD_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def find_tesseract() -> str | None:
    configured = os.environ.get("TESSERACT_PATH")
    if configured and Path(configured).exists():
        return configured
    return shutil.which("tesseract")


def paragraph_text(paragraph: ET.Element) -> str:
    parts: list[str] = []
    for node in paragraph.iter():
        if node.tag == f"{{{WORD_NS['w']}}}t" and node.text:
            parts.append(node.text)
        elif node.tag == f"{{{WORD_NS['w']}}}tab":
            parts.append("\t")
    return "".join(parts).strip()


def load_relationships(archive: zipfile.ZipFile) -> dict[str, str]:
    try:
        raw = archive.read("word/_rels/document.xml.rels")
    except KeyError:
        return {}
    root = ET.fromstring(raw)
    mapping: dict[str, str] = {}
    for rel in root.findall("pkgrel:Relationship", WORD_NS):
        mapping[rel.attrib["Id"]] = rel.attrib["Target"]
    return mapping


def paragraph_image_targets(paragraph: ET.Element, relationships: dict[str, str]) -> list[str]:
    targets: list[str] = []
    for blip in paragraph.findall(".//a:blip", WORD_NS):
        rel_id = blip.attrib.get(f"{{{WORD_NS['r']}}}embed")
        if rel_id and rel_id in relationships:
            targets.append(f"word/{relationships[rel_id].lstrip('/')}")
    return targets


def table_context(table: ET.Element) -> str:
    texts: list[str] = []
    for cell in table.findall(".//w:tc", WORD_NS):
        cell_text = "".join(
            (node.text or "")
            for node in cell.iter()
            if node.tag == f"{{{WORD_NS['w']}}}t" and node.text
        ).strip()
        if cell_text:
            texts.append(cell_text)
    return " | ".join(texts[:4]).strip()


def run_tesseract(image_path: Path) -> tuple[str, str]:
    tesseract = find_tesseract()
    if not tesseract:
        return "skipped", ""

    result = subprocess.run(
        [tesseract, str(image_path), "stdout"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return "failed", (result.stderr or result.stdout).strip()
    return "ok", result.stdout.strip()


def extract_docx_text(docx_path: Path, temp_root: Path | None = None) -> str:
    with zipfile.ZipFile(docx_path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
        relationships = load_relationships(archive)
        body = root.find("w:body", WORD_NS)
        if body is None:
            return ""

        blocks: list[dict] = []
        image_counter = 0

        for child in list(body):
            if child.tag == f"{{{WORD_NS['w']}}}p":
                text = paragraph_text(child)
                image_targets = paragraph_image_targets(child, relationships)
                if text:
                    blocks.append({"type": "text", "text": text})
                for target in image_targets:
                    image_counter += 1
                    blocks.append(
                        {
                            "type": "image",
                            "image_id": f"image-{image_counter:03d}",
                            "image_target": target,
                            "table_context": "",
                        }
                    )
            elif child.tag == f"{{{WORD_NS['w']}}}tbl":
                context = table_context(child)
                if context:
                    blocks.append({"type": "text", "text": f"[table-context] {context}"})
                for paragraph in child.findall(".//w:p", WORD_NS):
                    image_targets = paragraph_image_targets(paragraph, relationships)
                    for target in image_targets:
                        image_counter += 1
                        blocks.append(
                            {
                                "type": "image",
                                "image_id": f"image-{image_counter:03d}",
                                "image_target": target,
                                "table_context": context,
                            }
                        )

        lines: list[str] = []
        tesseract = find_tesseract()

        for index, block in enumerate(blocks):
            if block["type"] == "text":
                lines.append(block["text"])
                continue

            previous_text = ""
            next_text = ""
            for previous in reversed(blocks[:index]):
                if previous["type"] == "text" and previous["text"]:
                    previous_text = previous["text"]
                    break
            for following in blocks[index + 1 :]:
                if following["type"] == "text" and following["text"]:
                    next_text = following["text"]
                    break

            ocr_status = "skipped"
            ocr_text = ""
            if tesseract:
                if temp_root is None:
                    raise RuntimeError("OCR requires a writable temp_root when tesseract is available.")
                temp_root.mkdir(parents=True, exist_ok=True)
                image_path = temp_root / f"{block['image_id']}{Path(block['image_target']).suffix.lower()}"
                image_path.write_bytes(archive.read(block["image_target"]))
                ocr_status, ocr_text = run_tesseract(image_path)

            lines.append(f"[{block['image_id']}]")
            if block["table_context"]:
                lines.append(f"table_context: {block['table_context']}")
            lines.append(f"anchor_previous: {previous_text}")
            lines.append(f"anchor_next: {next_text}")
            lines.append(f"ocr_status: {ocr_status}")
            if ocr_text:
                lines.append(f"ocr_text: {ocr_text}")

        return "\n".join(line for line in lines if line).strip() + ("\n" if lines else "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export .docx text and inline-image OCR context without Word COM.")
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    if input_path.suffix.lower() != ".docx":
        raise SystemExit("export_docx_text.py only supports .docx files.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_root = output_path.parent / ".ocr-tmp"
    output_path.write_text(extract_docx_text(input_path, temp_root=temp_root), encoding="utf-8")
    if temp_root.exists():
        shutil.rmtree(temp_root, ignore_errors=True)

    print(
        json.dumps(
            {
                "input_path": str(input_path.resolve()),
                "output_path": str(output_path.resolve()),
                "method": "python-docx-xml",
                "tesseract_path": find_tesseract(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
