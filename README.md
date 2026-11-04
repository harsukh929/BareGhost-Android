# BareGhost Android

Status: integration starter, not a finished app or APK.

This repository tracks integration of Bare Browser (Chromium-based Android browser) with Android-capable parts of Ghost Downloader 3.

Upstreams:
- https://github.com/BareBrowser/bare-browser
- https://github.com/XiaoYouChR/Ghost-Downloader-3

Target: Android ARM64, Bare browser and extension capabilities where supported, Ghost downloader engines where Android dependencies permit, compact in-player download control, and quality options derived only from real extractor metadata. DRM/Widevine-protected media is unavailable; no decryption or DRM bypass.

Run policy tests: python3 -m unittest discover -s tests -v

Build status: no APK is included. Bare is a Chromium patch series, not a WebView wrapper. The documented build requires a substantial Linux/Docker host (about 100 GB free disk and at least 32 GB Docker RAM). Ghost's Android host/runtime integration also needs further work. See docs/ANDROID_AUDIT.md and docs/INTEGRATION.md.

See LICENSES.md before redistribution.