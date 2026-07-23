#!/usr/bin/env python3
"""Build tracked Markdown snapshots for every registered source manifest.

The generated library is an audit aid, not a replacement for structured source
manifests. It intentionally records failed locators and limits copying when the
manifest does not permit derivative use.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
import json
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "references" / "library"
USER_AGENT = (
    "divination-skills-source-audit/1.0 "
    "(+https://github.com/dajiaohuang/divination-skills)"
)
PARSER_VERSION = "1.0.1"
MAX_RESPONSE_BYTES = 20 * 1024 * 1024

IGNORED_TAGS = {
    "script",
    "style",
    "svg",
    "canvas",
    "noscript",
    "template",
}
BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "div",
    "dl",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "header",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "ul",
}


def normalize_markdown(value: str) -> str:
    """Return deterministic LF Markdown without trailing horizontal whitespace."""

    return "\n".join(line.rstrip(" \t") for line in value.splitlines()) + "\n"


@dataclass(frozen=True)
class Capture:
    locator: str
    resolved_locator: str
    status: str
    media_type: str
    sha256: str | None
    markdown: str
    note: str = ""


class HTMLMarkdownParser(HTMLParser):
    """Conservative HTML-to-Markdown converter for source snapshots."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ignored_depth = 0
        self.link_stack: list[str | None] = []
        self.list_depth = 0
        self.in_pre = False

    def _newline(self, count: int = 1) -> None:
        self.parts.append("\n" * count)

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        if tag in IGNORED_TAGS:
            self.ignored_depth += 1
            return
        if self.ignored_depth:
            return
        attr_map = dict(attrs)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._newline(2)
            self.parts.append("#" * int(tag[1]) + " ")
        elif tag == "br":
            self._newline()
        elif tag in {"ul", "ol"}:
            self.list_depth += 1
            self._newline()
        elif tag == "li":
            self._newline()
            self.parts.append("  " * max(self.list_depth - 1, 0) + "- ")
        elif tag == "blockquote":
            self._newline(2)
            self.parts.append("> ")
        elif tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "code" and not self.in_pre:
            self.parts.append("`")
        elif tag == "pre":
            self.in_pre = True
            self._newline(2)
            self.parts.append("```text\n")
        elif tag == "a":
            self.link_stack.append(attr_map.get("href"))
            self.parts.append("[")
        elif tag in {"td", "th"}:
            self.parts.append(" | ")
        elif tag in BLOCK_TAGS:
            self._newline(2)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in IGNORED_TAGS:
            self.ignored_depth = max(0, self.ignored_depth - 1)
            return
        if self.ignored_depth:
            return
        if tag in {"strong", "b"}:
            self.parts.append("**")
        elif tag in {"em", "i"}:
            self.parts.append("*")
        elif tag == "code" and not self.in_pre:
            self.parts.append("`")
        elif tag == "pre":
            self.parts.append("\n```")
            self.in_pre = False
            self._newline(2)
        elif tag == "a":
            target = self.link_stack.pop() if self.link_stack else None
            self.parts.append(f"]({target})" if target else "]")
        elif tag in {"ul", "ol"}:
            self.list_depth = max(0, self.list_depth - 1)
            self._newline()
        elif tag in BLOCK_TAGS or tag.startswith("h"):
            self._newline(2)

    def handle_data(self, data: str) -> None:
        if self.ignored_depth or not data:
            return
        if self.in_pre:
            self.parts.append(data)
            return
        value = re.sub(r"\s+", " ", data)
        if value.strip():
            if self.parts and not self.parts[-1].endswith(
                (" ", "\n", "[", "*", "`")
            ):
                self.parts.append(" ")
            self.parts.append(value.strip())

    def markdown(self) -> str:
        value = "".join(self.parts)
        value = re.sub(r"[ \t]+\n", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        value = re.sub(r"\[\s*\]\([^)]*\)", "", value)
        return value.strip()


def html_to_markdown(value: str) -> str:
    parser = HTMLMarkdownParser()
    parser.feed(value)
    parser.close()
    return parser.markdown()


def read_manifests() -> list[tuple[Path, dict[str, Any]]]:
    paths = sorted((ROOT / "catalog" / "sources").glob("*.json"))
    paths += sorted((ROOT / "systems").glob("*/sources/*.json"))
    manifests: list[tuple[Path, dict[str, Any]]] = []
    ids: set[str] = set()
    for path in paths:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        source_id = manifest["source_id"]
        if source_id in ids:
            raise ValueError(f"duplicate source_id: {source_id}")
        ids.add(source_id)
        manifests.append((path, manifest))
    return manifests


def request_bytes(url: str, *, accept: str = "*/*") -> tuple[bytes, str, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": accept},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_RESPONSE_BYTES:
            raise ValueError(
                f"response exceeds {MAX_RESPONSE_BYTES} bytes: {content_length}"
            )
        payload = response.read(MAX_RESPONSE_BYTES + 1)
        if len(payload) > MAX_RESPONSE_BYTES:
            raise ValueError(f"response exceeds {MAX_RESPONSE_BYTES} bytes")
        return (
            payload,
            response.geturl(),
            response.headers.get("Content-Type", "application/octet-stream"),
        )


def decode_text(payload: bytes, media_type: str) -> str:
    charset_match = re.search(r"charset=([^;\s]+)", media_type, re.I)
    candidates = [charset_match.group(1).strip("\"'")] if charset_match else []
    candidates += ["utf-8", "utf-8-sig", "windows-1252", "latin-1"]
    for encoding in candidates:
        try:
            return payload.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return payload.decode("utf-8", errors="replace")


def pdf_to_markdown(payload: bytes) -> str:
    executable = shutil.which("pdftotext")
    if not executable:
        return "_PDF text extraction unavailable: `pdftotext` was not found._"
    with tempfile.TemporaryDirectory(prefix="divination-reference-") as directory:
        source = Path(directory) / "source.pdf"
        target = Path(directory) / "source.txt"
        source.write_bytes(payload)
        result = subprocess.run(
            [executable, "-layout", "-nopgbrk", str(source), str(target)],
            capture_output=True,
            check=False,
            text=True,
            timeout=120,
        )
        if result.returncode != 0 or not target.exists():
            detail = (result.stderr or result.stdout).strip()
            return f"_PDF text extraction failed: {detail or 'unknown error'}_"
        text = target.read_text(encoding="utf-8", errors="replace")
        text = text.replace("\f", "\n\n")
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        return text.strip()


def pypi_capture(url: str, *, full_allowed: bool) -> Capture | None:
    match = re.match(r"https://pypi\.org/project/([^/]+)/([^/]+)/?", url)
    if not match:
        return None
    package, version = match.groups()
    api_url = f"https://pypi.org/pypi/{package}/{version}/json"
    payload, resolved, media_type = request_bytes(api_url, accept="application/json")
    data = json.loads(payload)
    info = data["info"]
    lines = [
        f"# {info.get('name', package)} {info.get('version', version)}",
        "",
        info.get("summary") or "",
        "",
        "## Package metadata",
        "",
        f"- License: {info.get('license') or 'not declared'}",
        f"- Python requirement: {info.get('requires_python') or 'not declared'}",
        f"- Project URL: {info.get('project_url') or url}",
        f"- Package URL: {info.get('package_url') or url}",
        "",
        "## Declared dependencies",
        "",
    ]
    requires = info.get("requires_dist") or []
    lines.extend(f"- `{item}`" for item in requires)
    description = (info.get("description") or "").strip()
    if description and full_allowed:
        content_type = info.get("description_content_type") or "text/plain"
        if "html" in content_type:
            description = html_to_markdown(description)
        lines += ["", "## Published description", "", description]
    return Capture(
        locator=url,
        resolved_locator=resolved,
        status="captured" if full_allowed else "metadata_only",
        media_type=media_type,
        sha256=hashlib.sha256(payload).hexdigest(),
        markdown="\n".join(lines).strip(),
        note=f"Retrieved through the PyPI JSON API: {api_url}",
    )


def github_capture(url: str, *, full_allowed: bool) -> Capture | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.lower() != "github.com":
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    owner, repository = parts[:2]
    repository = repository.removesuffix(".git")
    api_url = f"https://api.github.com/repos/{owner}/{repository}"
    payload, resolved, media_type = request_bytes(api_url, accept="application/json")
    data = json.loads(payload)
    lines = [
        f"# {data.get('full_name', f'{owner}/{repository}')}",
        "",
        data.get("description") or "",
        "",
        "## Repository metadata",
        "",
        f"- Default branch: `{data.get('default_branch')}`",
        f"- License: `{(data.get('license') or {}).get('spdx_id')}`",
        f"- Archived: `{data.get('archived')}`",
        f"- Created: `{data.get('created_at')}`",
        f"- Updated: `{data.get('updated_at')}`",
        f"- Repository: {data.get('html_url') or url}",
    ]
    note = f"Retrieved repository metadata through the GitHub API: {api_url}"
    if full_allowed:
        readme_url = (
            f"https://raw.githubusercontent.com/{owner}/{repository}/"
            f"{data.get('default_branch', 'main')}/README.md"
        )
        try:
            readme_payload, readme_resolved, _ = request_bytes(readme_url)
            readme = decode_text(readme_payload, "text/markdown; charset=utf-8")
            lines += ["", "## Upstream README", "", readme.strip()]
            note += (
                f"; README snapshot {readme_resolved} "
                f"sha256={hashlib.sha256(readme_payload).hexdigest()}"
            )
        except (OSError, ValueError, urllib.error.URLError) as error:
            note += f"; README capture failed: {error}"
    return Capture(
        locator=url,
        resolved_locator=resolved,
        status="captured" if full_allowed else "metadata_only",
        media_type=media_type,
        sha256=hashlib.sha256(payload).hexdigest(),
        markdown="\n".join(lines).strip(),
        note=note,
    )


def wikisource_capture(url: str) -> Capture | None:
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc.endswith("wikisource.org") or "/wiki/" not in parsed.path:
        return None
    page = urllib.parse.unquote(parsed.path.split("/wiki/", 1)[1])
    api_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            "/w/api.php",
            "",
            urllib.parse.urlencode(
                {
                    "action": "parse",
                    "page": page,
                    "prop": "text|displaytitle|sections",
                    "format": "json",
                    "formatversion": "2",
                }
            ),
            "",
        )
    )
    payload, resolved, media_type = request_bytes(api_url, accept="application/json")
    data = json.loads(payload)["parse"]
    title = html.unescape(re.sub(r"<[^>]+>", "", data.get("displaytitle", page)))
    markdown = html_to_markdown(data["text"])
    section_lines = [
        f"- {section.get('number')}: {html.unescape(section.get('line', ''))}"
        for section in data.get("sections", [])
    ]
    content = [f"# {title}", "", "## Parsed transcription", "", markdown]
    if section_lines:
        content += ["", "## API section index", "", *section_lines]
    return Capture(
        locator=url,
        resolved_locator=resolved,
        status="captured",
        media_type=media_type,
        sha256=hashlib.sha256(payload).hexdigest(),
        markdown="\n".join(content).strip(),
        note=(
            "Parsed through the MediaWiki API. The transcription retains the "
            "source site's declared CC BY-SA terms."
        ),
    )


