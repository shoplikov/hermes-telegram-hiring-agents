#!/usr/bin/env python3
"""Deterministic storage for the user's latest CV (Job War Room, cv-analyst agent).

store: extract text -> skip if same sha256 -> rotate current.md into history -> write new current.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

TEXT_EXT = {".md", ".txt"}
SUPPORTED = TEXT_EXT | {".pdf", ".docx"}


def default_root() -> Path:
    home = os.environ.get("HERMES_HOME")
    base = Path(home) if home else Path.home() / ".hermes" / "profiles" / "cv-analyst"
    return base / "cv"


def extract_text(src: Path) -> str:
    ext = src.suffix.lower()
    if ext in TEXT_EXT:
        return src.read_text(errors="replace")
    if ext == ".pdf":
        out = subprocess.run(["pdftotext", "-layout", str(src), "-"],
                             capture_output=True, text=True, check=True)
        return out.stdout
    if ext == ".docx":
        ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        with zipfile.ZipFile(src) as z:
            root = ElementTree.fromstring(z.read("word/document.xml"))
        paras = ("".join(t.text or "" for t in p.iter(f"{ns}t")) for p in root.iter(f"{ns}p"))
        return "\n".join(paras)
    raise ValueError(f"unsupported file type {ext}; send PDF, DOCX, MD or TXT")


def _meta(root: Path) -> dict | None:
    f = root / "current.meta.json"
    return json.loads(f.read_text()) if f.exists() else None


def _error(message: str) -> dict:
    return {"status": "error", "version": None, "previous_version": None, "path": None,
            "message": message}


def store(src: Path, root: Path, now: datetime | None = None) -> dict:
    now = now or datetime.now()
    try:
        text = extract_text(src)
    except (ValueError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile, KeyError,
            ElementTree.ParseError) as e:
        return _error(f"could not read file: {e}")
    if not text.strip():
        return _error("could not extract text (scanned/image PDF?); send a text-based PDF or DOCX")
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    text_sha = hashlib.sha256(text.strip().encode()).hexdigest()
    meta = _meta(root)
    cur = root / "current.md"
    # Same file bytes, or a re-export with identical text, is the same CV.
    if meta and (meta["sha256"] == sha or meta.get("text_sha256") == text_sha):
        return {"status": "unchanged", "version": meta["version"],
                "previous_version": meta["version"], "path": str(cur),
                "message": f"same CV as v{meta['version']}, nothing changed"}
    root.mkdir(parents=True, exist_ok=True)
    prev = meta["version"] if meta else None
    if prev is not None and cur.exists():
        (root / "history").mkdir(exist_ok=True)
        cur.replace(root / "history" / f"v{prev}.md")
    version = (prev or 0) + 1
    stamp = now.isoformat(timespec="seconds")
    header = f"<!-- version: {version} | uploaded_at: {stamp} | original_filename: {src.name} -->\n"
    cur.write_text(header + text.strip() + "\n")
    new_meta = {"version": version, "uploaded_at": stamp, "sha256": sha,
                "text_sha256": text_sha, "original_filename": src.name}
    (root / "current.meta.json").write_text(json.dumps(new_meta, indent=2))
    return {"status": "stored", "version": version, "previous_version": prev, "path": str(cur),
            "message": f"stored CV v{version}"}


def show(root: Path) -> dict:
    meta = _meta(root)
    if not meta:
        return {"status": "error", "message": "no CV stored"}
    return {"version": meta["version"], "uploaded_at": meta["uploaded_at"],
            "original_filename": meta["original_filename"], "path": str(root / "current.md")}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("store")
    s.add_argument("file", type=Path)
    sh = sub.add_parser("show")
    for p in (s, sh):
        p.add_argument("--root", type=Path, default=None)
    a = ap.parse_args(argv)
    root = a.root or default_root()
    r = store(a.file, root) if a.cmd == "store" else show(root)
    print(json.dumps(r, ensure_ascii=False))
    return 2 if r.get("status") == "error" else 0


if __name__ == "__main__":
    sys.exit(main())
