import json
import os
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "skills" / "rating-doc-audit" / "scripts"
LIST_WORKSPACE_FILES = SCRIPTS_DIR / "list_workspace_files.py"
EXPORT_DOCX_TEXT = SCRIPTS_DIR / "export_docx_text.py"
EXPORT_REVIEW_TEXT = SCRIPTS_DIR / "export_review_text.py"
PREPARE_STANDARD_WORKBOOK = SCRIPTS_DIR / "prepare_standard_workbook.py"
TEST_TMP_ROOT = ROOT / "tests" / ".tmp"

REVIEW_DIR_NAME = "\u8bc4\u7ea7\u5ba1\u6838\u6587\u4ef6"
STANDARD_DIR_NAME = "\u8bc4\u7ea7\u6807\u51c6\u6587\u4ef6"
FIRST_PARAGRAPH = "\u7b2c\u4e00\u6bb5"
SECOND_PARAGRAPH = "\u7b2c\u4e8c\u6bb5"
IMAGE_ANCHOR_PARAGRAPH = "\u62b5\u62bc\u7269\u622a\u56fe\u8bf4\u660e"
FOLLOW_UP_PARAGRAPH = "\u622a\u56fe\u4e0b\u65b9\u7eed\u5199"


def run_python_script(script: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def no_soffice_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PATH"] = ""
    env.pop("SOFFICE_PATH", None)
    return env


def fake_tesseract_env(helper_output: str) -> dict[str, str]:
    helper_path = TEST_TMP_ROOT / "fake_tesseract.py"
    helper_path.parent.mkdir(parents=True, exist_ok=True)
    helper_path.write_text(
        "import sys\n"
        f"sys.stdout.write({helper_output!r})\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["TESSERACT_PATH"] = sys.executable
    env["PYTHONUTF8"] = "1"
    env["FAKE_TESSERACT_HELPER"] = str(helper_path.resolve())
    return env


def write_minimal_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8"?>
            <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
              <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
              <Default Extension="xml" ContentType="application/xml"/>
              <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
            </Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
              <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
            </Relationships>""",
        )
        archive.writestr(
            "word/document.xml",
            f"""<?xml version="1.0" encoding="UTF-8"?>
            <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
              <w:body>
                <w:p><w:r><w:t>{FIRST_PARAGRAPH}</w:t></w:r></w:p>
                <w:p><w:r><w:t>{SECOND_PARAGRAPH}</w:t></w:r></w:p>
              </w:body>
            </w:document>""",
        )


def write_docx_with_inline_image(path: Path) -> None:
    image_bytes = (
        b"\x89PNG\r\n\x1a\n"
        b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
        b"\x00\x00\x00\x0cIDAT\x08\x99c\xf8\xff\xff?\x00\x05\xfe\x02\xfeA\xa5\x1f\x9b"
        b"\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8"?>
            <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
              <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
              <Default Extension="xml" ContentType="application/xml"/>
              <Default Extension="png" ContentType="image/png"/>
              <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
            </Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
              <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
            </Relationships>""",
        )
        archive.writestr(
            "word/_rels/document.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
              <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
            </Relationships>""",
        )
        archive.writestr(
            "word/document.xml",
            f"""<?xml version="1.0" encoding="UTF-8"?>
            <w:document
              xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
              xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
              xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
              xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <w:body>
                <w:p><w:r><w:t>{IMAGE_ANCHOR_PARAGRAPH}</w:t></w:r></w:p>
                <w:p>
                  <w:r>
                    <w:drawing>
                      <wp:inline>
                        <a:graphic>
                          <a:graphicData>
                            <pic:pic>
                              <pic:blipFill>
                                <a:blip r:embed="rIdImage1"/>
                              </pic:blipFill>
                            </pic:pic>
                          </a:graphicData>
                        </a:graphic>
                      </wp:inline>
                    </w:drawing>
                  </w:r>
                </w:p>
                <w:p><w:r><w:t>{FOLLOW_UP_PARAGRAPH}</w:t></w:r></w:p>
              </w:body>
            </w:document>""",
        )
        archive.writestr("word/media/image1.png", image_bytes)


class RatingDocAuditPortabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = TEST_TMP_ROOT / self._testMethodName
        if self.test_dir.exists():
            for path in sorted(self.test_dir.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink()
                else:
                    path.rmdir()
            self.test_dir.rmdir()
        self.test_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        if self.test_dir.exists():
            for path in sorted(self.test_dir.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink()
                else:
                    path.rmdir()
            self.test_dir.rmdir()

    def test_list_workspace_files_scans_required_folders(self) -> None:
        workspace = self.test_dir
        review_dir = workspace / REVIEW_DIR_NAME
        standard_dir = workspace / STANDARD_DIR_NAME
        review_dir.mkdir()
        standard_dir.mkdir()

        (review_dir / "sample.docx").write_text("placeholder", encoding="utf-8")
        (standard_dir / "standard.xlsx").write_text("placeholder", encoding="utf-8")

        result = run_python_script(LIST_WORKSPACE_FILES, str(workspace))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["review_folder"]["exists"])
        self.assertTrue(payload["standard_folder"]["exists"])
        self.assertEqual(payload["review_folder"]["files"][0]["name"], "sample.docx")
        self.assertEqual(payload["standard_folder"]["files"][0]["name"], "standard.xlsx")

    def test_list_workspace_files_help_works(self) -> None:
        result = run_python_script(LIST_WORKSPACE_FILES, "--help")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("usage:", result.stdout)

    def test_export_docx_text_extracts_paragraph_text(self) -> None:
        docx_path = self.test_dir / "sample.docx"
        output_path = self.test_dir / "sample.txt"
        write_minimal_docx(docx_path)

        result = run_python_script(EXPORT_DOCX_TEXT, str(docx_path), str(output_path))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        exported = output_path.read_text(encoding="utf-8")
        self.assertIn(FIRST_PARAGRAPH, exported)
        self.assertIn(SECOND_PARAGRAPH, exported)

    def test_export_docx_text_includes_image_anchor_and_ocr_status(self) -> None:
        docx_path = self.test_dir / "image-bound.docx"
        output_path = self.test_dir / "image-bound.txt"
        write_docx_with_inline_image(docx_path)

        result = run_python_script(EXPORT_DOCX_TEXT, str(docx_path), str(output_path), env=no_soffice_env())

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        exported = output_path.read_text(encoding="utf-8")
        self.assertIn(IMAGE_ANCHOR_PARAGRAPH, exported)
        self.assertIn(FOLLOW_UP_PARAGRAPH, exported)
        self.assertIn("[image-001]", exported)
        self.assertIn("anchor_previous", exported)
        self.assertIn("ocr_status: skipped", exported)

    def test_export_docx_text_reports_empty_ocr_explicitly(self) -> None:
        docx_path = self.test_dir / "image-empty-ocr.docx"
        output_path = self.test_dir / "image-empty-ocr.txt"
        write_docx_with_inline_image(docx_path)

        helper = self.test_dir / "fake_tesseract.py"
        helper.write_text("import sys\nsys.stdout.write('')\n", encoding="utf-8")
        env = os.environ.copy()
        env["TESSERACT_PATH"] = sys.executable
        env["FAKE_TESSERACT_HELPER"] = str(helper.resolve())

        result = run_python_script(EXPORT_DOCX_TEXT, str(docx_path), str(output_path), env=env)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        exported = output_path.read_text(encoding="utf-8")
        self.assertIn("ocr_status: empty", exported)
        self.assertIn("ocr_text:", exported)
        self.assertIn("ocr_note:", exported)

    def test_export_review_text_uses_python_for_docx_without_soffice(self) -> None:
        docx_path = self.test_dir / "review.docx"
        output_path = self.test_dir / "review.txt"
        write_minimal_docx(docx_path)

        result = run_python_script(EXPORT_REVIEW_TEXT, str(docx_path), str(output_path), env=no_soffice_env())

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["method"], "python-docx-xml")
        exported = output_path.read_text(encoding="utf-8")
        self.assertIn(FIRST_PARAGRAPH, exported)

    def test_export_review_text_blocks_doc_without_soffice(self) -> None:
        doc_path = self.test_dir / "legacy.doc"
        output_path = self.test_dir / "legacy.txt"
        doc_path.write_bytes(b"legacy-doc-placeholder")

        result = run_python_script(EXPORT_REVIEW_TEXT, str(doc_path), str(output_path), env=no_soffice_env())

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires soffice", result.stderr)

    def test_prepare_standard_workbook_keeps_xlsx_without_soffice(self) -> None:
        workbook_path = self.test_dir / "standard.xlsx"
        workbook_path.write_text("placeholder", encoding="utf-8")

        result = run_python_script(PREPARE_STANDARD_WORKBOOK, str(workbook_path), env=no_soffice_env())

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["method"], "direct")
        self.assertEqual(Path(payload["workbook_path"]), workbook_path.resolve())

    def test_prepare_standard_workbook_blocks_xls_without_soffice(self) -> None:
        workbook_path = self.test_dir / "legacy.xls"
        workbook_path.write_bytes(b"legacy-xls-placeholder")

        result = run_python_script(PREPARE_STANDARD_WORKBOOK, str(workbook_path), env=no_soffice_env())

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires soffice", result.stderr)


if __name__ == "__main__":
    unittest.main()