def gutenberg_capture(url: str) -> Capture | None:
    match = re.match(r"https://www\.gutenberg\.org/ebooks/(\d+)", url)
    if not match:
        return None
    ebook_id = match.group(1)
    text_url = f"https://www.gutenberg.org/ebooks/{ebook_id}.txt.utf-8"
    payload, resolved, media_type = request_bytes(text_url, accept="text/plain")
    text = decode_text(payload, media_type).replace("\r\n", "\n").strip()
    return Capture(
        locator=url,
        resolved_locator=resolved,
        status="captured",
        media_type=media_type,
        sha256=hashlib.sha256(payload).hexdigest(),
        markdown=text,
        note=(
            f"Resolved the ebook landing page to its UTF-8 text edition: {text_url}. "
            "The Project Gutenberg header and footer are retained."
        ),
    )


def wellcome_capture(url: str) -> Capture | None:
    match = re.match(
        r"https://wellcomecollection\.org/works/([A-Za-z0-9]+)", url
    )
    if not match:
        return None
    work_id = match.group(1)
    api_url = (
        "https://api.wellcomecollection.org/catalogue/v2/works/"
        f"{work_id}?include=identifiers,items,subjects,contributors,genres"
    )
    payload, resolved, media_type = request_bytes(api_url, accept="application/json")
    data = json.loads(payload)
    lines = [
        f"# {data.get('title', work_id)}",
        "",
        "## Catalogue metadata",
        "",
        f"- Work ID: `{data.get('id', work_id)}`",
        f"- Work type: `{(data.get('workType') or {}).get('label')}`",
        f"- Production: `{data.get('production', [])}`",
        f"- Languages: `{data.get('languages', [])}`",
        f"- Physical description: {data.get('physicalDescription', '')}",
        f"- Description: {data.get('description', '')}",
        "",
        "## Contributors",
        "",
    ]
    for contributor in data.get("contributors", []):
        agent = contributor.get("agent") or {}
        lines.append(f"- {agent.get('label', 'unknown')}")
    return Capture(
        locator=url,
        resolved_locator=resolved,
        status="captured",
        media_type=media_type,
        sha256=hashlib.sha256(payload).hexdigest(),
        markdown="\n".join(lines).strip(),
        note=f"Retrieved catalogue metadata through the Wellcome API: {api_url}",
    )


