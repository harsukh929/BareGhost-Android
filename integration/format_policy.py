"""Map real extractor metadata to honest UI choices; never extracts/downloads media."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

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
    state: str
    choices: tuple[FormatChoice, ...] = ()
    message: str = ""

def _positive_int(value: Any) -> int | None:
    try:
        number = int(value)
        return number if number > 0 else None
    except (TypeError, ValueError):
        return None

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
    if not isinstance(info, dict):
        return ChoiceState("unavailable", message="Media details could not be read.")
    if info.get("has_drm") is True or info.get("drm") is True:
        return ChoiceState("unavailable", message="This media is DRM-protected and cannot be downloaded here.")
    actual: list[FormatChoice] = []
    seen: set[str] = set()
    raw = info.get("formats")
    if isinstance(raw, list):
        for fmt in raw:
            if not isinstance(fmt, dict):
                continue
            fid, url = str(fmt.get("format_id") or "").strip(), str(fmt.get("url") or "").strip()
            if not fid or not url or fid in seen or fmt.get("has_drm") is True or fmt.get("drm") is True:
                continue
            seen.add(fid)
            actual.append(FormatChoice(fid, _label(fmt), _positive_int(fmt.get("width")), _positive_int(fmt.get("height")), (str(fmt.get("ext")).strip() or None) if fmt.get("ext") else None, (str(fmt.get("vcodec")).strip() or None) if fmt.get("vcodec") else None, (str(fmt.get("acodec")).strip() or None) if fmt.get("acodec") else None, _positive_int(fmt.get("filesize") or fmt.get("filesize_approx"))))
    if actual:
        actual.sort(key=lambda c: (c.height or 0, c.width or 0, c.format_id), reverse=True)
        return ChoiceState("formats", tuple(actual))
    if str(info.get("url") or "").strip():
        return ChoiceState("generic", message="Only a direct download is available; quality details were not provided.")
    return ChoiceState("unavailable", message="No downloadable source or selectable formats were found.")

def to_json(state: ChoiceState) -> dict[str, Any]:
    return {"state": state.state, "message": state.message, "choices": [asdict(x) for x in state.choices]}
