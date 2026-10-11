#!/usr/bin/env python3
from __future__ import annotations

import csv
import fnmatch
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import time
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET

INTERNAL_WORKSPACE = "_catalog"
DEFAULT_IGNORE_DIRS = {INTERNAL_WORKSPACE, ".git", "__pycache__"}
DEFAULT_IGNORE_PATTERNS = ["*/.git/*", "*/__pycache__/*", f"{INTERNAL_WORKSPACE}/*", "_catalog*/*"]

TEXT_EXTENSIONS = {
    "txt",
    "md",
    "markdown",
    "py",
    "js",
    "ts",
    "tsx",
    "jsx",
    "json",
    "yaml",
    "yml",
    "toml",
    "ini",
    "cfg",
    "conf",
    "csv",
    "tsv",
    "xml",
    "html",
    "css",
    "sql",
    "java",
    "go",
    "rs",
    "c",
    "cpp",
    "h",
    "sh",
    "zsh",
    "log",
}
DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx", "rtf"}
SPREADSHEET_EXTENSIONS = {"xlsx", "xls", "csv", "tsv"}
IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "heic", "tif", "tiff"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "m4v", "flv", "mpg", "mpeg", "wmv"}
AUDIO_EXTENSIONS = {"mp3", "wav", "m4a", "aac", "flac", "ogg", "amr"}
ARCHIVE_EXTENSIONS = {"zip", "7z", "rar", "tar", "gz", "bz2", "xz"}
CODE_EXTENSIONS = {"py", "js", "ts", "tsx", "jsx", "java", "go", "rs", "c", "cpp", "h", "sh", "sql"}

JUNK_FILE_NAMES = {".DS_Store", "Thumbs.db", "Desktop.ini"}
JUNK_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
JUNK_DIR_SEGMENTS = {"cache", "caches", "temp", "tmp", "logs"}
RESIDUAL_DIR_SEGMENTS = {"build", "dist", "target"}

PROJECT_KEYWORDS = {
    "project",
    "proposal",
    "spec",
    "roadmap",
    "deliverable",
    "milestone",
    "sprint",
    "issue",
    "ticket",
    "todo",
    "任务",
    "项目",
    "方案",
    "计划",
    "交付",
    "需求",
    "迭代",
}
AREA_KEYWORDS = {
    "finance",
    "health",
    "family",
    "home",
    "career",
    "legal",
    "invoice",
    "receipt",
    "育儿",
    "健康",
    "家庭",
    "证件",
    "发票",
    "体检",
    "合同",
    "履历",
}
RESOURCE_KEYWORDS = {
    "manual",
    "guide",
    "ebook",
    "tutorial",
    "reference",
    "notes",
    "course",
    "article",
    "template",
    "资料",
    "教程",
    "说明书",
    "电子书",
    "学习",
    "素材",
    "论文",
    "手册",
}
ARCHIVE_KEYWORDS = {
    "archive",
    "backup",
    "snapshot",
    "history",
    "restore",
    "export",
    "old",
    "legacy",
    "归档",
    "备份",
    "历史",
    "恢复",
    "导出",
    "旧",
    "存档",
}
SENSITIVE_HIGH_KEYWORDS = {
    "身份证",
    "护照",
    "发票",
    "体检",
    "病历",
    "合同",
    "invoice",
    "passport",
    "id card",
}
SENSITIVE_MEDIUM_KEYWORDS = {
    "family",
    "育儿",
    "健康",
    "resume",
    "履历",
    "财务",
}
GENERIC_KEYWORDS = {
    "files",
    "file",
    "data",
    "document",
    "documents",
    "folder",
    "资料",
    "文件",
    "文档",
    "未分类",
    "misc",
    "other",
    "stuff",
}
PROJECT_NEGATIVE_KEYWORDS = {
    "manual",
    "guide",
    "ebook",
    "book",
    "tutorial",
    "reference",
    "report",
    "research",
    "analysis",
    "stock",
    "证券",
    "研报",
    "年报",
    "招股说明书",
    "交割单",
    "说明书",
    "电子书",
    "教程",
    "攻略",
    "图片",
    "相片",
    "照片",
    "备份",
    "归档",
    "archive",
    "backup",
    "snapshot",
    "重复",
    "duplicate",
    "发票",
    "invoice",
}
FINANCE_RESEARCH_KEYWORDS = {
    "stock",
    "stocks",
    "证券",
    "研报",
    "行业",
    "招股说明书",
    "年报",
    "交割单",
    "个股",
    "投资",
    "券商",
    "估值",
    "财报",
    "白皮书",
}
GENERIC_MEDIA_NAME_RE = re.compile(
    r"(?i)^("
    r"img[_-]?\d+"
    r"|dscf?\d+"
    r"|dpp[_-]?\d+"
    r"|_mg[_-]?\d+"
    r"|p\d{4,}"
    r"|sdc\d+"
    r"|video\d+"
    r"|mmexport\d+"
    r"|weixin.*\d+"
    r"|wx_camera.*\d+"
    r"|screenshot.*\d*"
    r"|screen shot.*\d*"
    r"|\d{4}[-_ ]\d{2}[-_ ]\d{2}.*"
    r"|[0-9a-f]{24,}"
    r"|[0-9a-f]{8,}_[0-9a-f]{8,}"
    r")$"
)
CODED_CATEGORY_RE = re.compile(r"^\d{2}[-_].+")
DISPLAY_TO_LOGICAL = {
    "Projects": "projects",
    "Areas": "areas",
    "Resources": "resources",
    "Archives": "archives",
}