def npm_capture(url: str) -> Capture | None:
    match = re.match(
        r"https://www\.npmjs\.com/package/([^/]+)(?:/v/([^/]+))?", url
    )
    if not match:
        return None
    package, version = match.groups()
    version = version or "latest"
    api_url = f"https://registry.npmjs.org/{package}/{version}"
    payload, resolved, media_type = request_bytes(api_url, accept="application/json")
    data = json.loads(payload)
    lines = [
        f"# {data.get('name', package)} {data.get('version', version)}",
        "",
        data.get("description") or "",
        "",
        "## Package metadata",
        "",
        f"- License: `{data.get('license')}`",
        f"- Repository: `{data.get('repository')}`",
        f"- Dependencies: `{data.get('dependencies', {})}`",
    ]
    return Capture(
        locator=url,
        resolved_locator=resolved,
        status="metadata_only",
        media_type=media_type,
        sha256=hashlib.sha256(payload).hexdigest(),
        markdown="\n".join(lines).strip(),
        note=f"Retrieved through the npm registry API: {api_url}",
    )


def local_capture(locator: str) -> Capture:
    path = (ROOT / locator).resolve()
    if ROOT not in path.parents and path != ROOT:
        raise ValueError(f"local locator escapes repository: {locator}")
    if not path.is_file():
        return Capture(
            locator=locator,
            resolved_locator=locator,
            status="failed",
            media_type="text/plain",
            sha256=None,
            markdown="",
            note="Local locator does not identify a file.",
        )
    payload = path.read_bytes()
    text = decode_text(payload, "text/plain; charset=utf-8")
    return Capture(
        locator=locator,
        resolved_locator=path.relative_to(ROOT).as_posix(),
        status="captured",
        media_type="text/markdown",
        sha256=hashlib.sha256(payload).hexdigest(),
        markdown=text.strip(),
        note="Copied from the repository-local authoritative contract.",
    )


