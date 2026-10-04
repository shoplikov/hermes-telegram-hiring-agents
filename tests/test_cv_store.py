import json
import shutil
from datetime import datetime
from pathlib import Path

import pytest

import cv_store


def write(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text)
    return p


def cv(tag: str) -> str:
    """Realistic-length CV text (cv_store refuses near-empty extractions)."""
    return f"{tag} CV. ML Engineer, Astana. " + "Built production RAG and agent systems in Python. " * 6


T1 = datetime(2026, 10, 1, 12, 0, 0)
T2 = datetime(2026, 10, 2, 12, 0, 0)


def test_first_upload_creates_v1(tmp_path):
    root = tmp_path / "cv"
    src = write(tmp_path, "cv.md", "# Alisher\n" + cv("ML Engineer"))
    r = cv_store.store(src, root, now=T1)
    assert r["status"] == "stored" and r["version"] == 1 and r["previous_version"] is None
    cur = (root / "current.md").read_text()
    assert "version: 1" in cur and "ML Engineer" in cur
    meta = json.loads((root / "current.meta.json").read_text())
    assert meta["version"] == 1 and meta["original_filename"] == "cv.md"


def test_same_content_different_name_is_unchanged(tmp_path):
    root = tmp_path / "cv"
    cv_store.store(write(tmp_path, "a.md", cv("same")), root, now=T1)
    r = cv_store.store(write(tmp_path, "b.md", cv("same")), root, now=T2)
    assert r["status"] == "unchanged" and r["version"] == 1
    assert not (root / "history").exists() or not any((root / "history").iterdir())


def test_new_content_rotates_history(tmp_path):
    root = tmp_path / "cv"
    cv_store.store(write(tmp_path, "a.md", cv("old")), root, now=T1)
    r = cv_store.store(write(tmp_path, "b.md", cv("new")), root, now=T2)
    assert r["status"] == "stored" and r["version"] == 2 and r["previous_version"] == 1
    assert "old CV" in (root / "history" / "v1.md").read_text()
    assert "new CV" in (root / "current.md").read_text()


def test_empty_extraction_does_not_overwrite(tmp_path):
    root = tmp_path / "cv"
    cv_store.store(write(tmp_path, "a.md", cv("good")), root, now=T1)
    r = cv_store.store(write(tmp_path, "scan.md", "   \n  "), root, now=T2)
    assert r["status"] == "error" and "extract" in r["message"]
    assert "good CV" in (root / "current.md").read_text()
    assert json.loads((root / "current.meta.json").read_text())["version"] == 1


def test_show_without_cv_is_error(tmp_path):
    assert cv_store.show(tmp_path / "cv")["status"] == "error"


def test_show_reports_current(tmp_path):
    root = tmp_path / "cv"
    cv_store.store(write(tmp_path, "a.md", cv("x")), root, now=T1)
    s = cv_store.show(root)
    assert s["version"] == 1 and s["path"].endswith("current.md")


def test_unsupported_extension_is_error(tmp_path):
    r = cv_store.store(write(tmp_path, "cv.exe", "x"), tmp_path / "cv", now=T1)
    assert r["status"] == "error"


MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 300 100]/Contents 4 0 R"
    b"/Resources<</Font<</F1 5 0 R>>>>>>endobj\n"
    b"4 0 obj<</Length 38>>stream\nBT /F1 18 Tf 20 40 Td (Hello CV) Tj ET\nendstream endobj\n"
    b"5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)


def test_pdf_extraction(tmp_path):
    if not shutil.which("pdftotext"):
        pytest.skip("no pdftotext")
    pdf = tmp_path / "cv.pdf"
    pdf.write_bytes(MINIMAL_PDF)
    assert "Hello CV" in cv_store.extract_text(pdf)


def test_docx_extraction(tmp_path):
    import zipfile
    docx = tmp_path / "cv.docx"
    ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    xml = f'<w:document {ns}><w:body><w:p><w:r><w:t>Senior </w:t></w:r><w:r><w:t>Engineer</w:t></w:r></w:p><w:p><w:r><w:t>Almaty</w:t></w:r></w:p></w:body></w:document>'
    with zipfile.ZipFile(docx, "w") as z:
        z.writestr("word/document.xml", xml)
    assert cv_store.extract_text(docx) == "Senior Engineer\nAlmaty"


def test_tiny_text_layer_is_refused(tmp_path):
    # A scanned PDF often carries only a page number or watermark as text.
    root = tmp_path / "cv"
    good = "ML Engineer at Example LLC, 2024-2026. Built RAG systems with Python and PyTorch. " * 3
    cv_store.store(write(tmp_path, "a.md", good), root, now=T1)
    r = cv_store.store(write(tmp_path, "scan.md", "Page 1"), root, now=T2)
    assert r["status"] == "error" and "extract" in r["message"]
    assert "Example LLC" in (root / "current.md").read_text()


def test_image_only_pdf_is_refused(tmp_path):
    if not shutil.which("pdftotext"):
        pytest.skip("no pdftotext")
    pdf = tmp_path / "scan.pdf"
    pdf.write_bytes(MINIMAL_PDF.replace(b"(Hello CV) Tj", b""))
    r = cv_store.store(pdf, tmp_path / "cv", now=T1)
    assert r["status"] == "error"