@dataclass(frozen=True)
class CatalogPaths:
    root: Path
    catalog_dir: Path
    metadata_dir: Path
    stats_dir: Path
    duplicates_dir: Path
    semantic_dir: Path
    review_dir: Path
    plans_dir: Path
    work_dir: Path
    tools_dir: Path
    app_dir: Path
    backups_dir: Path
    db_path: Path
    profile_path: Path
    manifest_path: Path
    tree_path: Path


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


def resolve_root(root_arg: str | None) -> Path:
    target = Path(root_arg or ".").expanduser().resolve()
    if not target.exists() or not target.is_dir():
        raise SystemExit(f"Workspace root does not exist or is not a directory: {target}")
    return target


def paths_for(root: Path) -> CatalogPaths:
    catalog_dir = root / INTERNAL_WORKSPACE
    metadata_dir = catalog_dir / "metadata"
    return CatalogPaths(
        root=root,
        catalog_dir=catalog_dir,
        metadata_dir=metadata_dir,
        stats_dir=metadata_dir / "stats",
        duplicates_dir=metadata_dir / "duplicates",
        semantic_dir=metadata_dir / "semantic",
        review_dir=metadata_dir / "review",
        plans_dir=metadata_dir / "plans",
        work_dir=metadata_dir / "_work",
        tools_dir=catalog_dir / "tools",
        app_dir=catalog_dir / "app",
        backups_dir=catalog_dir / "backups",
        db_path=metadata_dir / "_work" / "catalog.sqlite3",
        profile_path=metadata_dir / "profile.json",
        manifest_path=metadata_dir / "manifest.json",
        tree_path=metadata_dir / "tree.json",
    )


def ensure_workspace(paths: CatalogPaths) -> None:
    for directory in (
        paths.catalog_dir,
        paths.metadata_dir,
        paths.stats_dir,
        paths.duplicates_dir,
        paths.semantic_dir,
        paths.review_dir,
        paths.plans_dir,
        paths.work_dir,
        paths.tools_dir,
        paths.app_dir,
        paths.backups_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)