CURATED_FALLBACKS = {
    "SRC-ASTRONOMY-NOAA-SOLAR-001": """# NOAA public-domain notice

NOAA-authored United States government information is generally in the public
domain. Reuse should credit NOAA, must not imply NOAA endorsement, and must
separately review any third-party material identified on an NOAA page.

This fallback records the rights rule used by the source manifest because the
registered copyright-policy host did not resolve during automated capture.
""",
    "SRC-ICHING-LOC-17845": """# Library of Congress item 2021666491

- Title: Zhou yi zhu shu : Shi san juan / 周易注疏 : 十三卷
- Contributor: Kong Yingda (574–648)
- Date: early Southern Song print, 1127–1279
- Extent: six volumes
- Contents: 64 hexagrams, 384 lines, and classical commentary layers
- Digital ID: https://hdl.loc.gov/loc.wdl/wdl.17845
- Rights: the Library of Congress reports no known copyright restrictions

The digitized object is image-based. This fallback records catalogue facts only;
it does not claim OCR completeness or silently substitute a modern edition.
""",
    "SRC-LENORMAND-BM-HOPE-001": """# British Museum object 1896,0501.495

- Title: Das Spiel der Hofnung
- Object type: print; playing-card
- Description: complete pack of 36 hand-coloured playing cards with French suits
- Publisher: G. P. J. Bieling
- Production: Nuremberg, circa 1800–1850
- Card dimensions: 66 × 50 mm
- Registration number: 1896,0501.495
- Catalogue note: each card combines a numbered vignette, French suit value, and
  a German-suit equivalent

Only object and card-identity facts are retained. Museum photography and
catalogue prose are not redistributed.
""",
    "SRC-NUMEROLOGY-CHEIRO-001": """# Google Books bibliographic record

- Title: Cheiro's Book of Numbers, Volumes 1–2
- Author: Cheiro
- Publisher: Garden City Publishing Company
- Date: 1927
- Length: 304 pages
- Digitized from: University of Illinois at Urbana-Champaign
- Google Books volume ID: `-qMgZzxmN1oC`

Google Books exposes bibliographic metadata and selected-page/snippet access.
This snapshot does not claim a complete OCR transcription. The production rule
layer retains only the historical letter-value table and reduction facts.
""",
    "SRC-RUNES-SHM-KYLVER-001": """# Kylverstenen

- Museum: Swedish History Museum
- Collection object: 267753
- Date: fifth century
- Inscription: the older runic row from beginning to end
- Inventory fact: the older row contains 24 characters, compared with the
  later Viking-period row of 16 characters
- Interpretive caveat: the final tree-like sign has disputed readings

Only museum-established object and inscription facts are retained. Images and
museum prose are not redistributed.
""",
}


