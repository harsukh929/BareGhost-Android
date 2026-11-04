"""Map real extractor metadata to safe, honest UI choices.

This module does not extract or download media. It deliberately accepts only
HTTP(S) source URLs; protocol-specific engines (BitTorrent, FTP, etc.) should
use their own typed task path rather than smuggling arbitrary schemes here.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from urllib.parse import urlsplit


@dataclass(frozen=True)
class FormatChoice:
    format_id: str
    label: str
    width: int | None
    height: int | None
    ext: str | None
    video_codec: str | None
    audio_codec: str | None
    filesize: int | None


@dataclass(frozen=True)
class ChoiceState:
    state: str  # formats | generic | unavailable
    choices: tuple[FormatChoice, ...] = ()
    message: str = ""


def _positive_int(value: Any) -> int | None:
    try:
        number = int(value)
        return number if number > 0 else None
    except (TypeError, ValueError):
        return None


def _safe_http_url(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = urlsplit(value.strip())
        return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)
    except ValueError:
        return False


def _label(fmt: dict[str, Any]) -> str:
    height = _positive_int(fmt.get("height"))
    ext = str(fmt.get("ext") or "").strip()
    note = str(fmt.get("format_note") or "").strip()
    fps = _positive_int(fmt.get("fps"))
    parts = [f"{height}p" if height else (note or "Available format")]
    if fps:
        parts.append(f"{fps} fps")
    if ext:
        parts.append(ext.upper())
    return " · ".join(parts)


def choices_from_extractor(info: dict[str, Any] | None) -> ChoiceState:
    """Return real, safe format choices or one honest fallback state."""
    if not isinstance(info, dict):
        return ChoiceState("unavailable", message="Media details could not be read.")
    if info.get("has_drm") is True or info.get("drm") is True:
        return ChoiceState("unavailable", message="This media is DRM-protected and cannot be downloaded here.")

    actual: list[FormatChoice] = []
    seen: set[str] = set()
    raw_formats = info.get("formats")
    saw_drm_format = False
    if isinstance(raw_formats, list):
        for fmt in raw_formats:
            if not isinstance(fmt, dict):
                continue
            if fmt.get("has_drm") is True or fmt.get("drm") is True:
                saw_drm_format = True
                continue
            format_id = str(fmt.get("format_id") or "").strip()
            if not format_id or not _safe_http_url(fmt.get("url")) or format_id in seen:
                continue
            seen.add(format_id)
            actual.append(FormatChoice(
                format_id=format_id,
                label=_label(fmt),
                width=_positive_int(fmt.get("width")),
                height=_positive_int(fmt.get("height")),
                ext=(str(fmt.get("ext")).strip() or None) if fmt.get("ext") else None,
                video_codec=(str(fmt.get("vcodec")).strip() or None) if fmt.get("vcodec") else None,
                audio_codec=(str(fmt.get("acodec")).strip() or None) if fmt.get("acodec") else None,
                filesize=_positive_int(fmt.get("filesize") or fmt.get("filesize_approx")),
            ))
    if actual:
        actual.sort(key=lambda c: (c.height or 0, c.width or 0, c.format_id), reverse=True)
        return ChoiceState("formats", tuple(actual))

    # Do not fall back to a generic URL when the extractor explicitly marked
    # its only formats as DRM-protected.
    if saw_drm_format:
        return ChoiceState("unavailable", message="The available formats are DRM-protected.")

    if _safe_http_url(info.get("url")):
        return ChoiceState("generic", message="Only a direct HTTP(S) download is available; quality details were not provided.")
    return ChoiceState("unavailable", message="No safe downloadable source or selectable formats were found.")


def to_json(state: ChoiceState) -> dict[str, Any]:
    return {
        "state": state.state,
        "message": state.message,
        "choices": [asdict(item) for item in state.choices],
    }
