# Upstream Android audit (verified 2026-11-04)

## Bare Browser
- Current audited main commit: `e776f77629bb915e0f3df63449f1f993cc1b0648`.
- README reports Bare `2.0.0-beta.6`, Chromium `156.0.8078.73`, Android 10+, ARM64/32-bit ARM, and 296 patches.
- Bare is a Chromium patch series, not an embeddable Android library or WebView wrapper.
- The source build guide pins Chromium commit `2f9a11097447f226133bc1a31c787291a5eeab98` and requires Docker with at least 32 GB allocated RAM, about 100 GB free disk, an x86-64 Ubuntu 22.04 container, and an ARM64 Android device for testing.
- Build steps include fetching Chromium/depot_tools, applying the complete ordered patch series, bundling the signed uBlock Origin CRX, GN configuration, then `autoninja ... chrome_public_apk`.

## Ghost Downloader 3
- Current audited main commit: `256b082166fec444b517dd3f4bb88c55ead1325b`.
- README declares Android 9+ and `arm64-v8a`; the latest inspected release page advertises an Android ARM64 APK (`v4.4.5`).
- Android adapters are present for HTTP, FTP, BitTorrent, eD2k, M3U8, yt-dlp, Bilibili, GitHub and HuggingFace. The yt-dlp adapter is explicitly a draft.
- The public source tree includes `tests/test_android.py`, which expects `android/app/build.gradle.kts` and `android/app/src/main/python/app/config/cfg.py`, but those Android host paths were absent from the recursive `main` tree inspected. Therefore the public source snapshot does not currently provide the complete Android host project that its test expects.
- The upstream Android APK demonstrates that an Android build exists, but it does not by itself provide embeddable source or prove a reusable library API.

## Integration decision
- Do not attempt to embed Ghost's APK as if it were a library. Obtain/build its Android host source or reproduce the Android host against its documented Python/runtime bridge.
- Keep Bare as the browser base and Ghost as a separately audited engine/runtime integration until a stable in-process interface is proven.
- Pin both upstream commits in `integration/upstream-lock.json` before importing code.

## Local build limitation
This workspace does not have Docker, Gradle or sufficient RAM/disk for Bare's documented Chromium build. No APK has been built or tested here.