def remote_capture(
    source_id: str,
    url: str,
    *,
    full_allowed: bool,
) -> Capture:
    handlers = (
        lambda: pypi_capture(url, full_allowed=full_allowed),
        lambda: wikisource_capture(url) if full_allowed else None,
        lambda: gutenberg_capture(url) if full_allowed else None,
        lambda: wellcome_capture(url),
        lambda: npm_capture(url),
        lambda: github_capture(url, full_allowed=full_allowed),
    )
    for handler in handlers:
        capture = handler()
        if capture is not None:
            return capture
    payload, resolved, media_type = request_bytes(url)
    digest = hashlib.sha256(payload).hexdigest()
    if not full_allowed:
        safe_summary = CURATED_FALLBACKS.get(source_id)
        return Capture(
            locator=url,
            resolved_locator=resolved,
            status="metadata_only",
            media_type=media_type,
            sha256=digest,
            markdown=safe_summary.strip()
            if safe_summary
            else (
                "_The locator was resolved and hashed, but its expressive content "
                "was not copied because the manifest does not authorize derivative "
                "use._"
            ),
            note="Rights-safe metadata-only capture.",
        )
    media_lower = media_type.lower()
    if "pdf" in media_lower or (
        "octet-stream" in media_lower and resolved.lower().endswith(".pdf")
    ):
        markdown = pdf_to_markdown(payload)
    elif "json" in media_lower:
        markdown = "```json\n" + json.dumps(
            json.loads(payload), ensure_ascii=False, indent=2
        ) + "\n```"
    else:
        markdown = html_to_markdown(decode_text(payload, media_type))
    return Capture(
        locator=url,
        resolved_locator=resolved,
        status="captured",
        media_type=media_type,
        sha256=digest,
        markdown=markdown,
    )


def capture_locator(
    source_id: str,
    locator: dict[str, Any],
    *,
    full_allowed: bool,
) -> Capture:
    value = locator["value"]
    if locator["kind"] == "local":
        return local_capture(value)
    if not value.startswith(("http://", "https://")):
        return Capture(
            locator=value,
            resolved_locator=value,
            status="metadata_only",
            media_type="text/plain",
            sha256=None,
            markdown=f"_Non-HTTP locator recorded without network resolution: `{value}`._",
        )
    try:
        return remote_capture(source_id, value, full_allowed=full_allowed)
    except (
        OSError,
        TimeoutError,
        ValueError,
        json.JSONDecodeError,
        subprocess.SubprocessError,
        urllib.error.URLError,
    ) as error:
        fallback = CURATED_FALLBACKS.get(source_id, "")
        return Capture(
            locator=value,
            resolved_locator=value,
            status="curated_fallback" if fallback else "failed",
            media_type="text/markdown" if fallback else "text/plain",
            sha256=None,
            markdown=fallback.strip(),
            note=f"Automated retrieval failed: {type(error).__name__}: {error}",
        )


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return json.dumps(str(value), ensure_ascii=False)


def full_copy_allowed(manifest: dict[str, Any]) -> bool:
    license_id = manifest["license"]["identifier"].lower()
    return (
        manifest["rights"]["derivative_use"] == "allowed"
        and "facts-only" not in license_id
    )


