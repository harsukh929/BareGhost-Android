# BareGhost Android

**Status: source integration scaffold — not a finished app or APK.**

This repository tracks a combined Android browser/downloader project using:
- [Bare Browser](https://github.com/BareBrowser/bare-browser), a Chromium patch series with Android desktop-extension support.
- [Ghost Downloader 3](https://github.com/XiaoYouChR/Ghost-Downloader-3), whose public tree includes Android adapter modules but does not currently expose the Android host project referenced by its own Android tests.

## Current work
- Pinned audited upstream revisions in `integration/upstream-lock.json`.
- Added Kotlin browser-to-downloader request and host interfaces.
- Added a versioned bridge schema and validation contract.
- Added strict media-choice policy: only actual extractor formats with safe HTTP(S) URLs; generic Download only for a direct HTTP(S) URL; DRM-protected sources are unavailable.
- Added GitHub Actions policy-test workflow.

## Checks
Run:
```bash
python3 -m unittest discover -s tests -v
```
The current policy suite contains 19 tests. GitHub Actions has reported successful runs for the policy workflow.

## Build status and constraints
No APK has been built or tested. Bare is a Chromium patch series, not a Gradle library or WebView wrapper. Its documented build requires an x86-64 Ubuntu 22.04 Docker environment, at least 32 GB RAM allocated to Docker, and about 100 GB free disk. The available workspace does not meet these requirements.

Ghost's public source tree is missing Android host files referenced by `tests/test_android.py`; the yt-dlp Android adapter is also marked draft. A real in-process integration requires the corresponding host/runtime source or a documented stable engine API. The upstream APK cannot simply be embedded as a library.

## Target
Android ARM64 (`arm64-v8a`), with Bare's extension support where compatible, Ghost engines only where Android dependencies are verified, a compact in-player download affordance, and no DRM decryption or bypass.

See `docs/ANDROID_AUDIT.md`, `docs/BRIDGE_PROTOCOL.md`, `docs/BUILD_HOST.md`, and `LICENSES.md`.
