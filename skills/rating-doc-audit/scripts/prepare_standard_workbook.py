#!/usr/bin/env python3
import argparse
import json
import shutil
import sys
from pathlib import Path

from soffice_utils import convert_with_soffice, find_soffice


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a rating standard workbook for inspection.")
    parser.add_argument("input_path")
    parser.add_argument("--output-path")
    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()
    suffix = input_path.suffix.lower()

    try:
        if suffix in {".xlsx", ".xlsm"}:
            payload = {
                "workbook_path": str(input_path),
                "method": "direct",
                "converted": False,
            }
        elif suffix == ".xls":
            if not find_soffice():
                raise RuntimeError("Preparing legacy .xls files requires soffice, but no soffice executable was found.")

            output_path = Path(args.output_path).resolve() if args.output_path else input_path.with_suffix(".xlsx")
            result = convert_with_soffice(input_path, output_path.parent, "xlsx")
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "soffice workbook conversion failed")

            soffice_output = output_path.parent / f"{input_path.stem}.xlsx"
            if not soffice_output.exists():
                raise RuntimeError("soffice reported success but did not create the expected .xlsx output")

            if soffice_output.resolve() != output_path.resolve():
                output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(soffice_output), str(output_path))

            payload = {
                "workbook_path": str(output_path.resolve()),
                "method": "soffice",
                "converted": True,
                "soffice_path": find_soffice(),
            }
        else:
            raise RuntimeError("prepare_standard_workbook.py supports only .xls, .xlsx, and .xlsm files.")
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