def render_source(
    manifest_path: Path,
    manifest: dict[str, Any],
    captures: list[Capture],
) -> str:
    source_id = manifest["source_id"]
    full_allowed = full_copy_allowed(manifest)
    payload_hashes = [item.sha256 for item in captures if item.sha256]
    aggregate = hashlib.sha256("".join(payload_hashes).encode()).hexdigest()
    lines = [
        "---",
        f"source_id: {yaml_scalar(source_id)}",
        f"title: {yaml_scalar(manifest['title'])}",
        f"parser_version: {yaml_scalar(PARSER_VERSION)}",
        f"retrieved_at: {yaml_scalar(manifest['retrieved_at'])}",
        f"manifest_path: {yaml_scalar(manifest_path.relative_to(ROOT).as_posix())}",
        f"capture_mode: {yaml_scalar('full' if full_allowed else 'metadata_only')}",
        f"aggregate_payload_sha256: {yaml_scalar(aggregate)}",
        f"license: {yaml_scalar(manifest['license']['identifier'])}",
        "---",
        "",
        f"# {manifest['title']}",
        "",
        "> Generated audit snapshot. The structured source manifest remains the",
        "> authority for rights, lineage, and production status.",
        "",
        "## Provenance",
        "",
        f"- Source ID: `{source_id}`",
        f"- Manifest: `{manifest_path.relative_to(ROOT).as_posix()}`",
        f"- Type: `{manifest['source_type']}`",
        f"- Language: `{manifest['language']}`",
        f"- Edition/version: `{manifest.get('edition_or_version', 'not recorded')}`",
        f"- Retrieved: `{manifest['retrieved_at']}`",
        f"- Usage status: `{manifest['usage_status']}`",
        f"- Systems: {', '.join(f'`{item}`' for item in manifest['systems'])}",
        f"- Lineages: {', '.join(f'`{item}`' for item in manifest['lineages'])}",
        "",
        "## Rights envelope",
        "",
        f"- License: `{manifest['license']['identifier']}`",
        f"- Rights review: `{manifest['rights_review']['status']}`",
        f"- Derivative use: `{manifest['rights']['derivative_use']}`",
        f"- Dataset use: `{manifest['rights']['dataset']}`",
        f"- Evidence: {manifest['rights_review']['evidence']}",
    ]
    if manifest["license"].get("notes"):
        lines.append(f"- License notes: {manifest['license']['notes']}")
    lines += ["", "## Locator capture ledger", ""]
    for index, capture in enumerate(captures, start=1):
        lines += [
            f"### Locator {index}",
            "",
            f"- Registered: {capture.locator}",
            f"- Resolved: {capture.resolved_locator}",
            f"- Status: `{capture.status}`",
            f"- Media type: `{capture.media_type}`",
            f"- SHA-256: `{capture.sha256 or 'unavailable'}`",
        ]
        if capture.note:
            lines.append(f"- Note: {capture.note}")
        if capture.markdown:
            lines += ["", "#### Parsed material", "", capture.markdown]
        lines.append("")
    lines += [
        "## Manifest quality note",
        "",
        manifest["quality"]["notes"],
        "",
        "## Reproducibility",
        "",
        f"- Parser: `tooling/scripts/build_reference_library.py` v{PARSER_VERSION}",
        f"- Aggregate payload SHA-256: `{aggregate}`",
        "- Use `--check` to verify tracked snapshot integrity; run without it to "
        "refresh remote material.",
        "",
    ]
    return "\n".join(lines)


def render_index(rows: list[dict[str, Any]]) -> str:
    captured = sum(row["failed"] == 0 for row in rows)
    lines = [
        "# Reference library index",
        "",
        "This directory contains tracked, rights-aware Markdown snapshots for every",
        "registered source manifest. It excludes `references/upstream/`, which remains",
        "an ignored collection of non-production comparison repositories.",
        "",
        f"- Parser version: `{PARSER_VERSION}`",
        f"- Registered sources: `{len(rows)}`",
        f"- Sources without failed locators: `{captured}`",
        f"- Sources with at least one failed locator: `{len(rows) - captured}`",
        "",
        "| Source ID | Systems | Mode | Captures | Failed | Snapshot |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {source_id} | {systems} | {mode} | {captures} | {failed} | "
            "[Markdown]({source_id}.md) |".format(**row)
        )
    lines += [
        "",
        "A failed locator is retained as audit evidence. A source may still have a",
        "usable snapshot through another locator or a clearly marked curated fallback.",
        "",
    ]
    return "\n".join(lines)


