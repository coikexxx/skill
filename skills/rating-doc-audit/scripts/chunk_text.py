#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def detect_encoding(raw: bytes) -> str:
    if raw.startswith(b"\xff\xfe"):
        return "utf-16"
    if raw.startswith(b"\xfe\xff"):
        return "utf-16"
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    return "utf-8"


def main() -> int:
    parser = argparse.ArgumentParser(description="Split text into review chunks.")
    parser.add_argument("input_path")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--chunk-bytes", type=int, default=2_000_000)
    args = parser.parse_args()

    input_path = Path(args.input_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_head = input_path.read_bytes()[:4]
    encoding = detect_encoding(raw_head)

    manifest = {
        "source_path": str(input_path.resolve()),
        "encoding": encoding,
        "chunk_bytes": args.chunk_bytes,
        "chunks": [],
    }

    chunk_lines = []
    chunk_bytes = 0
    chunk_start_line = 1
    chunk_index = 1
    line_number = 0

    def flush() -> None:
        nonlocal chunk_lines, chunk_bytes, chunk_start_line, chunk_index
        if not chunk_lines:
            return
        chunk_name = f"chunk-{chunk_index:04d}.txt"
        chunk_path = out_dir / chunk_name
        content = "".join(chunk_lines)
        chunk_path.write_text(content, encoding="utf-8")
        manifest["chunks"].append(
            {
                "chunk_id": chunk_name.removesuffix(".txt"),
                "path": str(chunk_path.resolve()),
                "line_start": chunk_start_line,
                "line_end": chunk_start_line + len(chunk_lines) - 1,
                "byte_count": chunk_bytes,
            }
        )
        chunk_index += 1
        chunk_start_line += len(chunk_lines)
        chunk_lines = []
        chunk_bytes = 0

    with input_path.open("r", encoding=encoding, errors="replace", newline="") as handle:
        for line in handle:
            line_number += 1
            encoded = line.encode("utf-8")
            if chunk_lines and chunk_bytes + len(encoded) > args.chunk_bytes:
                flush()
            chunk_lines.append(line)
            chunk_bytes += len(encoded)

    flush()
    manifest["total_lines"] = line_number

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(manifest_path.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
