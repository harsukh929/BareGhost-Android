# BareGhost Android

**Status: source integration scaffold — not a finished app or APK.**

This repository tracks a combined Android browser/downloader project using:
- [Bare Browser](https://github.com/BareBrowser/bare-browser), a Chromium patch series with Android desktop-extension support.
- [Ghost Downloader 3](https://github.com/XiaoYouChR/Ghost-Downloader-3), which publishes Android feature-pack adapters and uses a separate Android host repository in its own build workflow.

## Current work
- Pinned audited upstream revisions in `integration/upstream-lock.json`.
- Added Kotlin browser-to-downloader request and host interfaces.
- Added a versioned bridge schema and validation contract.
- Added strict media-choice policy: only actual extractor formats with safe HTTP(S) URLs; generic Download only for a direct HTTP(S) URL; DRM-protected sources are unavailable.
- Added GitHub Actions policy-test workflow.
- Documented the newly confirmed Ghost Android build boundary in `docs/GHOST_ANDROID_BUILD.md`.

## Checks
Run:
```bash
python3 -m unittest discover -s tests -v
```
The current policy suite contains 19 tests. GitHub Actions has reported successful runs for the policy workflow.

## Build status and constraints
No APK has been built or tested. Bare is a Chromium patch series, not a Gradle library or WebView wrapper. Its documented build requires a substantial x86-64 Linux/Docker environment.

Ghost's public repository contains Android adapters, but its Android Gradle host is fetched by its own workflow from the separate `XiaoYouChR/Ghost-Downloader-Android` repository using an `ANDROID_REPO_TOKEN` secret. A direct lookup of that repository returned 404 to this connection, so its source is not currently available here. A genuine integration needs authorized access to that source or a documented stable Android engine API.

The upstream Ghost APK is not a reusable library. Do not replace the missing host with dummy Gradle files or desktop Qt code.

## Target
Android ARM64 (`arm64-v8a`), with Bare's extension support where compatible, Ghost engines only where Android dependencies are verified, a compact in-player download affordance, and no DRM decryption or bypass.

See `docs/ANDROID_AUDIT.md`, `docs/GHOST_ANDROID_BUILD.md`, `docs/BRIDGE_PROTOCOL.md`, `docs/BUILD_HOST.md`, and `LICENSES.md`.