def update_manifest_snapshots(
    manifests: list[tuple[Path, dict[str, Any]]],
) -> None:
    for manifest_path, manifest in manifests:
        snapshot_path = OUTPUT_ROOT / f"{manifest['source_id']}.md"
        digest = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
        manifest["local_snapshot"] = {
            "retained": True,
            "path": snapshot_path.relative_to(ROOT).as_posix(),
            "sha256": digest,
        }
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )


def verify_existing(manifests: list[tuple[Path, dict[str, Any]]]) -> int:
    """Verify committed snapshots without making nondeterministic network requests."""

    rows: list[dict[str, Any]] = []
    mismatches: list[str] = []
    expected_files = {"INDEX.md", "README.md"}
    for _, manifest in manifests:
        source_id = manifest["source_id"]
        filename = f"{source_id}.md"
        expected_files.add(filename)
        output_path = OUTPUT_ROOT / filename
        snapshot = manifest.get("local_snapshot", {})
        if not output_path.is_file():
            mismatches.append(filename)
            continue
        content = output_path.read_text(encoding="utf-8")
        digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
        expected_path = output_path.relative_to(ROOT).as_posix()
        if snapshot.get("path") != expected_path or snapshot.get("sha256") != digest:
            mismatches.append(filename)
        rows.append(
            {
                "source_id": source_id,
                "systems": ", ".join(manifest["systems"]),
                "mode": "full" if full_copy_allowed(manifest) else "metadata",
                "captures": content.count("\n- Registered: "),
                "failed": content.count("\n- Status: `failed`"),
            }
        )
    index_path = OUTPUT_ROOT / "INDEX.md"
    expected_index = render_index(rows)
    if not index_path.is_file() or index_path.read_text(encoding="utf-8") != expected_index:
        mismatches.append("INDEX.md")
    unexpected = {path.name for path in OUTPUT_ROOT.glob("*.md")} - expected_files
    mismatches.extend(sorted(f"unexpected:{item}" for item in unexpected))
    if mismatches:
        print("Reference library differs:")
        for mismatch in sorted(set(mismatches)):
            print(f"- {mismatch}")
        return 1
    print(f"Reference library verified: {len(rows)} sources")
    return 0


def build(*, check: bool, update_manifests: bool) -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    manifests = read_manifests()
    if check:
        return verify_existing(manifests)
    rows: list[dict[str, Any]] = []
    captured_by_source: dict[str, list[Capture | None]] = {
        manifest["source_id"]: [None] * len(manifest["locators"])
        for _, manifest in manifests
    }
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_map: dict[concurrent.futures.Future[Capture], tuple[str, int]] = {}
        for _, manifest in manifests:
            full_allowed = full_copy_allowed(manifest)
            for index, locator in enumerate(manifest["locators"]):
                future = executor.submit(
                    capture_locator,
                    manifest["source_id"],
                    locator,
                    full_allowed=full_allowed,
                )
                future_map[future] = (manifest["source_id"], index)
        for future in concurrent.futures.as_completed(future_map):
            source_id, index = future_map[future]
            captured_by_source[source_id][index] = future.result()
    for manifest_path, manifest in manifests:
        full_allowed = full_copy_allowed(manifest)
        captures = [
            capture
            for capture in captured_by_source[manifest["source_id"]]
            if capture is not None
        ]
        content = normalize_markdown(render_source(manifest_path, manifest, captures))
        filename = f"{manifest['source_id']}.md"
        output_path = OUTPUT_ROOT / filename
        output_path.write_text(content, encoding="utf-8", newline="\n")
        rows.append(
            {
                "source_id": manifest["source_id"],
                "systems": ", ".join(manifest["systems"]),
                "mode": "full" if full_allowed else "metadata",
                "captures": len(captures),
                "failed": sum(item.status == "failed" for item in captures),
            }
        )
    index = normalize_markdown(render_index(rows))
    index_path = OUTPUT_ROOT / "INDEX.md"
    index_path.write_text(index, encoding="utf-8", newline="\n")
    if update_manifests:
        update_manifest_snapshots(manifests)
    print(f"Reference library built: {len(rows)} sources")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed snapshots and indexes without network access",
    )
    parser.add_argument(
        "--update-manifests",
        action="store_true",
        help="record generated Markdown paths and SHA-256 values in source manifests",
    )
    args = parser.parse_args()
    if args.check and args.update_manifests:
        parser.error("--check and --update-manifests cannot be combined")
    return build(check=args.check, update_manifests=args.update_manifests)


if __name__ == "__main__":
    raise SystemExit(main())
