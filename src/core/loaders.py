"""Document loaders for every supported source type."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Optional

from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain_core.documents import Document


def _attach_metadata(docs: Iterable[Document], path: Path) -> List[Document]:
    out: List[Document] = []
    for d in docs:
        d.metadata.setdefault("filename", path.name)
        d.metadata.setdefault("source_path", str(path))
        out.append(d)
    return out


def load_pdf_single(path: Path) -> List[Document]:
    """Load a single PDF and tag every page with filename / source_path."""
    return _attach_metadata(PyPDFLoader(str(path)).load(), path)


def load_pdfs_from_folder(
    folder: Path,
    filenames: Optional[List[str]] = None,
) -> List[Document]:
    """
    Load every (or a selected subset of) PDF in ``folder``.

    ``filenames`` is an optional whitelist of filenames (not paths) to load.
    """
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    pdfs = sorted(folder.glob("*.pdf"))
    if filenames:
        keep = set(filenames)
        pdfs = [p for p in pdfs if p.name in keep]

    if not pdfs:
        raise ValueError(f"No PDF files found in: {folder}")

    docs: List[Document] = []
    for pdf in pdfs:
        docs.extend(load_pdf_single(pdf))
    return docs


def load_txts_from_folder(
    folder: Path,
    filenames: Optional[List[str]] = None,
) -> List[Document]:
    """Load every (or a selected subset of) `.txt` file in ``folder``."""
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    files = sorted(folder.glob("*.txt"))
    if filenames:
        keep = set(filenames)
        files = [f for f in files if f.name in keep]

    if not files:
        raise ValueError(f"No .txt files found in: {folder}")

    docs: List[Document] = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        if not text.strip():
            continue
        docs.append(
            Document(
                page_content=text,
                metadata={"filename": f.name, "source_path": str(f)},
            )
        )
    return docs


def load_csv(path: Path) -> List[Document]:
    """Load a CSV with one Document per row."""
    return _attach_metadata(CSVLoader(file_path=str(path)).load(), path)


def load_files_dispatch(paths: List[Path]) -> List[Document]:
    """
    Convenience: load a heterogeneous list of files by extension.

    Used after an upload picks files of mixed type.
    """
    docs: List[Document] = []
    for p in paths:
        suffix = p.suffix.lower()
        if suffix == ".pdf":
            docs.extend(load_pdf_single(p))
        elif suffix == ".txt":
            text = p.read_text(encoding="utf-8", errors="ignore")
            if text.strip():
                docs.append(
                    Document(
                        page_content=text,
                        metadata={"filename": p.name, "source_path": str(p)},
                    )
                )
        elif suffix == ".csv":
            docs.extend(load_csv(p))
        else:
            raise ValueError(f"Unsupported file type: {p.suffix} ({p.name})")
    return docs


_SANITIZE_RE = re.compile(r"[^a-zA-Z0-9_-]+")


def sanitize_for_collection(name: str) -> str:
    """
    Make an arbitrary filename safe to use in a Chroma collection name
    and as a directory component.
    """
    stem = Path(name).stem
    cleaned = _SANITIZE_RE.sub("_", stem).strip("_").lower()
    return cleaned or "upload"


def save_uploaded_file(uploaded_file, destination_folder: Path) -> Path:
    """
    Persist a Streamlit ``UploadedFile`` to disk and return the saved Path.

    Streamlit is intentionally not imported here so this module stays usable
    outside the app; ``uploaded_file`` only needs ``.name`` and ``.getbuffer()``.
    """
    destination_folder.mkdir(parents=True, exist_ok=True)
    target = destination_folder / uploaded_file.name
    with open(target, "wb") as fh:
        fh.write(uploaded_file.getbuffer())
    return target
