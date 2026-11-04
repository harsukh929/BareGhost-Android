"""Validation for the browser-to-downloader hand-off contract.

This is a pure policy module. It does not fetch, probe, or download media.
"""
from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Mapping
from urllib.parse import urlsplit

_HEADER_NAME = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
_MAX_HEADERS = 64
_MAX_HEADER_VALUE = 8192

@dataclass(frozen=True)
class DownloadRequest:
    page_url: str
    media_url: str
    title: str | None = None
    format_id: str | None = None
    headers: Mapping[str, str] | None = None
    is_incognito: bool = False
    allow_session_cookies: bool = False

def _is_http_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)
    except (TypeError, ValueError):
        return False

def validate_request(request: DownloadRequest) -> None:
    if not _is_http_url(request.page_url):
        raise ValueError("page_url must be an absolute HTTP(S) URL")
    if not _is_http_url(request.media_url):
        raise ValueError("media_url must be an absolute HTTP(S) URL")
    if request.is_incognito and request.allow_session_cookies:
        raise ValueError("Incognito requests cannot forward session cookies")
    if request.title is not None and len(request.title) > 512:
        raise ValueError("title is too long")
    if request.format_id is not None and len(request.format_id) > 128:
        raise ValueError("format_id is too long")
    headers = request.headers or {}
    if len(headers) > _MAX_HEADERS:
        raise ValueError("too many headers")
    for name, value in headers.items():
        if not isinstance(name, str) or not _HEADER_NAME.fullmatch(name):
            raise ValueError("invalid HTTP header name")
        if not isinstance(value, str) or len(value) > _MAX_HEADER_VALUE:
            raise ValueError("invalid HTTP header value")
        if "\r" in value or "\n" in value:
            raise ValueError("HTTP header values cannot contain CR or LF")
        if name.lower() in {"cookie", "cookie2"} and not request.allow_session_cookies:
            raise ValueError("Cookie headers require explicit user permission")
