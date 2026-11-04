# Upstream integration checklist

## Bare Browser
- [ ] Pin and verify `integration/upstream-lock.json`.
- [ ] Fetch pinned Chromium snapshot and apply all 296 Bare patches in order.
- [ ] Bundle the exact upstream signed uBlock Origin CRX and verify its checksum/license.
- [ ] Build ARM64 `chrome_public_apk`; verify extensions, navigation, downloads and background playback.

## Ghost Downloader 3
- [ ] Obtain the Android host/runtime source corresponding to the official Android ARM64 release.
- [ ] Resolve why the public source tree's `tests/test_android.py` references absent `android/app` paths.
- [ ] Audit Python 3.13, Chaquopy/native ABI and every engine dependency.
- [ ] Integrate HTTP, BitTorrent, FTP, M3U8, DASH, eD2k, yt-dlp, GitHub and HuggingFace only after ARM64 dependency tests.
- [ ] Treat yt-dlp Android adapter as draft until verified.

## Combined app
- [ ] Define and implement the browser-to-Ghost bridge.
- [ ] Implement in-player download button and real metadata-driven quality picker.
- [ ] Add Android background service, notifications and storage flow.
- [ ] No DRM download/decryption.
- [ ] Build, sign and test on Android 16 ARM64.
- [ ] Publish corresponding source and license notices as required.