def default_profile(root: Path) -> dict[str, Any]:
    return {
        "version": 1,
        "workspace_root": str(root),
        "organization_mode": "para",
        "bucket_names": {
            "projects": "Projects",
            "areas": "Areas",
            "resources": "Resources",
            "archives": "Archives",
            "to_delete": "ToDelete",
            "unsorted": "Resources/Unsorted",
            "conflicts": "Resources/Unsorted/Conflicts",
            "snapshots": "Archives/Snapshots",
        },
        "ignore_dirs": sorted(DEFAULT_IGNORE_DIRS),
        "ignore_patterns": list(DEFAULT_IGNORE_PATTERNS),
        "junk_rules": {
            "file_names": sorted(JUNK_FILE_NAMES),
            "dir_names": sorted(JUNK_DIR_NAMES),
            "dir_segments": sorted(JUNK_DIR_SEGMENTS),
            "residual_segments": sorted(RESIDUAL_DIR_SEGMENTS),
        },
        "tag_rules": {
            "project_keywords": sorted(PROJECT_KEYWORDS),
            "area_keywords": sorted(AREA_KEYWORDS),
            "resource_keywords": sorted(RESOURCE_KEYWORDS),
            "archive_keywords": sorted(ARCHIVE_KEYWORDS),
        },
        "ocr_mode": "online",
        "safety_policy": {
            "require_plan_before_execution": True,
            "require_confirmation_before_execution": True,
            "delete_defaults_to_quarantine": True,
            "never_treat_catalog_as_user_content": True,
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_profile(paths: CatalogPaths) -> dict[str, Any]:
    ensure_workspace(paths)
    if not paths.profile_path.exists():
        profile = default_profile(paths.root)
        write_json(paths.profile_path, profile)
        return profile
    profile = read_json(paths.profile_path, {})
    if not isinstance(profile, dict):
        profile = default_profile(paths.root)
    profile.setdefault("workspace_root", str(paths.root))
    profile.setdefault("organization_mode", "para")
    profile.setdefault("bucket_names", default_profile(paths.root)["bucket_names"])
    profile.setdefault("ignore_dirs", sorted(DEFAULT_IGNORE_DIRS))
    profile.setdefault("ignore_patterns", list(DEFAULT_IGNORE_PATTERNS))
    profile.setdefault("junk_rules", default_profile(paths.root)["junk_rules"])
    profile.setdefault("tag_rules", default_profile(paths.root)["tag_rules"])
    profile.setdefault("ocr_mode", "online")
    profile.setdefault("safety_policy", default_profile(paths.root)["safety_policy"])
    write_json(paths.profile_path, profile)
    return profile


def connect_db(paths: CatalogPaths) -> sqlite3.Connection:
    ensure_workspace(paths)
    conn = sqlite3.connect(paths.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;

        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dirs (
            rel_path TEXT PRIMARY KEY,
            parent_rel_path TEXT,
            name TEXT NOT NULL,
            depth INTEGER NOT NULL,
            top_dir TEXT NOT NULL,
            direct_dir_count INTEGER NOT NULL,
            direct_file_count INTEGER NOT NULL,
            total_file_count INTEGER NOT NULL,
            total_size INTEGER NOT NULL,
            dominant_bucket TEXT,
            dominant_topic TEXT,
            bucket_distribution_json TEXT,
            cohesion_score REAL,
            split_need_score REAL,
            structure_value_score REAL,
            granularity_decision TEXT,
            granularity_confidence REAL,
            summary TEXT,
            flags_json TEXT
        );

        CREATE TABLE IF NOT EXISTS files (
            rel_path TEXT PRIMARY KEY,
            dir_rel_path TEXT NOT NULL,
            name TEXT NOT NULL,
            stem TEXT NOT NULL,
            ext TEXT NOT NULL,
            size INTEGER NOT NULL,
            mtime REAL NOT NULL,
            depth INTEGER NOT NULL,
            top_dir TEXT NOT NULL,
            head_hash TEXT,
            full_hash TEXT,
            excerpt TEXT,
            content_status TEXT,
            keyword_text TEXT,
            tags_json TEXT,
            para_scores_json TEXT,
            dominant_bucket TEXT,
            classification_confidence REAL,
            reasons_json TEXT,
            flags_json TEXT,
            sensitivity TEXT,
            is_junk INTEGER NOT NULL DEFAULT 0,
            junk_reasons_json TEXT,
            duplicate_name_with_ext_group TEXT,
            duplicate_name_ignore_ext_group TEXT,
            exact_duplicate_group TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_files_dir ON files(dir_rel_path);
        CREATE INDEX IF NOT EXISTS idx_files_ext ON files(ext);
        CREATE INDEX IF NOT EXISTS idx_files_size ON files(size);
        CREATE INDEX IF NOT EXISTS idx_files_bucket ON files(dominant_bucket);
        CREATE INDEX IF NOT EXISTS idx_dirs_parent ON dirs(parent_rel_path);
        """
    )


def reset_inventory(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM dirs")
    conn.execute("DELETE FROM files")
    conn.execute("DELETE FROM meta")
    conn.commit()


def normalize_ext(name: str) -> str:
    ext = Path(name).suffix.lower().lstrip(".")
    return ext or "[no_ext]"


def infer_form(ext: str) -> str:
    if ext in CODE_EXTENSIONS:
        return "code"
    if ext in TEXT_EXTENSIONS:
        return "text"
    if ext in DOCUMENT_EXTENSIONS:
        return "document"
    if ext in SPREADSHEET_EXTENSIONS:
        return "spreadsheet"
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    if ext in ARCHIVE_EXTENSIONS:
        return "archive"
    if ext in {"app", "exe", "dmg", "pkg"}:
        return "software"
    return "file"


def first_component(rel_path: str) -> str:
    if not rel_path:
        return "[root]"
    return rel_path.split("/", 1)[0]


def join_rel(parent: str, name: str) -> str:
    return name if not parent else f"{parent}/{name}"


def parent_rel(rel_path: str) -> str | None:
    if not rel_path:
        return None
    if "/" not in rel_path:
        return ""
    return rel_path.rsplit("/", 1)[0]


def ancestors_for_dir(dir_rel_path: str) -> list[str]:
    if dir_rel_path == "":
        return [""]
    parts = dir_rel_path.split("/")
    output = [""]
    for index in range(1, len(parts) + 1):
        output.append("/".join(parts[:index]))
    return output


def rel_from_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def safe_path_component(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "-", value).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip(" .")
    return cleaned or "Untitled"


def flattened_source_fragment(rel_path: str) -> str:
    return re.sub(r"[/]+", "__", rel_path).strip("_") or "root"


def looks_like_coded_category(name: str) -> bool:
    return bool(CODED_CATEGORY_RE.match(name.strip()))


def looks_like_generic_media_name(name: str) -> bool:
    lowered = name.strip().lower()
    if not lowered:
        return False
    if GENERIC_MEDIA_NAME_RE.match(lowered):
        return True
    if lowered.isdigit() and len(lowered) >= 2:
        return True
    return False


def is_internal_catalog_path(rel_path: str, name: str | None = None) -> bool:
    if name and name.startswith("_catalog"):
        return True
    if rel_path == INTERNAL_WORKSPACE or rel_path.startswith(f"{INTERNAL_WORKSPACE}/"):
        return True
    parts = [part for part in rel_path.split("/") if part]
    return any(part.startswith("_catalog") for part in parts)


def should_skip_dir(rel_path: str, name: str, profile: dict[str, Any]) -> bool:
    if is_internal_catalog_path(rel_path, name):
        return True
    ignore_dirs = set(profile.get("ignore_dirs") or [])
    if name in ignore_dirs:
        return True
    for pattern in profile.get("ignore_patterns") or []:
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(name, pattern):
            return True
    return False


def should_skip_file(rel_path: str, name: str, profile: dict[str, Any]) -> bool:
    if is_internal_catalog_path(rel_path, name):
        return True
    for pattern in profile.get("ignore_patterns") or []:
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(name, pattern):
            return True
    return False


def detect_junk(rel_path: str, name: str, ext: str, is_dir: bool = False) -> list[str]:
    lowered = rel_path.lower()
    reasons: list[str] = []
    if not is_dir and name in JUNK_FILE_NAMES:
        reasons.append("system_junk")
    if is_dir and name in JUNK_DIR_NAMES:
        reasons.append("generated_cache_dir")
    if is_dir and name.lower() in JUNK_DIR_SEGMENTS:
        reasons.append("cache_like_dir")
    if is_dir and name.lower() in RESIDUAL_DIR_SEGMENTS:
        reasons.append("build_output_dir")
    if "wechat files" in lowered or "tencent files" in lowered:
        if any(segment in lowered for segment in ("/cache", "/temp", "/backup", "/offlinepackage")):
            reasons.append("chat_cache_candidate")
    if ext in {"tmp", "swp", "part", "crdownload"}:
        reasons.append("temporary_file")
    if re.search(r"\.(db_sqlite_notadb\d+|jpg_httpdltemp)$", lowered):
        reasons.append("odd_residual_suffix")
    return reasons


def human_size(size: int) -> str:
    if size < 1024:
        return f"{size}B"
    value = float(size)
    for unit in ("KB", "MB", "GB", "TB"):
        value /= 1024.0
        if value < 1024.0 or unit == "TB":
            return f"{value:.1f}{unit}"
    return f"{value:.1f}TB"


def text_from_bytes(raw: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def clean_snippet(value: str, limit: int = 220) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) > limit:
        return value[: limit - 1] + "…"
    return value


def read_text_excerpt(path: Path, ext: str) -> tuple[str | None, str]:
    try:
        if ext in TEXT_EXTENSIONS and ext not in {"csv", "tsv"}:
            raw = path.read_bytes()[:8192]
            return clean_snippet(text_from_bytes(raw)) or None, "text_excerpt"
        if ext in {"csv", "tsv"}:
            delimiter = "," if ext == "csv" else "\t"
            rows: list[str] = []
            with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
                reader = csv.reader(handle, delimiter=delimiter)
                for index, row in enumerate(reader):
                    compact = " | ".join(cell.strip() for cell in row[:6] if str(cell).strip())
                    if compact:
                        rows.append(compact)
                    if index >= 2:
                        break
            return clean_snippet(" ; ".join(rows)) or None, "table_preview"
        if ext == "docx":
            with zipfile.ZipFile(path) as archive:
                with archive.open("word/document.xml") as handle:
                    tree = ET.parse(handle)
            text = " ".join(node.text for node in tree.iter() if node.text)
            return clean_snippet(text) or None, "text_excerpt"
        if ext in {"doc", "rtf"}:
            result = subprocess.run(
                ["textutil", "-convert", "txt", "-stdout", str(path)],
                capture_output=True,
                check=False,
                timeout=20,
            )
            if result.stdout:
                return clean_snippet(text_from_bytes(result.stdout[:8192])) or None, "text_excerpt"
        if ext == "pdf":
            raw = path.read_bytes()[:512]
            if raw.startswith(b"%PDF"):
                return None, "metadata_only"
    except Exception:
        return None, "extract_failed"
    return None, "metadata_only"


def head_fingerprint(path: Path, chunk_size: int = 65536) -> str:
    digest = hashlib.sha256()
    size = path.stat().st_size
    with path.open("rb") as handle:
        digest.update(handle.read(chunk_size))
        if size > chunk_size:
            offset = max(size - chunk_size, 0)
            handle.seek(offset)
            digest.update(handle.read(chunk_size))
    return digest.hexdigest()


def full_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def extract_keywords(rel_path: str, excerpt: str | None = None) -> list[str]:
    candidates: list[str] = []
    lowered_rel = rel_path.replace("/", " ")
    for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9._+-]{1,}", lowered_rel):
        candidates.append(token.lower())
    for token in re.findall(r"[\u4e00-\u9fff]{2,}", lowered_rel):
        candidates.append(token)
    if excerpt:
        for token in re.findall(r"[A-Za-z][A-Za-z0-9+-]{2,}", excerpt):
            candidates.append(token.lower())
        for token in re.findall(r"[\u4e00-\u9fff]{2,}", excerpt):
            candidates.append(token)
    output: list[str] = []
    seen: set[str] = set()
    for token in candidates:
        token = token.strip("._- ")
        if not token or token in seen or token in GENERIC_KEYWORDS:
            continue
        seen.add(token)
        output.append(token)
        if len(output) >= 20:
            break
    return output


def infer_source(rel_path: str) -> str:
    lowered = rel_path.lower()
    if "wechat files" in lowered or "tencent files" in lowered or "微信" in rel_path:
        return "chat_export"
    if any(keyword in lowered for keyword in ("backup", "snapshot", "restore")) or any(
        keyword in rel_path for keyword in ("备份", "历史", "恢复", "归档")
    ):
        return "snapshot"
    if any(keyword in lowered for keyword in ("manual", "guide", "ebook", "course")) or any(
        keyword in rel_path for keyword in ("说明书", "教程", "电子书", "课程")
    ):
        return "reference"
    return "workspace"


def infer_sensitivity(rel_path: str, excerpt: str | None) -> str:
    text = f"{rel_path} {excerpt or ''}".lower()
    if any(keyword.lower() in text for keyword in SENSITIVE_HIGH_KEYWORDS):
        return "high"
    if any(keyword.lower() in text for keyword in SENSITIVE_MEDIUM_KEYWORDS):
        return "medium"
    return "low"


def contextual_topic_from_path(rel_path: str) -> str:
    path = Path(rel_path)
    parts = list(path.parts[:-1])
    for name in reversed(parts):
        cleaned = safe_path_component(name)
        lowered = cleaned.lower()
        if not cleaned or cleaned in {"文件", "文档"}:
            continue
        if cleaned == first_component(rel_path) and looks_like_coded_category(cleaned):
            continue
        if lowered in {"unsorted", "conflicts", "snapshots"}:
            continue
        if looks_like_generic_media_name(cleaned):
            continue
        return cleaned
    top = first_component(rel_path)
    if top and top != "[root]":
        return safe_path_component(top)
    return "Unsorted"


def topic_label_from_keywords(rel_path: str, keywords: list[str]) -> str:
    name = Path(rel_path).stem if Path(rel_path).suffix else Path(rel_path).name
    if looks_like_generic_media_name(name):
        return contextual_topic_from_path(rel_path)
    preferred = safe_path_component(name)
    if preferred and preferred.lower() not in {"untitled", "readme"} and preferred not in {"文件", "文档"}:
        return preferred
    for keyword in keywords:
        if keyword in GENERIC_KEYWORDS:
            continue
        return safe_path_component(keyword)
    return contextual_topic_from_path(rel_path)


def top_level_context_adjustments(rel_path: str) -> tuple[dict[str, float], list[str], list[str]]:
    top = first_component(rel_path)
    scores = {"Projects": 0.0, "Areas": 0.0, "Resources": 0.0, "Archives": 0.0}
    reasons: list[str] = []
    flags: list[str] = []
    if top == "[root]":
        return scores, reasons, flags

    top_lower = top.lower()
    if looks_like_coded_category(top):
        flags.append("coded_top_level_dir")

    if top_lower.startswith("10-") or any(keyword in top_lower for keyword in ("backup", "archive", "snapshot")):
        scores["Archives"] += 1.45
        scores["Projects"] -= 0.65
        reasons.append(f"top-level container {top} looks archival or staged")
        flags.append("top_level_archive_context")
    elif top_lower.startswith(("01-", "02-", "03-")):
        scores["Resources"] += 1.05
        scores["Projects"] -= 0.45
        reasons.append(f"top-level container {top} looks like a curated content library")
        flags.append("top_level_content_library")
    elif top_lower.startswith("09-"):
        scores["Areas"] += 0.85
        scores["Resources"] += 0.55
        scores["Projects"] -= 0.35
        reasons.append(f"top-level container {top} looks like a themed topic area")
        flags.append("top_level_topic_area")

    if any(keyword in top_lower for keyword in ("stock", "security", "broker")) or any(
        keyword in top for keyword in ("股票", "证券", "研报", "投资")
    ):
        scores["Areas"] += 0.55
        scores["Resources"] += 0.90
        scores["Projects"] -= 0.90
        reasons.append("finance or research context suppresses project classification")
        flags.append("finance_research_context")

    if any(keyword in top for keyword in ("说明书", "电子书", "教程", "攻略", "网图", "搞笑图")):
        scores["Resources"] += 0.70
        scores["Projects"] -= 0.35
    if any(keyword in top for keyword in ("发票", "票据", "体检", "育儿", "证件")):
        scores["Areas"] += 0.80
        scores["Resources"] += 0.20
        scores["Projects"] -= 0.30
    if any(keyword in top for keyword in ("备份", "归档", "待删除", "重复照片")):
        scores["Archives"] += 0.70
        scores["Projects"] -= 0.40

    return scores, reasons, flags


def score_para_bucket(
    rel_path: str,
    ext: str,
    excerpt: str | None,
    keywords: list[str],
    mtime: float,
    is_dir: bool,
    is_junk: bool,
) -> tuple[dict[str, float], str, float, list[str], list[str]]:
    text = f"{rel_path} {' '.join(keywords)} {excerpt or ''}".lower()
    form = infer_form(ext)
    scores = {"Projects": 0.2, "Areas": 0.2, "Resources": 0.2, "Archives": 0.2}
    reasons: list[str] = []
    flags: list[str] = []

    project_hits = 0
    project_negative_hits = 0
    for keyword in PROJECT_KEYWORDS:
        if keyword.lower() in text:
            scores["Projects"] += 0.55
            project_hits += 1
    for keyword in AREA_KEYWORDS:
        if keyword.lower() in text:
            scores["Areas"] += 1.0
    for keyword in RESOURCE_KEYWORDS:
        if keyword.lower() in text:
            scores["Resources"] += 1.0
    for keyword in ARCHIVE_KEYWORDS:
        if keyword.lower() in text:
            scores["Archives"] += 1.1
    for keyword in PROJECT_NEGATIVE_KEYWORDS:
        if keyword.lower() in text:
            project_negative_hits += 1
    if project_negative_hits:
        scores["Projects"] -= 0.35 * min(project_negative_hits, 3)
        reasons.append("reference, archive, or research signals reduce project likelihood")
    if any(keyword.lower() in text for keyword in FINANCE_RESEARCH_KEYWORDS):
        scores["Resources"] += 0.95
        scores["Areas"] += 0.35
        scores["Projects"] -= 0.85
        flags.append("finance_research")
        reasons.append("research-heavy content biases toward resources or areas")

    top_scores, top_reasons, top_flags = top_level_context_adjustments(rel_path)
    for bucket, delta in top_scores.items():
        scores[bucket] += delta
    reasons.extend(top_reasons)
    flags.extend(top_flags)

    if form in {"text", "document", "spreadsheet"}:
        scores["Resources"] += 0.4
    if form in {"archive"}:
        scores["Archives"] += 0.6
    if form in {"image", "video", "audio"}:
        scores["Projects"] -= 0.25
    if form in {"code"} and not is_dir:
        scores["Projects"] += 0.3
        scores["Areas"] += 0.3
    if infer_source(rel_path) == "snapshot":
        scores["Archives"] += 0.7
        flags.append("snapshot_like")
    if infer_source(rel_path) == "chat_export":
        scores["Archives"] += 0.4
        flags.append("chat_export")
    if is_junk:
        scores["Archives"] += 0.2
        flags.append("junk_candidate")

    age_days = max(0.0, (time.time() - mtime) / 86400.0)
    active_project = project_hits > 0 and project_negative_hits == 0 and not any(
        flag in flags for flag in ("snapshot_like", "chat_export", "top_level_archive_context", "finance_research_context")
    )
    if active_project and (age_days < 365 or form in {"code", "spreadsheet"}):
        scores["Projects"] += 0.45
        reasons.append("active project signals are present without archive or research context")
    elif project_hits > 0 and not active_project:
        scores["Projects"] -= 0.35
        reasons.append("project-like words exist, but surrounding context is not an active project")
    if age_days > 365:
        scores["Archives"] += 0.3
    if age_days < 90 and scores["Projects"] > scores["Archives"]:
        scores["Projects"] += 0.2

    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    dominant_bucket, top_score = ordered[0]
    second_score = ordered[1][1]
    margin = top_score - second_score
    signal_count = sum(1 for bucket in scores.values() if bucket > 0.8)
    content_signal = 1.0 if excerpt else 0.6 if keywords else 0.35
    path_signal = 1.0 if len(rel_path.split("/")) > 1 else 0.6
    confidence = clamp(0.35 + 0.22 * margin + 0.18 * content_signal + 0.12 * path_signal + 0.05 * signal_count)

    if margin < 0.35:
        flags.append("close_bucket_scores")
    if confidence < 0.65:
        flags.append("low_confidence")

    reasons.append(f"dominant bucket score {dominant_bucket}={top_score:.2f}")
    reasons.append(f"score margin {margin:.2f}")
    if infer_source(rel_path) == "snapshot":
        reasons.append("path looks like backup, archive, export, or recovery material")
    if form in {"document", "spreadsheet", "text"}:
        reasons.append("readable file types bias toward reference-style resources")

    return scores, dominant_bucket, confidence, reasons, flags


def bucket_dir(profile: dict[str, Any], logical_key: str) -> str:
    mapping = profile.get("bucket_names") or {}
    return str(mapping.get(logical_key) or default_profile(Path(profile.get("workspace_root", ".")))["bucket_names"][logical_key])


def existing_paths_outside_catalog(root: Path) -> set[str]:
    output: set[str] = set()
    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)
        rel_dir = rel_from_path(current_path, root)
        if rel_dir == INTERNAL_WORKSPACE or rel_dir.startswith(f"{INTERNAL_WORKSPACE}/"):
            dirnames[:] = []
            continue
        filtered = []
        for dirname in dirnames:
            child = join_rel(rel_dir, dirname) if rel_dir else dirname
            if child == INTERNAL_WORKSPACE or child.startswith(f"{INTERNAL_WORKSPACE}/"):
                continue
            filtered.append(dirname)
        dirnames[:] = filtered
        for name in filenames:
            rel_file = join_rel(rel_dir, name) if rel_dir else name
            if rel_file == INTERNAL_WORKSPACE or rel_file.startswith(f"{INTERNAL_WORKSPACE}/"):
                continue
            output.add(rel_file)
    return output
