#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path


def find_soffice() -> str | None:
    configured = os.environ.get("SOFFICE_PATH")
    if configured:
        configured_path = Path(configured)
        if configured_path.exists():
            return str(configured_path)

    for candidate in ("soffice", "libreoffice"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def convert_with_soffice(input_path: Path, output_dir: Path, convert_to: str) -> subprocess.CompletedProcess[str]:
    soffice = find_soffice()
    if not soffice:
        raise RuntimeError("This conversion requires soffice, but no soffice executable was found.")

    output_dir.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        [soffice, "--headless", "--convert-to", convert_to, "--outdir", str(output_dir), str(input_path)],
        text=True,
        capture_output=True,
        check=False,
    )
