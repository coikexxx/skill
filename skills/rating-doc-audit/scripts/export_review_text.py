#!/usr/bin/env python3
import argparse
import json
import shutil
import sys
from pathlib import Path

from export_docx_text import extract_docx_text
from soffice_utils import convert_with_soffice, find_soffice


def export_with_python_docx(input_path: Path, output_path: Path) -> dict:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(extract_docx_text(input_path), encoding="utf-8")
    return {
        "input_path": str(input_path.resolve()),
        "output_path": str(output_path.resolve()),
        "method": "python-docx-xml",
    }


def export_with_soffice(input_path: Path, output_path: Path) -> dict:
    result = convert_with_soffice(input_path, output_path.parent, "txt:Text")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "soffice conversion failed")

    soffice_output = output_path.parent / f"{input_path.stem}.txt"
    if not soffice_output.exists():
        raise RuntimeError("soffice reported success but did not create the expected .txt output")

    if soffice_output.resolve() != output_path.resolve():
        shutil.move(str(soffice_output), str(output_path))

    return {
        "input_path": str(input_path.resolve()),
        "output_path": str(output_path.resolve()),
        "method": "soffice",
        "soffice_path": find_soffice(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export review documents to text using Python or soffice.")
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    suffix = input_path.suffix.lower()

    try:
        if suffix == ".docx":
            try:
                payload = export_with_python_docx(input_path, output_path)
            except Exception:
                if find_soffice():
                    payload = export_with_soffice(input_path, output_path)
                else:
                    raise RuntimeError(
                        "The .docx Python parser failed and fallback export requires soffice, but no soffice executable was found."
                    )
        elif suffix == ".doc":
            if not find_soffice():
                raise RuntimeError("Exporting legacy .doc files requires soffice, but no soffice executable was found.")
            payload = export_with_soffice(input_path, output_path)
        else:
            raise RuntimeError("export_review_text.py supports only .doc and .docx input files.")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
