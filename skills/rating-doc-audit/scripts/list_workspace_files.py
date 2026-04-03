#!/usr/bin/env python3
import json
import sys
from pathlib import Path


REVIEW_FOLDER_NAME = "评级审核文件"
STANDARD_FOLDER_NAME = "评级标准文件"


def get_candidate_files(base_path: Path, extensions: set[str]) -> list[dict]:
    if not base_path.exists():
        return []

    items = []
    for path in sorted(p for p in base_path.rglob("*") if p.is_file() and p.suffix.lower() in extensions):
        stat = path.stat()
        items.append(
            {
                "index": len(items) + 1,
                "name": path.name,
                "full_path": str(path.resolve()),
                "extension": path.suffix,
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "last_write_time": __import__("datetime").datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    return items


def main() -> int:
    workspace = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    review_folder = workspace / REVIEW_FOLDER_NAME
    standard_folder = workspace / STANDARD_FOLDER_NAME

    payload = {
        "workspace": str(workspace),
        "review_folder": {
            "path": str(review_folder),
            "exists": review_folder.exists(),
            "files": get_candidate_files(review_folder, {".doc", ".docx"}),
        },
        "standard_folder": {
            "path": str(standard_folder),
            "exists": standard_folder.exists(),
            "files": get_candidate_files(standard_folder, {".xls", ".xlsx", ".xlsm"}),
        },
    }

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
